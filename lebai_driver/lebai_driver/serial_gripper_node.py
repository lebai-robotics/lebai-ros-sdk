import rclpy
from rclpy.node import Node


class LebaiSerialGripperNode(Node):
    def __init__(self):
        super().__init__('lebai_serial_gripper')


def main(args=None):
    rclpy.init(args=args)
    node = LebaiSerialGripperNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
