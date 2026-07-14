# Copyright 2022-2026 Shanghai Lebai Robotics Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import unittest

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_testing
from launch_testing_ros import MessagePump
from moveit_msgs.srv import GetPlanningScene
import pytest
import rclpy


LIVE_ROBOT_IP = os.environ.get("LEBAI_TEST_ROBOT_IP")
LIVE_CASES = [
    ("lm3.launch.py", "true"),
    ("lm3.launch.py", "false"),
    ("lm3_l1.launch.py", "true"),
    ("lm3_l1.launch.py", "false"),
]
FORBIDDEN_STARTUP_OUTPUT = (
    "Semantic description is not specified for the same robot as the URDF",
    "No root/virtual joint specified in SRDF. Assuming fixed joint",
    "Skipping virtual joint",
)


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
class TestMoveGroupModelStartup(unittest.TestCase):
    def setUp(self):
        self.node = None
        self.pump = None
        self.pump_started = False
        if not rclpy.ok():
            rclpy.init()
        try:
            self.node = rclpy.create_node("lebai_model_startup_probe")
            self.pump = MessagePump(self.node)
            self.pump.start()
            self.pump_started = True
        except BaseException:
            self._cleanup_ros()
            raise

    def tearDown(self):
        self._cleanup_ros()

    def _cleanup_ros(self):
        try:
            if self.pump is not None and self.pump_started:
                self.pump.stop()
                self.pump_started = False
        finally:
            try:
                if self.node is not None:
                    self.node.destroy_node()
                    self.node = None
            finally:
                if rclpy.ok():
                    rclpy.shutdown()

    def test_move_group_model_is_ready_without_semantic_warnings(
        self,
        launch_name,
        has_gripper,
        proc_output,
    ):
        del launch_name, has_gripper
        client = self.node.create_client(
            GetPlanningScene,
            "/get_planning_scene",
        )
        try:
            self.assertTrue(
                client.wait_for_service(timeout_sec=30.0),
                "move_group planning-scene service did not become ready",
            )
            future = client.call_async(GetPlanningScene.Request())
            deadline = time.monotonic() + 30.0
            while not future.done() and time.monotonic() < deadline:
                time.sleep(0.05)

            self.assertTrue(
                future.done(),
                "move_group planning-scene request timed out",
            )
            self.assertIsNotNone(future.result())
        finally:
            self.node.destroy_client(client)

        startup_output = "".join(
            event.text.decode(errors="replace")
            for event in proc_output
        ).lower()
        for warning in FORBIDDEN_STARTUP_OUTPUT:
            self.assertNotIn(warning.lower(), startup_output)
