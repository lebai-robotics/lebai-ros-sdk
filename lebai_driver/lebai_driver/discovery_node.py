import rclpy
from rclpy.node import Node


class LebaiDiscoveryNode(Node):
    def __init__(self):
        super().__init__('lebai_discovery')


def main(args=None):
    rclpy.init(args=args)
    node = LebaiDiscoveryNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
