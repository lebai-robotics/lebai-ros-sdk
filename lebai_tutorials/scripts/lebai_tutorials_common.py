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

import math

import rclpy


GRIPPER_MAX_JOINT_POSITION = math.pi / 3.0
GRIPPER_JOINT_NAME = "gripper_r_joint1"
MANIPULATOR_JOINT_NAMES = (
    "joint_1",
    "joint_2",
    "joint_3",
    "joint_4",
    "joint_5",
    "joint_6",
)


def call_service(node, client, request, label):
    future = client.call_async(request)
    while rclpy.ok():
        rclpy.spin_once(node)
        if not future.done():
            continue

        try:
            response = future.result()
        except Exception as exc:
            node.get_logger().error(
                'Service "%s" transport failed: %s' % (label, exc)
            )
            return False

        if not response.result.success:
            node.get_logger().error(
                'Service "%s" failed with code %d: %s'
                % (label, response.result.code, response.result.message)
            )
            return False

        node.get_logger().info('Service "%s" succeeded.' % label)
        return True

    node.get_logger().error('Service "%s" interrupted.' % label)
    return False


def amplitude_to_gripper_joint(amplitude):
    amplitude = float(amplitude)
    if amplitude < 0.0 or amplitude > 100.0:
        raise ValueError("amplitude must be in the range [0, 100]")
    return GRIPPER_MAX_JOINT_POSITION * amplitude / 100.0


def parse_joint_positions(value):
    positions = [float(item.strip()) for item in value.split(",") if item.strip()]
    if len(positions) != len(MANIPULATOR_JOINT_NAMES):
        raise ValueError("expected six comma-separated joint positions")
    return positions
