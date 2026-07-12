from contextlib import suppress
import os
import time
import unittest

from ament_index_python.packages import get_package_share_path
from control_msgs.action import FollowJointTrajectory, GripperCommand
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_testing
from launch_testing_ros import MessagePump
from moveit_msgs.action import MoveGroup
import pytest
import rclpy
from rclpy.action import ActionClient
from sensor_msgs.msg import JointState
from std_msgs.msg import Header


LIVE_ROBOT_IP = os.environ.get("LEBAI_TEST_ROBOT_IP")
STACK_NAMESPACES = ("robot_1", "robot_2")
ACTION_SERVICE_SUFFIX = "/_action/send_goal"


@pytest.mark.integration
@pytest.mark.skipif(
    not LIVE_ROBOT_IP,
    reason="LEBAI_TEST_ROBOT_IP is not set",
)
@pytest.mark.launch_test
def generate_test_description():
    if not LIVE_ROBOT_IP:
        pytest.skip("LEBAI_TEST_ROBOT_IP is not set")

    os.environ["ROS_DOMAIN_ID"] = str(1 + os.getpid() % 230)
    launch_path = (
        get_package_share_path("lebai_lm3_moveit_config")
        / "launch"
        / "lm3.launch.py"
    )
    stacks = [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(launch_path)),
            launch_arguments={
                "namespace": namespace,
                "robot_ip": LIVE_ROBOT_IP,
                "simulator": "true",
                "has_gripper": "true",
            }.items(),
        )
        for namespace in STACK_NAMESPACES
    ]
    return LaunchDescription([
        *stacks,
        launch_testing.actions.ReadyToTest(),
    ])


