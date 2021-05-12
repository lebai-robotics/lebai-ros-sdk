#!/usr/bin/python3
import unittest
import rostest
import sys
import math
from system_service_proxy import SystemServiceProxy
from robot_state_proxy  import RobotStateProxy
from motion_service_proxy import MotionServiceProxy
import rospy
from industrial_msgs.msg import RobotStatus

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
        self.assertTrue(self.array_almost_equal([0, -1.2, math.pi/6, 0, math.pi/4, 0], self.robot_state_proxy_.joint_states_.position))
        self.assertTrue(self.motion_service_proxy_.move_line())
        # self.assertTrue(self.motion_service_proxy_.move_joint([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
        # self.assertTrue([0.1, 0.2], [0.0999, 0.2001], 3)
    # def check_system_service_exist(self):
    #     try:
    #         rospy.wait_for_service('/system_service/enable', 3.0)
    #     except rospy.ROSException:
    #         self.fail("Service /system_service/enable doesn't exists!")

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
        self.assertTrue(self.robot_state_proxy_.robot_status_.e_stopped.val)
        self.assertTrue(self.system_service_proxy_.power_on())
        rate.sleep()
        self.assertFalse(self.robot_state_proxy_.robot_status_.e_stopped.val)
        self.assertTrue(self.robot_state_proxy_.robot_status_.drives_powered.val)
        self.assertFalse(self.robot_state_proxy_.robot_status_.in_motion.val)
        self.assertTrue(self.robot_state_proxy_.robot_status_.motion_possible.val)



    # def test_split(self):
    #     s = 'hello world'
        # self.assertEqual(s.split(), ['hello', 'world'])
        # # check that s.split fails when the separator is not a string
        # with self.assertRaises(TypeError):
        #     s.split(2)


PKG = 'lebai_driver'
NAME = 'lebai_driver_test'

if __name__ == '__main__':
    rospy.init_node('test_lebai_driver', anonymous=True)
    rostest.rosrun(PKG, NAME, TestAll, sys.argv)
