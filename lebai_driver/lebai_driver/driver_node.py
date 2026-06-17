import rclpy
from rclpy.node import Node

from lebai_driver.connection import RobotConnection
from lebai_driver.parameters import DEFAULT_PARAMETERS
from lebai_driver.claw_services import register_claw_services
from lebai_driver.io_services import register_io_services
from lebai_driver.led_signal_services import register_led_signal_services
from lebai_driver.motion_services import register_motion_services
from lebai_driver.resource_services import register_resource_services
from lebai_driver.start_stop_services import register_start_stop_services
from lebai_driver.status import register_status_publishers


class LebaiDriverNode(Node):
    def __init__(self, robot_factory=None):
        super().__init__('lebai_driver')

        for name, value in DEFAULT_PARAMETERS.items():
            self.declare_parameter(name, value)

        robot_ip = self.get_parameter('robot_ip').value
        simulator = self.get_parameter('simulator').value
        self.connection = RobotConnection(
            robot_ip=robot_ip,
            simulator=simulator,
            robot_factory=robot_factory,
        )

        register_status_publishers(self, self.connection)
        register_start_stop_services(self, self.connection)
        register_motion_services(self, self.connection)
        register_io_services(self, self.connection)
        register_led_signal_services(self, self.connection)
        register_resource_services(self, self.connection)
        register_claw_services(self, self.connection)


def main(args=None):
    rclpy.init(args=args)
    node = LebaiDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
