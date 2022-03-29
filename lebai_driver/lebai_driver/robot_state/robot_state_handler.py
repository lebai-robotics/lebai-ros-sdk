from lebai import RobotState
from lebai_interfaces.msg import RobotStatus, RobotMode
from rclpy.node import Node
from lebai import LebaiRobot




class RobotStateHandler:
    def __init__(self, node: Node, lebai_robot: LebaiRobot):
        self.node_ = node
        self.lebai_robot_ = lebai_robot
        self.robot_status_pub_ = self.node_.create_publisher(RobotStatus, 'robot_status', 1)
        self.timer_ = self.node_.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        rc_robot_mode = self.lebai_robot_.get_robot_mode()
        robot_status = self.get_robot_status(rc_robot_mode)
        self.robot_status_pub_.publish(robot_status)

    def get_robot_status(self, rc_robot_mode):
        robot_status = RobotStatus()
        robot_status.header.stamp = self.node_.get_clock().now().to_msg()
        if rc_robot_mode == RobotState.RUNNING:
            robot_status.motion_possible.val = False
            robot_status.in_motion.val = True
            robot_status.e_stopped.val = False
            robot_status.drives_powered.val = True
        elif rc_robot_mode == RobotState.IDLE:
            robot_status.motion_possible.val = True
            robot_status.in_motion.val = False
            robot_status.e_stopped.val = False
            robot_status.drives_powered.val = True
        elif rc_robot_mode == RobotState.TEACHING:
            robot_status.motion_possible.val = False
            robot_status.in_motion.val = False
            robot_status.e_stopped.val = False
            robot_status.drives_powered.val = True
        elif rc_robot_mode == RobotState.ESTOP:
            robot_status.motion_possible.val = False
            robot_status.in_motion.val = False
            robot_status.e_stopped.val = True
            robot_status.drives_powered.val = False
        else:
            robot_status.motion_possible.val = False
            robot_status.in_motion.val = False
            robot_status.e_stopped.val = False
            robot_status.drives_powered.val = False
        robot_status.mode.val = RobotMode.UNKNOWN
        return robot_status

