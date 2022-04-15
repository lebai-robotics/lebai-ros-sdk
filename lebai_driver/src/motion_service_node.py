#!/usr/bin/python3
import rospy
from lebai_driver.motion_service.motion_service_interface import MotionServiceInterface

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
