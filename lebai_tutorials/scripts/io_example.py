#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from lebai_interfaces.srv import SetAnalogOutput, SetDigitalOutput


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
        self._call(srv, req, 'io/set_do')

    def set_ao(self):
        srv = self.create_client(SetAnalogOutput, '/lebai/io/set_ao')
        while not srv.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service "io/set_ao" not available, waiting...')
        req = SetAnalogOutput.Request()
        req.device = 'robot'
        req.pin = 0
        req.value = 3.0
        self._call(srv, req, 'io/set_ao')

    def _call(self, srv, req, label):
        future = srv.call_async(req)
        while rclpy.ok():
            rclpy.spin_once(self)
            if future.done():
                try:
                    future.result()
                except Exception as e:
                    self.get_logger().info('Service "%s" failed %r' % (label, e))
                else:
                    self.get_logger().info('Service "%s" succeeded.' % label)
                break


def run():
    io_example = IOExample()
    io_example.set_do()
    io_example.set_ao()
    io_example.destroy_node()
    return


def main():
    rclpy.init()
    run()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
