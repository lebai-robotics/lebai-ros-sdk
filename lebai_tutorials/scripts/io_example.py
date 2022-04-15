#!/usr/bin/env python3

import rospy
from lebai_msgs.srv import SetAO
from lebai_msgs.srv import SetDO
    
def Run():
    rospy.wait_for_service("/io_service/set_robot_do")
    rospy.wait_for_service("/io_service/set_robot_ao")
    set_do_caller = rospy.ServiceProxy('/io_service/set_robot_do', SetDO)
    set_ao_caller = rospy.ServiceProxy('/io_service/set_robot_ao', SetAO)

    try:
        set_do_caller(7 , 0)
    except rospy.ServiceException as e:
        rospy.logerr("Service 'set_robot_do' call failed: %s", e)
    try:
        set_ao_caller(1 , -3.123)
    except rospy.ServiceException as e:
        rospy.logerr("Service call 'set_robot_ao' failed: %s", e)
    return

if __name__ == '__main__':
    try:
        rospy.init_node('io_example', anonymous=True)
        Run()
    except rospy.ROSInterruptException:
        pass
