#!/usr/bin/python3
import unittest
import rostest
import sys
import math
from system_service_proxy import SystemServiceProxy
from robot_state_proxy  import RobotStateProxy
from motion_service_proxy import MotionServiceProxy
import rospy
# from industrial_msgs.msg import RobotStatus

class TestAll(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)        
        self.system_service_proxy_ = SystemServiceProxy()
        self.robot_state_proxy_ = RobotStateProxy()
        self.motion_service_proxy_ = MotionServiceProxy()
    
    def almost_equal(self, value_1, value_2, accuracy = 10**-3):
        return abs(value_1 - value_2) < accuracy

    def array_almost_equal(self, array_1, array_2, accuracy = 10**-3):
        for i in range(len(array_1)):
            # rospy.logerr("data %s %s"%(array_1[i], array_2[i]))
            if not self.almost_equal(array_1[i], array_2[i], accuracy):
                return False
        return True       

    def test_motion(self):
        self.assertTrue(self.system_service_proxy_.enable())
        rate = rospy.Rate(1.0)
        rate.sleep()
        self.assertTrue(self.motion_service_proxy_.move_joint([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
        self.assertTrue(self.motion_service_proxy_.move_joint([0, -1.2, math.pi/6, 0, math.pi/4, 0]))
        rate.sleep()
        while self.robot_state_proxy_.robot_status_.in_motion.val:
            rate.sleep()
        
        # rospy.logerr("position %s %s %s %s %s %s"%(self.robot_state_proxy_.joint_states_.position[0],
        # self.robot_state_proxy_.joint_states_.position[1],
        # self.robot_state_proxy_.joint_states_.position[2],
        # self.robot_state_proxy_.joint_states_.position[3],
        # self.robot_state_proxy_.joint_states_.position[4],
        # self.robot_state_proxy_.joint_states_.position[5]))
        self.assertTrue(self.array_almost_equal([0, -1.2, math.pi/6, 0, math.pi/4, 0], self.robot_state_proxy_.joint_states_.position, 0.01))
        self.assertTrue(self.motion_service_proxy_.move_line())


    def test_system(self):
        self.assertTrue(self.system_service_proxy_.enable())
        rate = rospy.Rate(1.0)
        rate.sleep()
        self.assertTrue(self.robot_state_proxy_.robot_status_.drives_powered.val)
        self.assertTrue(self.system_service_proxy_.disable())
        rate.sleep()
        self.assertFalse(self.robot_state_proxy_.robot_status_.drives_powered.val)
        self.assertTrue(self.system_service_proxy_.emergency_stop())
        rate.sleep()
        rate.sleep()
        rate.sleep()
        self.assertTrue(self.robot_state_proxy_.robot_status_.e_stopped.val)
        self.assertTrue(self.system_service_proxy_.power_on())
        rate.sleep()
        self.assertFalse(self.robot_state_proxy_.robot_status_.e_stopped.val)
        self.assertTrue(self.robot_state_proxy_.robot_status_.drives_powered.val)
        self.assertFalse(self.robot_state_proxy_.robot_status_.in_motion.val)
        self.assertTrue(self.robot_state_proxy_.robot_status_.motion_possible.val)


PKG = 'lebai_driver'
NAME = 'lebai_driver_test'

if __name__ == '__main__':
    rospy.init_node('test_lebai_driver', anonymous=True)
    rostest.rosrun(PKG, NAME, TestAll, sys.argv)
