#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from lebai_interfaces.srv import SetAnalogOutput, SetDigitalOutput

from lebai_tutorials_common import call_service


class IOExample(Node):
    def __init__(self):
        super().__init__('io_example')

    def set_do(self):
        srv = self.create_client(SetDigitalOutput, '/lebai/io/set_do')
        while not srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "io/set_do" not available, waiting...')
        req = SetDigitalOutput.Request()
        req.device = 'robot'
        req.pin = 0
        req.value = True
        return call_service(self, srv, req, 'io/set_do')

    def set_ao(self):
        srv = self.create_client(SetAnalogOutput, '/lebai/io/set_ao')
        while not srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "io/set_ao" not available, waiting...')
        req = SetAnalogOutput.Request()
        req.device = 'robot'
        req.pin = 0
        req.value = 3.0
        return call_service(self, srv, req, 'io/set_ao')


def run():
    io_example = IOExample()
    try:
        outcomes = (
            io_example.set_do(),
            io_example.set_ao(),
        )
        return all(outcomes)
    finally:
        io_example.destroy_node()


def main():
    rclpy.init()
    try:
        succeeded = run()
    finally:
        rclpy.shutdown()
    raise SystemExit(0 if succeeded else 1)


if __name__ == '__main__':
    main()
