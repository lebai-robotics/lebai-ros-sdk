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

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Namespace for the standalone display nodes",
    )
    has_gripper_arg = DeclareLaunchArgument(
        "has_gripper",
        default_value="false",
        choices=["true", "false"],
        description="Mount gripper on the end",
    )
    namespace = LaunchConfiguration("namespace")
    has_gripper = LaunchConfiguration("has_gripper")
    launch_dir = PathJoinSubstitution([
        FindPackageShare("lebai_lm3_support"),
        "launch",
    ])

    display = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            launch_dir,
            "/display_lm3.launch.py",
        ]),
        launch_arguments={
            "joint_state_publisher": "true",
            "namespace": namespace,
        }.items(),
        condition=UnlessCondition(has_gripper),
    )
    display_with_gripper = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            launch_dir,
            "/display_lm3_with_gripper.launch.py",
        ]),
        launch_arguments={
            "joint_state_publisher": "true",
            "namespace": namespace,
        }.items(),
        condition=IfCondition(has_gripper),
    )

    return LaunchDescription([
        namespace_arg,
        has_gripper_arg,
        display,
        display_with_gripper,
    ])
