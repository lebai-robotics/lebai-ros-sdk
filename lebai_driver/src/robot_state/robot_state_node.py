#!/usr/bin/python3
import rospy
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import robot_state_interface

def run():    
    rate = rospy.Rate(10) # 10hz
    if not rospy.has_param('robot_ip_address'):
        rospy.logerr('robot_ip_address is not assigned')
        return
    
    robot_ip = rospy.get_param('robot_ip_address')
    # rospy.logerr("robot_ip %s"%(robot_ip))

    rsi = robot_state_interface.RobotStateInterface(robot_ip)

    while not rospy.is_shutdown():
        rsi.run()
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('robot_state', anonymous=True)
    try:
        run()
    except rospy.ROSInterruptException:
        pass
