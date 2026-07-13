#!/usr/bin/env python3

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

import rclpy
from geometry_msgs.msg import Point, Pose, Quaternion
from rclpy.node import Node
from lebai_interfaces.msg import MotionParams, MotionTarget
from lebai_interfaces.srv import MoveJoint
from lebai_interfaces.srv import MoveLinear

from lebai_tutorials_common import call_service


class MoveExample(Node):
    def __init__(self):
        super().__init__('move_example')

    def send_move_joint(self):
        srv = self.create_client(MoveJoint, '/lebai/motion/movej')
        while not srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "motion/movej" not available, waiting...')
        req = MoveJoint.Request()
        req.target = MotionTarget(
            is_joint_pose=True,
            joint_positions=[-0.516, -1.384, 0.932, -1.084, -0.833, -0.792],
        )
        req.params = MotionParams(acceleration=1.0, velocity=0.1)
        return call_service(self, srv, req, 'motion/movej')

    def send_move_linear(self):
        srv = self.create_client(MoveLinear, '/lebai/motion/movel')
        while not srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "motion/movel" not available, waiting...')
        req = MoveLinear.Request()
        req.target.is_joint_pose = False
        req.target.cartesian_pose = Pose(
            position=Point(x=0.022, y=0.473, z=0.431),
            orientation=Quaternion(
                x=0.4452199054419614,
                y=-0.023637240544570032,
                z=-0.1897987542851597,
                w=0.8747553655334106,
            ),
        )
        req.params = MotionParams(acceleration=1.0, velocity=0.1)
        return call_service(self, srv, req, 'motion/movel')


def run():
    move_example = MoveExample()
    try:
        outcomes = (
            move_example.send_move_joint(),
            move_example.send_move_linear(),
        )
        return all(outcomes)
    finally:
        move_example.destroy_node()


def main():
    rclpy.init()
    try:
        succeeded = run()
    finally:
        rclpy.shutdown()
    raise SystemExit(0 if succeeded else 1)


if __name__ == '__main__':
    main()
