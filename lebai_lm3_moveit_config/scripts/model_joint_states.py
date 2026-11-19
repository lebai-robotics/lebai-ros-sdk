#!/usr/bin/env python3
"""Forward complete LM3 measurements to MoveIt's current-state monitor."""

import math

import rospy
from sensor_msgs.msg import JointState


MODEL_JOINTS = frozenset(
    ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6",
     "gripper_r_joint1"]
)


def is_complete_model_state(message):
    fields = (message.position, message.velocity, message.effort)
    return (
        len(message.name) == len(MODEL_JOINTS)
        and set(message.name) == MODEL_JOINTS
        and all(len(field) == len(MODEL_JOINTS) for field in fields)
        and all(math.isfinite(value) for field in fields for value in field)
    )


def main():
    rospy.init_node("model_joint_states")
    publisher = rospy.Publisher("output", JointState, queue_size=1)

    def forward(message):
        # The driver's seven-position failure fallback has empty velocity and effort.
        if is_complete_model_state(message):
            publisher.publish(message)

    rospy.Subscriber("input", JointState, forward, queue_size=1)
    rospy.spin()


if __name__ == "__main__":
    main()
