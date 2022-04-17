#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from lebai_interfaces.srv import SetDO
from lebai_interfaces.srv import SetAO


class IOExample(Node):
    def __init__(self):
        super().__init__('io_example')

    def SetDO(self):
        srv = self.create_client(
            SetDO, '/io_service/set_robot_do')
        while not srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "set_robot_do" not available, waiting...')
        req = SetDO.Request()
        req.pin = 0
        req.value = True
        future = srv.call_async(req)
        while rclpy.ok():
            rclpy.spin_once(self)
            if future.done():
                try:
                    future.result()
                except Exception as e:
                    self.get_logger().info(
                        'Service "set_robot_do" call failed %r' % (e,))
                else:
                    self.get_logger().info(
                        'Service "set_robot_do" call succeed.')
                break

    def SetAO(self):
        srv = self.create_client(
            SetAO, '/io_service/set_robot_ao')
        while not srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "set_robot_ao" not available, waiting...')
        req = SetAO.Request()
        req.pin = 0
        req.value = 3.0
        future = srv.call_async(req)
        while rclpy.ok():
            rclpy.spin_once(self)
            if future.done():
                try:
                    future.result()
                except Exception as e:
                    self.get_logger().info(
                        'Service "set_robot_ao" call failed %r' % (e,))
                else:
                    self.get_logger().info(
                        'Service "set_robot_ao" call succeed.')
                break


def Run():
    io_example = IOExample()
    io_example.SetDO()
    io_example.SetAO()
    # SendMoveCircle()
    return


def main():
    rclpy.init()
    Run()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
