#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState


def log_joint_state(message):
    rospy.loginfo_throttle(1.0, 'Joint positions: %s', list(zip(message.name, message.position)))


def main():
    rospy.init_node('joint_state_subscriber')
    rospy.Subscriber('/lebai/status/joint_states', JointState, log_joint_state, queue_size=10)
    rospy.spin()


if __name__ == '__main__':
    main()
