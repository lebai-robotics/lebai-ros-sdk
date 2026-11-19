#!/usr/bin/env python3
"""Advertise the driver action endpoints and publish the resulting joint state."""

import math
import threading

import actionlib
from control_msgs.msg import (FollowJointTrajectoryAction, FollowJointTrajectoryResult,
                              GripperCommand, GripperCommandAction, GripperCommandResult)
import rospy
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.status import register_status_publishers
from trajectory_msgs.msg import JointTrajectory


class FakeControllers:
    def __init__(self, has_gripper):
        names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]
        if has_gripper:
            names.append("gripper_r_joint1")
        self.positions = dict.fromkeys(names, 0.0)
        self.lock = threading.Lock()
        self.arm_goals = 0
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
        self.status = register_status_publishers(RosNodeAdapter(), self)

    @property
    def robot(self):
        return self

    def get_actual_joint_positions(self):
        with self.lock:
            return list(self.positions.values())[:6]

    def get_actual_joint_speed(self):
        return [0.0] * 6

    def get_actual_joint_torques(self):
        return [0.0] * 6

    def get_claw(self):
        if rospy.get_param_cached("~fail_claw", False):
            raise RuntimeError("claw read failed")
        with self.lock:
            amplitude = self.positions.get("gripper_r_joint1", 0.0) * 300.0 / math.pi
        return (0.0, amplitude, False)

    def move_arm(self, goal):
        trajectory = goal.trajectory
        self.arm_goal.publish(trajectory)
        with self.lock:
            self.positions.update(zip(trajectory.joint_names, trajectory.points[-1].positions))
            self.arm_goals += 1
            rospy.set_param("~arm_goals", self.arm_goals)
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
