from logging import exception
from typing import List
from urdf_parser_py.urdf import URDF
from rclpy.node import Node
from lebai_driver import urdf_helper

def get_joint_names(node: Node, joints_name_param: str, robot_description_param: str):
    if node.has_parameter(joints_name_param):        
        return node.get_parameter(joints_name_param).get_parameter_value().string_array_value
    # rospy.logerr("robot_description_param %s"%(robot_description_param))
    # robot_description = node.get_parameter(robot_description_param).get_parameter_value().string_value
    # # rospy.logerr("robot_description %s"%(robot_description))    
    # try:
    #     urdf_robot = URDF.from_xml_string(robot_description)
    #     return urdf_helper.find_chain_joints_name(urdf_robot)
    # except Exception:
    #     pass


