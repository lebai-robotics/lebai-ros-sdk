from lebai_interfaces.msg import GripperStatus
from rclpy.node import Node
from lebai import LebaiRobot



class GripperStateHandler:
    def __init__(self, node: Node, lebai_robot: LebaiRobot):
        self.node_ = node
        self.lebai_robot_ = lebai_robot
        self.gripper_state_pub_ = self.node_.create_publisher(GripperStatus, 'gripper_status', 1)
        self.timer_ = self.node_.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        gripper_status = GripperStatus()
        gripper_status.force = float(self.lebai_robot_.get_claw_aio(str('force')))
        gripper_status.position = float(self.lebai_robot_.get_claw_aio(str()))
        self.gripper_state_pub_.publish(gripper_status)
