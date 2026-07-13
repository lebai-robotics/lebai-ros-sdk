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

DEFAULT_JOINT_NAMES = [
    'joint_1',
    'joint_2',
    'joint_3',
    'joint_4',
    'joint_5',
    'joint_6',
]

DEFAULT_PARAMETERS = {
    'robot_ip': '127.0.0.1',
    'simulator': False,
    'namespace': '',
    'joint_state_publish_rate': 20.0,
    'robot_state_publish_rate': 10.0,
    'joint_motion_publish_rate': 20.0,
    'io_state_publish_rate': 10.0,
    'gripper_state_publish_rate': 10.0,
    'gripper_joint_name': 'gripper_r_joint1',
    'io_state_device': 'robot',
    'io_state_digital_input_count': 0,
    'io_state_digital_output_count': 0,
    'io_state_analog_input_count': 0,
    'io_state_analog_output_count': 0,
    'io_state_dio_count': 0,
}
