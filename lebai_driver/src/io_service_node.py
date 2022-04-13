#!/usr/bin/python3
# license removed for brevity
import rospy
from lebai_driver.io_service.io_service_interface import IOServiceInterface
# from std_srvs.srv import Empty, EmptyResponse, EmptyRequest

def run():    
    rate = rospy.Rate(10) # 10hz
    if not rospy.has_param('robot_ip_address'):
        rospy.logerr('robot_ip_address is not assigned')
        return
    robot_ip = rospy.get_param('robot_ip_address')
    isi = IOServiceInterface(robot_ip)
    # ssi.direct_cmd_enable()

    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node('io_service', anonymous=True)
    try:
        run()
    except rospy.ROSInterruptException:
        pass
