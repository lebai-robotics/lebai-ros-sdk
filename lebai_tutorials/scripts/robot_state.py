#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState


def callback(data: JointState):
    rospy.loginfo("Joint pose: %s", data.position)
    
def Run():
    rospy.Subscriber("/joint_states", JointState, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('robot_state', anonymous=True)
        Run()
    except rospy.ROSInterruptException:
        pass
