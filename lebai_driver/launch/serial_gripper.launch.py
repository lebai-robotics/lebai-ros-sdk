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
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='lebai'),
        DeclareLaunchArgument('port_name', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('gripper_state_publish_rate', default_value='10.0'),
        Node(
            package='lebai_driver',
            executable='serial_gripper',
            name='lebai_serial_gripper',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[{
                'port_name': LaunchConfiguration('port_name'),
                'gripper_state_publish_rate': LaunchConfiguration(
                    'gripper_state_publish_rate',
                ),
            }],
        ),
    ])
