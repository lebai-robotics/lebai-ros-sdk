from contextlib import suppress
import os
import signal
import subprocess
import sys
import time
import unittest

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_testing
from launch_testing_ros import MessagePump
import pytest
import pytest_xvfb
import rclpy
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String
import yaml


SUPPORT_SHARE = get_package_share_path("lebai_lm3_support")
DIRECT_DISPLAY_LAUNCHES = (
    "display_gripper.launch",
    "display_gripper.py",
    "display_lm3.launch.py",
    "display_lm3_l1.launch.py",
    "display_lm3_l1_with_gripper.launch.py",
    "display_lm3_with_gripper.launch.py",
)
CASE_INDEX_ENV = "LEBAI_DISPLAY_GRAPH_CASE_INDEX"
DISPLAY_CASES = [
    (
        launch_name,
        namespace,
        1 + (os.getpid() + case_index) % 230,
        (
            "gripper.rviz"
            if "gripper" in launch_name and "lm3" not in launch_name
            else "view.rviz"
        ),
    )
    for case_index, (launch_name, namespace) in enumerate(
        (
            (launch_name, namespace)
            for launch_name in (
                *DIRECT_DISPLAY_LAUNCHES,
                "standalone_lm3.launch.py",
            )
            for namespace in ("", "test_robot")
        ),
    )
]
SELECTED_CASE_INDEX = os.environ.get(CASE_INDEX_ENV)


def _output_text(output):
    if isinstance(output, bytes):
        return output.decode(errors="replace")
    return output or ""


if SELECTED_CASE_INDEX is None:
    @pytest.mark.hermetic
    @pytest.mark.parametrize(
        "case_index",
        range(len(DISPLAY_CASES)),
        ids=[
            f"{launch_name}-{namespace or 'root'}"
            for (
                launch_name,
                namespace,
                _domain_id,
                _rviz_config_name,
            ) in DISPLAY_CASES
        ],
    )
    def test_display_launch_graph_case(case_index, xvfb):
        assert xvfb is not None
        environment = os.environ.copy()
        environment[CASE_INDEX_ENV] = str(case_index)
        environment["RMW_IMPLEMENTATION"] = "rmw_cyclonedds_cpp"
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "pytest",
                os.path.abspath(__file__),
                "-q",
                "--no-xvfb",
            ],
            start_new_session=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=environment,
            text=True,
        )

        try:
            output, _ = process.communicate(timeout=90)
        except subprocess.TimeoutExpired as timeout_error:
            captured_output = [_output_text(timeout_error.output)]
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGTERM)
            try:
                output, _ = process.communicate(timeout=5)
            except subprocess.TimeoutExpired as terminate_error:
                captured_output.append(_output_text(terminate_error.output))
                with suppress(ProcessLookupError):
                    os.killpg(process.pid, signal.SIGKILL)
                output, _ = process.communicate()
            captured_output.append(_output_text(output))
            assert False, (
                "display graph child timed out after 90 seconds:\n"
                + "".join(captured_output)
            )

        assert process.returncode == 0, _output_text(output)
else:
    case_index = int(SELECTED_CASE_INDEX)
    if not 0 <= case_index < len(DISPLAY_CASES):
        raise RuntimeError(f"invalid {CASE_INDEX_ENV}: {case_index}")

    @pytest.mark.hermetic
    @pytest.mark.launch_test
    @launch_testing.parametrize(
        "launch_name, namespace, domain_id, rviz_config_name",
        [DISPLAY_CASES[case_index]],
    )
    def generate_test_description(
        launch_name,
        namespace,
        domain_id,
        rviz_config_name,
    ):
        del rviz_config_name
        launch_arguments = {"namespace": namespace}
        if launch_name in DIRECT_DISPLAY_LAUNCHES:
            launch_arguments["joint_state_publisher"] = "false"

        display = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(SUPPORT_SHARE / "launch" / launch_name)
            ),
            launch_arguments=launch_arguments.items(),
        )
        return LaunchDescription([
            SetEnvironmentVariable("ROS_DOMAIN_ID", str(domain_id)),
            display,
            launch_testing.actions.ReadyToTest(),
        ])


