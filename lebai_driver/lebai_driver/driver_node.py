import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from lebai_driver.connection import RobotConnection
from lebai_driver.parameters import DEFAULT_PARAMETERS
from lebai_driver.claw_services import register_claw_services
from lebai_driver.gripper_action import register_gripper_action
from lebai_driver.io_services import register_io_services
from lebai_driver.led_signal_services import register_led_signal_services
from lebai_driver.motion_services import register_motion_services
from lebai_driver.resource_services import register_resource_services
from lebai_driver.sdk_gate import StatusServiceGate
from lebai_driver.start_stop_services import register_start_stop_services
from lebai_driver.status import register_status_publishers
from lebai_driver.trajectory_action import register_trajectory_action


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

        self.service_callback_group = MutuallyExclusiveCallbackGroup()
        self.service_sdk_gate = StatusServiceGate()

        register_status_publishers(
            self,
            self.connection,
            sdk_gate=self.service_sdk_gate,
        )
        register_start_stop_services(
            self,
            self.connection,
            callback_group=self.service_callback_group,
            sdk_gate=self.service_sdk_gate,
        )
        register_motion_services(
            self,
            self.connection,
            callback_group=self.service_callback_group,
            sdk_gate=self.service_sdk_gate,
        )
        register_io_services(
            self,
            self.connection,
            callback_group=self.service_callback_group,
            sdk_gate=self.service_sdk_gate,
        )
        register_led_signal_services(
            self,
            self.connection,
            callback_group=self.service_callback_group,
            sdk_gate=self.service_sdk_gate,
        )
        register_resource_services(
            self,
            self.connection,
            callback_group=self.service_callback_group,
            sdk_gate=self.service_sdk_gate,
        )
        register_claw_services(
            self,
            self.connection,
            callback_group=self.service_callback_group,
            sdk_gate=self.service_sdk_gate,
        )
        self.trajectory_action = register_trajectory_action(self, self.connection)
        self.gripper_action = register_gripper_action(self, self.connection)


def main(args=None):
    rclpy.init(args=args)
    node = LebaiDriverNode()
    executor = create_executor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


def create_executor():
    return MultiThreadedExecutor()