@pytest.mark.integration
@pytest.mark.skipif(
    not LIVE_ROBOT_IP,
    reason="LEBAI_TEST_ROBOT_IP is not set",
)
class TestNamespacedMoveItStacks(unittest.TestCase):
    def setUp(self):
        self.node = None
        self.pump = None
        self.pump_started = False
        self.action_clients = []
        self.publishers = []
        self.subscriptions = []
        if not rclpy.ok():
            rclpy.init()
        try:
            self.node = rclpy.create_node("namespaced_moveit_stack_probe")
            self.pump = MessagePump(self.node)
            self.pump.start()
            self.pump_started = True
        except BaseException:
            self._cleanup_ros()
            raise

    def tearDown(self):
        self._cleanup_ros()

    def _cleanup_ros(self):
        if self.pump is not None and self.pump_started:
            with suppress(Exception):
                self.pump.stop()
            self.pump_started = False
        for client in reversed(self.action_clients):
            with suppress(Exception):
                client.destroy()
        self.action_clients.clear()
        if self.node is not None:
            for subscription in reversed(self.subscriptions):
                with suppress(Exception):
                    self.node.destroy_subscription(subscription)
            for publisher in reversed(self.publishers):
                with suppress(Exception):
                    self.node.destroy_publisher(publisher)
            with suppress(Exception):
                self.node.destroy_node()
            self.node = None
        if rclpy.ok():
            with suppress(Exception):
                rclpy.shutdown()

    @pytest.mark.integration
    def test_state_and_action_graphs_are_isolated_by_namespace(self):
        state_topics = {
            namespace: f"/{namespace}/model/joint_states"
            for namespace in STACK_NAMESPACES
        }
        expected_action_types = {
            namespace: {
                f"/{namespace}/move_action": MoveGroup,
                (
                    f"/{namespace}/lebai_trajectory_controller/"
                    "follow_joint_trajectory"
                ): FollowJointTrajectory,
                f"/{namespace}/lebai_gripper_controller/gripper_cmd": (
                    GripperCommand
                ),
            }
            for namespace in STACK_NAMESPACES
        }

        self._wait_until(
            lambda: self._state_subscribers_are_ready(state_topics),
            timeout_sec=60.0,
            description="namespaced MoveIt state subscribers",
        )
        self._assert_state_subscriber_isolation(state_topics)
        self._publish_and_observe_sentinels(state_topics)

        for actions in expected_action_types.values():
            for action_name, action_type in actions.items():
                client = ActionClient(self.node, action_type, action_name)
                self.action_clients.append(client)
                self.assertTrue(
                    client.wait_for_server(timeout_sec=60.0),
                    f"action server did not appear: {action_name}",
                )

        expected_actions = {
            action_name
            for actions in expected_action_types.values()
            for action_name in actions
        }
        self._wait_until(
            lambda: expected_actions.issubset(self._action_server_names()),
            timeout_sec=10.0,
            description="namespaced action service graph",
        )
        self.assertTrue(expected_actions.issubset(self._action_server_names()))
        self.assertTrue(self._forbidden_action_names().isdisjoint(
            self._action_server_names()
        ))

        topic_names = {
            topic_name
            for topic_name, _topic_types in self.node.get_topic_names_and_types()
        }
        expected_moveit_topics = {
            f"/{namespace}/{topic}"
            for namespace in STACK_NAMESPACES
            for topic in (
                "display_planned_path",
                "monitored_planning_scene",
            )
        }
        self.assertTrue(expected_moveit_topics.issubset(topic_names))
        self.assertTrue({
            "/move_action",
            "/joint_states",
            "/display_planned_path",
            "/monitored_planning_scene",
        }.isdisjoint(topic_names))

    def _state_subscribers_are_ready(self, state_topics):
        return all(
            {
                (f"/{namespace}", "move_group"),
                (f"/{namespace}", "robot_state_publisher"),
            }.issubset(self._subscriber_nodes(topic_name))
            for namespace, topic_name in state_topics.items()
        )

    def _assert_state_subscriber_isolation(self, state_topics):
        subscriber_graph = {
            namespace: self._subscriber_nodes(topic_name)
            for namespace, topic_name in state_topics.items()
        }
        for namespace in STACK_NAMESPACES:
            expected_nodes = {
                (f"/{namespace}", "move_group"),
                (f"/{namespace}", "robot_state_publisher"),
            }
            other_namespace = next(
                candidate
                for candidate in STACK_NAMESPACES
                if candidate != namespace
            )
            self.assertTrue(expected_nodes.issubset(subscriber_graph[namespace]))
            self.assertTrue(expected_nodes.isdisjoint(
                subscriber_graph[other_namespace]
            ))

    def _subscriber_nodes(self, topic_name):
        return {
            (endpoint.node_namespace, endpoint.node_name)
            for endpoint in self.node.get_subscriptions_info_by_topic(topic_name)
        }

    def _publish_and_observe_sentinels(self, state_topics):
        received = {namespace: [] for namespace in STACK_NAMESPACES}
        for index, (namespace, topic_name) in enumerate(
            state_topics.items(),
            start=1,
        ):
            self.publishers.append(
                self.node.create_publisher(JointState, topic_name, 10)
            )
            self.subscriptions.append(
                self.node.create_subscription(
                    JointState,
                    topic_name,
                    lambda message, key=namespace: received[key].append(message),
                    10,
                )
            )

            message = JointState(
                header=Header(frame_id=f"{namespace}_sentinel"),
                name=["joint_1"],
                position=[float(index)],
            )
            deadline = time.monotonic() + 10.0
            while (
                time.monotonic() < deadline
                and not any(
                    sample.header.frame_id == f"{namespace}_sentinel"
                    for sample in received[namespace]
                )
            ):
                self.publishers[-1].publish(message)
                time.sleep(0.05)

            sentinel_samples = [
                sample
                for sample in received[namespace]
                if sample.header.frame_id == f"{namespace}_sentinel"
            ]
            self.assertTrue(sentinel_samples)
            self.assertEqual(
                sentinel_samples[-1].header.frame_id,
                f"{namespace}_sentinel",
            )
            self.assertEqual(sentinel_samples[-1].position, [float(index)])

    def _action_server_names(self):
        return {
            service_name[:-len(ACTION_SERVICE_SUFFIX)]
            for service_name, _service_types in self.node.get_service_names_and_types()
            if service_name.endswith(ACTION_SERVICE_SUFFIX)
        }

    @staticmethod
    def _forbidden_action_names():
        forbidden = {
            "/move_action",
            "/lebai_trajectory_controller",
            "/lebai_trajectory_controller/follow_joint_trajectory",
            "/lebai_gripper_controller/gripper_cmd",
        }
        for namespace in STACK_NAMESPACES:
            forbidden.update({
                f"/{namespace}/lebai_trajectory_controller",
                f"/{namespace}/follow_joint_trajectory",
                f"/{namespace}/gripper_cmd",
            })
        return forbidden

    def _wait_until(self, predicate, timeout_sec, description):
        deadline = time.monotonic() + timeout_sec
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.05)
        self.fail(f"timed out waiting for {description}")
