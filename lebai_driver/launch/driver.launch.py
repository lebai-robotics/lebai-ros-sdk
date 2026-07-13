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
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    parameters = {
        'robot_ip': LaunchConfiguration('robot_ip'),
        'simulator': LaunchConfiguration('simulator'),
        'namespace': LaunchConfiguration('namespace'),
        'joint_state_publish_rate': LaunchConfiguration('joint_state_publish_rate'),
        'robot_state_publish_rate': LaunchConfiguration('robot_state_publish_rate'),
        'joint_motion_publish_rate': LaunchConfiguration('joint_motion_publish_rate'),
        'io_state_publish_rate': LaunchConfiguration('io_state_publish_rate'),
        'gripper_state_publish_rate': LaunchConfiguration('gripper_state_publish_rate'),
        'gripper_joint_name': LaunchConfiguration('gripper_joint_name'),
        'io_state_device': LaunchConfiguration('io_state_device'),
        'io_state_digital_input_count': LaunchConfiguration(
            'io_state_digital_input_count',
        ),
        'io_state_digital_output_count': LaunchConfiguration(
            'io_state_digital_output_count',
        ),
        'io_state_analog_input_count': LaunchConfiguration(
            'io_state_analog_input_count',
        ),
        'io_state_analog_output_count': LaunchConfiguration(
            'io_state_analog_output_count',
        ),
        'io_state_dio_count': LaunchConfiguration('io_state_dio_count'),
    }
    robot_description = ParameterValue(
        Command([
            'xacro ',
            PathJoinSubstitution([
                FindPackageShare('lebai_lm3_support'),
                'urdf',
                LaunchConfiguration('robot_model'),
            ]),
        ]),
        value_type=str,
    )

    return LaunchDescription([
        DeclareLaunchArgument('robot_ip', default_value='127.0.0.1'),
        DeclareLaunchArgument('simulator', default_value='false'),
        DeclareLaunchArgument('namespace', default_value='lebai'),
        DeclareLaunchArgument('publish_robot_description', default_value='true'),
        DeclareLaunchArgument('robot_model', default_value='lm3_with_gripper.xacro'),
        DeclareLaunchArgument('joint_state_publish_rate', default_value='20.0'),
        DeclareLaunchArgument('robot_state_publish_rate', default_value='10.0'),
        DeclareLaunchArgument('joint_motion_publish_rate', default_value='20.0'),
        DeclareLaunchArgument('io_state_publish_rate', default_value='10.0'),
        DeclareLaunchArgument('gripper_state_publish_rate', default_value='10.0'),
        DeclareLaunchArgument('gripper_joint_name', default_value='gripper_r_joint1'),
        DeclareLaunchArgument('io_state_device', default_value='robot'),
        DeclareLaunchArgument('io_state_digital_input_count', default_value='0'),
        DeclareLaunchArgument('io_state_digital_output_count', default_value='0'),
        DeclareLaunchArgument('io_state_analog_input_count', default_value='0'),
        DeclareLaunchArgument('io_state_analog_output_count', default_value='0'),
        DeclareLaunchArgument('io_state_dio_count', default_value='0'),
        Node(
            package='lebai_driver',
            executable='driver',
            name='lebai_driver',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[parameters],
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[{'robot_description': robot_description}],
            remappings=[('joint_states', 'model/joint_states')],
            condition=IfCondition(LaunchConfiguration('publish_robot_description')),
        ),
    ])
