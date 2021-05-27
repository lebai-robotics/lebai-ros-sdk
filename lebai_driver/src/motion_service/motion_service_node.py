#!/usr/bin/python3
# license removed for brevity
import rospy
import os, sys
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)
from motion_service_interface import MotionServiceInterface

# from std_srvs.srv import Empty, EmptyResponse, EmptyRequest

def run():    
    rate = rospy.Rate(10) # 10hz
    if not rospy.has_param('robot_ip_address'):
        rospy.logerr('robot_ip_address is not assigned')
        return
    robot_ip = rospy.get_param('robot_ip_address')
    msi = MotionServiceInterface(robot_ip)

    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == '__main__':

    
    
    rospy.init_node('motion_service', anonymous=True)
    try:
        run()
    except rospy.ROSInterruptException:
        pass
