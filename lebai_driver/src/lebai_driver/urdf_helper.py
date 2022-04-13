import roslib
#  roslib.load_manifest('urdfdom_py')
# import urdfdom_py

from urdf_parser_py.urdf import URDF
from urdf_parser_py.urdf import Joint

def find_chain_joints_name(robot):
    joints_name = list()
    for joint in robot.joints:
        if joint.type != 'fixed':
            joints_name.append(joint.name)
    # print(joints_name)
    return joints_name
