from lebai import LebaiRobot
import rospy
import os, sys
from lebai_driver.motion_service.tp_trajectory_handler import TPTrajectoryHandler
from lebai_driver.motion_service.tp_stream_trajectory_handler import TPStreamTrajectoryHandler
# from urdf_helper import find_chain_joints_name
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import lebai_driver.param_utils as param_utils
from urdf_parser_py.urdf import URDF


class MotionServiceInterface:
    def __init__(self, ip):
        self.lebai_robot_ = LebaiRobot(ip, False)
        if not rospy.has_param('controller_joint_names'):
            rospy.loginfo('controller_joint_names is not assigned')
        self.joints_name_ = param_utils.get_joint_names("controller_joint_names", "/robot_description")
        self.tp_traj_handler_ = TPTrajectoryHandler(self.lebai_robot_)
        self.tp_stream_traj_handler_ = TPStreamTrajectoryHandler(self.lebai_robot_, self.joints_name_)

    def __del__(self):
        self.tp_traj_handler_ = None
        self.tp_stream_traj_handler_ = None


