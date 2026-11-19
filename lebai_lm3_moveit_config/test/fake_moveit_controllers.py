#!/usr/bin/env python3
"""Advertise the driver action endpoints and publish the resulting joint state."""

import threading

import actionlib
from control_msgs.msg import (FollowJointTrajectoryAction, FollowJointTrajectoryResult,
                              GripperCommand, GripperCommandAction, GripperCommandResult)
import rospy
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory


class FakeControllers:
    def __init__(self, has_gripper):
        names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]
        if has_gripper:
            names.append("gripper_r_joint1")
        self.positions = dict.fromkeys(names, 0.0)
        self.lock = threading.Lock()
        self.states = rospy.Publisher("joint_states", JointState, queue_size=1)
        self.arm_goal = rospy.Publisher("~arm_goal", JointTrajectory, queue_size=1, latch=True)
        self.arm = actionlib.SimpleActionServer("/lebai_trajectory_controller",
                                                FollowJointTrajectoryAction, self.move_arm,
                                                auto_start=False)
        self.arm.start()
        if has_gripper:
            self.gripper_goal = rospy.Publisher("~gripper_goal", GripperCommand, queue_size=1, latch=True)
            self.gripper = actionlib.SimpleActionServer("/lebai_gripper_controller/gripper_cmd",
                                                        GripperCommandAction, self.move_gripper,
                                                        auto_start=False)
            self.gripper.start()
        self.timer = rospy.Timer(rospy.Duration(0.02), self.publish_state)

    def publish_state(self, _event):
        state = JointState()
        state.header.stamp = rospy.Time.now()
        with self.lock:
            state.name = list(self.positions)
            state.position = list(self.positions.values())
        self.states.publish(state)

    def move_arm(self, goal):
        trajectory = goal.trajectory
        self.arm_goal.publish(trajectory)
        with self.lock:
            self.positions.update(zip(trajectory.joint_names, trajectory.points[-1].positions))
        self.arm.set_succeeded(FollowJointTrajectoryResult())

    def move_gripper(self, goal):
        self.gripper_goal.publish(goal.command)
        with self.lock:
            self.positions["gripper_r_joint1"] = goal.command.position
        self.gripper.set_succeeded(GripperCommandResult(position=goal.command.position, reached_goal=True))


if __name__ == "__main__":
    rospy.init_node("fake_moveit_controllers")
    controllers = FakeControllers(rospy.get_param("~has_gripper"))
    rospy.spin()
