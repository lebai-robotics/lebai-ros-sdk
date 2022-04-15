from logging import exception
from urdf_parser_py.urdf import URDF
from urdf_parser_py.urdf import Joint
import rospy
import lebai_driver.urdf_helper as urdf_helper

def get_joint_names(joints_name_param, robot_description_param):
    if rospy.has_param(joints_name_param):
        # rospy.logerr("joints_name_param %s"%(joints_name_param))
        joint_names = rospy.get_param(joints_name_param)
        # rospy.logerr("joint_names %s"%(joint_names))
        return joint_names
    # rospy.logerr("robot_description_param %s"%(robot_description_param))
    robot_description = rospy.get_param(robot_description_param)
    # rospy.logerr("robot_description %s"%(robot_description))    
    try:
        urdf_robot = URDF.from_xml_string(robot_description)
        return urdf_helper.find_chain_joints_name(urdf_robot)
    except Exception:
        pass


