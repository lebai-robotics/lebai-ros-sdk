#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from lebai_interfaces.srv import MoveJoint
from lebai_interfaces.srv import MoveLine
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion


class MoveExample(Node):
    def __init__(self):
        super().__init__('move_example')

    def SendMoveJoint(self):
        move_joint_srv = self.create_client(
            MoveJoint, '/motion_service/move_joint')
        while not move_joint_srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "move_joint" not available, waiting...')
        req = MoveJoint.Request()
        req.is_joint_pose = True
        req.joint_pose = [-0.516, -1.384, 0.932, -1.084, -0.833, -0.792]
        req.common.vel = 0.1
        req.common.acc = 1.0
        req.common.radius = 0.0
        future = move_joint_srv.call_async(req)
        while rclpy.ok():
            rclpy.spin_once(self)
            if future.done():
                try:
                    future.result()
                except Exception as e:
                    self.get_logger().info(
                        'Service "move_joint" call failed %r' % (e,))
                else:
                    self.get_logger().info(
                        'Service "move_joint" call succeed.')
                break

    def SendMoveLine(self):
        move_line_srv = self.create_client(
            MoveLine, '/motion_service/move_line')
        while not move_line_srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "move_line" not available, waiting...')
        req = MoveLine.Request()
        req.is_joint_pose = False
        req.cartesian_pose.position.x = 0.022
        req.cartesian_pose.position.y = 0.473
        req.cartesian_pose.position.z = 0.431
        req.cartesian_pose.orientation.x = 0.918
        req.cartesian_pose.orientation.y = 0.128
        req.cartesian_pose.orientation.z = -0.364
        req.cartesian_pose.orientation.w = -0.091
        req.common.vel = 0.1
        req.common.acc = 1.0
        req.common.radius = 0.0
        future = move_line_srv.call_async(req)
        while rclpy.ok():
            rclpy.spin_once(self)
            if future.done():
                try:
                    future.result()
                except Exception as e:
                    self.get_logger().info(
                        'Service "move_line" call failed %r' % (e,))
                else:
                    self.get_logger().info(
                        'Service "move_line" call succeed.')
                break


def Run():
    move_example = MoveExample()
    move_example.SendMoveJoint()
    move_example.SendMoveLine()
    # SendMoveCircle()
    return


def main():
    rclpy.init()
    Run()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
