#!/usr/bin/env python2

import rospy
from lebai_msgs.srv import SetAO
from lebai_msgs.srv import SetDO
from lebai_msgs.msg import ExecuteMode
    
def Run():
    rospy.wait_for_service("/io_service/set_robot_do")
    rospy.wait_for_service("/io_service/set_robot_ao")
    set_do_caller = rospy.ServiceProxy('/io_service/set_robot_do', SetDO)
    set_ao_caller = rospy.ServiceProxy('/io_service/set_robot_ao', SetAO)

    exeucte_mode = ExecuteMode()
    exeucte_mode.data = ExecuteMode.EXECUTE_MODE_IMMED
    try:
        set_do_caller(7 , 0, exeucte_mode)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)   
    try:
        set_ao_caller(1 , -3.123, exeucte_mode)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)   
    return

if __name__ == '__main__':
    try:
        rospy.init_node('io_example', anonymous=True)
        Run()
    except rospy.ROSInterruptException:
        pass