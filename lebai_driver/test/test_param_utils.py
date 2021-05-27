#!/usr/bin/python3
import unittest
import rostest
import sys
import os
import rospy
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir+"/src")
import param_utils


class TestAll(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)       

    def test_get_joint_names_case1(self): 
        joint_names = param_utils.get_joint_names("controller_joint_names", "robot_description")
        # rospy.logerr(joint_names)
        self.assertEqual(["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"],joint_names)

    def test_get_joint_names_case2(self): 
        joint_names = param_utils.get_joint_names("xxx", "robot_description")
        # rospy.logerr(joint_names)
        self.assertEqual(['robot1_joint_1', 'robot1_joint_2', 'robot1_joint_3', 'robot1_joint_4', 
        'robot1_joint_5', 'robot1_joint_6', 'robot2_joint_1', 'robot2_joint_2', 'robot2_joint_3', 
        'robot2_joint_4', 'robot2_joint_5', 'robot2_joint_6'],joint_names)

PKG = 'lebai_driver'
NAME = 'param_utils_test'

if __name__ == '__main__':
    rospy.init_node('test_param_utils', anonymous=True)
    rostest.rosrun(PKG, NAME, TestAll, sys.argv)
