#!/usr/bin/env python3
"""Forward complete LM3 measurements to MoveIt's current-state monitor."""

import math

import rospy
from sensor_msgs.msg import JointState


def main():
    rospy.init_node("model_joint_states")
    publisher = rospy.Publisher("output", JointState, queue_size=1)

    def forward(message):
        # The driver's seven-position failure fallback has empty velocity and effort.
        fields = (message.position, message.velocity, message.effort)
        if len(message.name) == 7 and all(len(field) == 7 for field in fields):
            if all(math.isfinite(value) for field in fields for value in field):
                publisher.publish(message)

    rospy.Subscriber("input", JointState, forward, queue_size=1)
    rospy.spin()


if __name__ == "__main__":
    main()
