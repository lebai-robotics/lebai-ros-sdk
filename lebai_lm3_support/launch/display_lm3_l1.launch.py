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

from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    support_path = get_package_share_path("lebai_lm3_support")
    model_path = support_path / "urdf/lm3_l1.xacro"
    rviz_config_path = support_path / "rviz/view.rviz"
    namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Namespace for the standalone display nodes",
    )
    rviz_config_arg = DeclareLaunchArgument(
        "rvizconfig",
        default_value=str(rviz_config_path),
        description="Absolute path to RViz config file",
    )
    joint_state_publisher_arg = DeclareLaunchArgument(
        "joint_state_publisher",
        default_value="true",
        choices=["true", "false"],
        description="Flag to enable joint_state_publisher_gui",
    )
    namespace = LaunchConfiguration("namespace")
    joint_state_publisher = LaunchConfiguration("joint_state_publisher")
    robot_description = ParameterValue(
        Command(["xacro ", str(model_path)]),
        value_type=str,
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        namespace=namespace,
        parameters=[{"robot_description": robot_description}],
        output="screen",
        condition=IfCondition(joint_state_publisher),
    )
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace=namespace,
        parameters=[{"robot_description": robot_description}],
        output="screen",
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        namespace=namespace,
        output="screen",
        arguments=["-d", LaunchConfiguration("rvizconfig")],
    )

    return LaunchDescription([
        namespace_arg,
        joint_state_publisher_arg,
        rviz_config_arg,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node,
    ])
