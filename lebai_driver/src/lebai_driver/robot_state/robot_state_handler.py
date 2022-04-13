from lebai import RobotState
from industrial_msgs.msg import RobotStatus, RobotMode
import rospy



class RobotStateHandler:
    def __init__(self, lebai_robot):
        self.lebai_robot_ = lebai_robot
        self.robot_status_pub_ = rospy.Publisher('robot_status', RobotStatus, queue_size=1)

    def run(self):
        rc_robot_mode = self.lebai_robot_.get_robot_mode()
        robot_status = self.get_robot_status(rc_robot_mode)
        self.robot_status_pub_.publish(robot_status)

    def get_robot_status(self, rc_robot_mode):
        robot_status = RobotStatus()
        robot_status.header.stamp = rospy.Time.now()
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

