from lebai import LebaiRobot
import rospy
import os, sys
from tp_trajectory_handler import TPTrajectoryHandler
from tp_stream_trajectory_handler import TPStreamTrajectoryHandler
# from urdf_helper import find_chain_joints_name
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import urdf_helper
from urdf_parser_py.urdf import URDF


class MotionServiceInterface:
    def __init__(self, ip):
        self.lebai_robot_ = LebaiRobot(ip, False)
        self.robot_description_param_ = rospy.get_param("/robot_description")
        self.urdf_robot_ = URDF.from_xml_string(self.robot_description_param_)
        self.joints_name_ = urdf_helper.find_chain_joints_name(self.urdf_robot_)
        self.tp_traj_handler_ = TPTrajectoryHandler(self.lebai_robot_)
        self.tp_stream_traj_handler_ = TPStreamTrajectoryHandler(self.lebai_robot_, self.joints_name_)
        