@pytest.mark.hermetic
class TestDisplayLaunchGraph(unittest.TestCase):
    __test__ = SELECTED_CASE_INDEX is not None

    def setUp(self):
        self.context = None
        self.node = None
        self.pump = None
        self.subscription = None

    def _start_ros(self, domain_id):
        try:
            self.context = rclpy.Context()
            rclpy.init(
                context=self.context,
                domain_id=int(domain_id),
            )
            self.node = rclpy.create_node(
                "display_launch_graph_probe",
                context=self.context,
            )
            self.pump = MessagePump(self.node, context=self.context)
            self.pump.start()
        except BaseException:
            self._cleanup_ros()
            raise

    def tearDown(self):
        self._cleanup_ros()

    def test_relative_description_reaches_real_rviz(
        self,
        launch_name,
        namespace,
        domain_id,
        rviz_config_name,
    ):
        del launch_name
        self._start_ros(domain_id)
        self.assertTrue(pytest_xvfb.xvfb_available())
        self.assertTrue(os.environ.get("DISPLAY"))

        topic_name = _resolved_topic(namespace, "robot_description")
        config_topic = _robot_model_topic(rviz_config_name)
        self.assertEqual(config_topic, "robot_description")
        self.assertEqual(
            _resolved_topic(namespace, config_topic),
            topic_name,
        )

        messages = []
        qos = QoSProfile(
            depth=1,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            reliability=ReliabilityPolicy.RELIABLE,
        )
        self.subscription = self.node.create_subscription(
            String,
            topic_name,
            messages.append,
            qos,
        )
        expected_namespace = _resolved_namespace(namespace)
        self._wait_until(
            lambda: self._graph_state(
                messages,
                topic_name,
                expected_namespace,
            )["ready"],
            timeout_sec=30.0,
            description=(
                f"nonempty transient-local description and RViz subscription "
                f"on {topic_name}"
            ),
            diagnostics=lambda: self._graph_state(
                messages,
                topic_name,
                expected_namespace,
            ),
        )

        self.assertTrue(messages[-1].data.strip())

    def _graph_state(self, messages, topic_name, namespace):
        publishers = self.node.get_publishers_info_by_topic(topic_name)
        subscriptions = self.node.get_subscriptions_info_by_topic(topic_name)
        description_ready = any(
            endpoint.node_name == "robot_state_publisher"
            and endpoint.node_namespace == namespace
            and endpoint.topic_type == "std_msgs/msg/String"
            and endpoint.qos_profile.durability
            == DurabilityPolicy.TRANSIENT_LOCAL
            for endpoint in publishers
        )
        rviz_ready = any(
            endpoint.node_name == "rviz2"
            and endpoint.node_namespace == namespace
            and endpoint.topic_type == "std_msgs/msg/String"
            and endpoint.qos_profile.durability
            == DurabilityPolicy.TRANSIENT_LOCAL
            for endpoint in subscriptions
        )
        message_ready = any(message.data.strip() for message in messages)
        return {
            "ready": message_ready and description_ready and rviz_ready,
            "message_ready": message_ready,
            "description_publisher_ready": description_ready,
            "rviz_subscription_ready": rviz_ready,
            "publishers": _endpoint_summaries(publishers),
            "subscriptions": _endpoint_summaries(subscriptions),
        }

    def _wait_until(
        self,
        predicate,
        timeout_sec,
        description,
        diagnostics,
    ):
        deadline = time.monotonic() + timeout_sec
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.05)
        self.fail(
            f"timed out waiting for {description}; "
            f"last graph state: {diagnostics()}"
        )

    def _cleanup_ros(self):
        if self.pump is not None:
            with suppress(Exception):
                self.pump.stop()
            self.pump = None
        if self.node is not None:
            if self.subscription is not None:
                with suppress(Exception):
                    self.node.destroy_subscription(self.subscription)
                self.subscription = None
            with suppress(Exception):
                self.node.destroy_node()
            self.node = None
        if self.context is not None and self.context.ok():
            with suppress(Exception):
                self.context.shutdown()
        self.context = None


def _robot_model_topic(rviz_config_name):
    config = yaml.safe_load(
        (SUPPORT_SHARE / "rviz" / rviz_config_name).read_text()
    )
    displays = config["Visualization Manager"]["Displays"]
    robot_models = [
        display
        for display in displays
        if display.get("Class") == "rviz_default_plugins/RobotModel"
    ]
    assert len(robot_models) == 1
    return robot_models[0]["Description Topic"]["Value"]


def _resolved_namespace(namespace):
    return f"/{namespace.strip('/')}" if namespace.strip("/") else "/"


def _resolved_topic(namespace, relative_topic):
    prefix = namespace.strip("/")
    return f"/{prefix}/{relative_topic}" if prefix else f"/{relative_topic}"


def _endpoint_summaries(endpoints):
    return [
        {
            "node": f"{endpoint.node_namespace}/{endpoint.node_name}",
            "type": endpoint.topic_type,
            "durability": str(endpoint.qos_profile.durability),
        }
        for endpoint in endpoints
    ]
