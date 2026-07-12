import os
import time
import unittest

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_testing
from launch_testing_ros import MessagePump
import pytest
from rcl_interfaces.msg import ParameterType
from rcl_interfaces.srv import GetParameters
import rclpy


ARM_JOINT_NAMES = [f"joint_{index}" for index in range(1, 7)]
EXPECTED_ARM_LIMIT = {
    "has_velocity_limits": True,
    "max_velocity": 3.0,
    "has_acceleration_limits": True,
    "max_acceleration": 6.0,
}
EXPECTED_GRIPPER_LIMIT = {
    "has_velocity_limits": True,
    "max_velocity": 1.0,
    "has_acceleration_limits": False,
    "max_acceleration": 1.0,
}
LIVE_ROBOT_IP = os.environ.get("LEBAI_TEST_ROBOT_IP")
LIVE_CASES = [
    ("lm3.launch.py", "true"),
    ("lm3.launch.py", "false"),
    ("lm3_l1.launch.py", "true"),
    ("lm3_l1.launch.py", "false"),
]


@pytest.mark.integration
@pytest.mark.skipif(
    not LIVE_ROBOT_IP,
    reason="LEBAI_TEST_ROBOT_IP is not set",
)
@pytest.mark.launch_test
@launch_testing.parametrize("launch_name, has_gripper", LIVE_CASES)
def generate_test_description(launch_name, has_gripper):
    launch_path = (
        get_package_share_path("lebai_lm3_moveit_config")
        / "launch"
        / launch_name
    )
    public_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(launch_path)),
        launch_arguments={
            "robot_ip": LIVE_ROBOT_IP,
            "simulator": "true",
            "has_gripper": has_gripper,
        }.items(),
    )
    return LaunchDescription([
        public_launch,
        launch_testing.actions.ReadyToTest(),
    ])


@pytest.mark.integration
@pytest.mark.skipif(
    not LIVE_ROBOT_IP,
    reason="LEBAI_TEST_ROBOT_IP is not set",
)
class TestLiveMoveGroupPlanningLimits(unittest.TestCase):
    def setUp(self):
        rclpy.init()
        self.node = rclpy.create_node("lebai_planning_limits_probe")
        self.pump = MessagePump(self.node)
        self.pump.start()

    def tearDown(self):
        self.pump.stop()
        self.node.destroy_node()
        rclpy.shutdown()

    def test_effective_parameters(self, launch_name, has_gripper):
        del launch_name
        expected = {
            "robot_description_planning.default_velocity_scaling_factor": 0.2,
            "robot_description_planning.default_acceleration_scaling_factor": 0.2,
        }
        for joint_name in ARM_JOINT_NAMES:
            expected.update(_flatten_joint_limit(joint_name, EXPECTED_ARM_LIMIT))
        if has_gripper == "true":
            expected.update(
                _flatten_joint_limit("gripper_r_joint1", EXPECTED_GRIPPER_LIMIT)
            )

        client = self.node.create_client(
            GetParameters,
            "/move_group/get_parameters",
        )
        self.assertTrue(client.wait_for_service(timeout_sec=30.0))
        request = GetParameters.Request(names=list(expected))
        future = client.call_async(request)
        deadline = time.monotonic() + 30.0
        while not future.done() and time.monotonic() < deadline:
            time.sleep(0.05)

        self.assertTrue(future.done(), "move_group parameter request timed out")
        actual = {
            name: _parameter_value(value)
            for name, value in zip(request.names, future.result().values)
        }
        for name, expected_value in expected.items():
            if isinstance(expected_value, float):
                self.assertAlmostEqual(actual[name], expected_value)
            else:
                self.assertEqual(actual[name], expected_value)
        self.node.destroy_client(client)


def _flatten_joint_limit(joint_name, values):
    prefix = f"robot_description_planning.joint_limits.{joint_name}."
    return {prefix + key: value for key, value in values.items()}


def _parameter_value(value):
    if value.type == ParameterType.PARAMETER_BOOL:
        return value.bool_value
    if value.type == ParameterType.PARAMETER_DOUBLE:
        return value.double_value
    if value.type == ParameterType.PARAMETER_INTEGER:
        return value.integer_value
    raise AssertionError(f"unexpected parameter type: {value.type}")
