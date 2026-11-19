#!/usr/bin/env python3
import math
import sys
import unittest

from control_msgs.msg import GripperCommand
import moveit_commander
import rospy
import rostest
from moveit_msgs.msg import RobotTrajectory
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class MoveItExecution(unittest.TestCase):
    __test__ = False  # The rostest launch supplies move_group and the action servers.

    def plan_and_execute(self, group):
        success, plan, _, error = group.plan()
        self.assertTrue(success, "Planning failed for %s (code %s)" % (group.get_name(), error.val))
        self.assertGreater(len(plan.joint_trajectory.points), 1)
        self.assertTrue(group.execute(plan, wait=True), "Execution failed for " + group.get_name())

    def test_selected_controllers_execute(self):
        has_gripper = rospy.get_param("~has_gripper")
        rospy.wait_for_message("joint_states", JointState, timeout=15)
        robot = moveit_commander.RobotCommander()
        self.assertIn("manipulator", robot.get_group_names())
        self.assertEqual("gripper" in robot.get_group_names(), has_gripper)
        arm = moveit_commander.MoveGroupCommander("manipulator", wait_for_servers=30)
        target = [0.12, 0.0, 0.0, 0.0, 0.0, 0.0]
        arm.set_joint_value_target(target)
        self.plan_and_execute(arm)
        sent = rospy.wait_for_message("/fake_moveit_controllers/arm_goal", JointTrajectory, timeout=5)
        self.assertEqual(sent.joint_names, ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"])
        self.assertGreater(len(sent.points), 1)
        self.assertEqual(len(sent.points[-1].positions), len(target))
        for actual, expected in zip(sent.points[-1].positions, target):
            self.assertAlmostEqual(actual, expected, delta=0.002)
        rospy.loginfo("Arm executed %d points at /lebai_trajectory_controller, joint_1=%.6f",
                      len(sent.points), sent.points[-1].positions[0])

        if has_gripper:
            gripper = moveit_commander.MoveGroupCommander("gripper", wait_for_servers=30)
            gripper.set_named_target("open")
            self.plan_and_execute(gripper)
            command = rospy.wait_for_message("/fake_moveit_controllers/gripper_goal", GripperCommand, timeout=5)
            self.assertAlmostEqual(command.position, math.pi / 3, delta=0.002)
            rospy.loginfo("Named open executed at /lebai_gripper_controller/gripper_cmd, position=%.6f",
                          command.position)
            self.check_claw_read_failure_blocks_execution(arm)
        else:
            controllers = rospy.get_param("/move_group/controller_list")
            self.assertEqual([c["name"] for c in controllers], ["/lebai_trajectory_controller"])
            topics = dict(rospy.get_published_topics())
            self.assertNotIn("/lebai_gripper_controller/gripper_cmd/status", topics)

    def check_claw_read_failure_blocks_execution(self, arm):
        rospy.set_param("/fake_moveit_controllers/fail_claw", True)
        for _ in range(5):
            raw = rospy.wait_for_message("/lebai/model/joint_states", JointState, timeout=3)
            if not raw.velocity:
                break
        self.assertEqual(list(raw.position), [0.0] * 7)
        self.assertFalse(raw.velocity)
        actual = rospy.wait_for_message("/lebai/status/joint_states", JointState, timeout=3)
        self.assertAlmostEqual(actual.position[0], 0.12, delta=0.002)
        # Send a trajectory whose start matches the fallback but differs from the arm.
        plan = RobotTrajectory()
        plan.joint_trajectory.joint_names = list(actual.name)
        for seconds, first in ((0, 0.0), (1, 0.2)):
            plan.joint_trajectory.points.append(JointTrajectoryPoint(
                positions=[first] + [0.0] * 5, velocities=[0.0] * 6,
                accelerations=[0.0] * 6, time_from_start=rospy.Duration(seconds)))
        count = rospy.get_param("/fake_moveit_controllers/arm_goals")
        self.assertFalse(arm.execute(plan, wait=True), "MoveIt executed from the model fallback")
        self.assertEqual(rospy.get_param("/fake_moveit_controllers/arm_goals"), count)


if __name__ == "__main__":
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node("test_moveit_execution")
    try:
        rostest.rosrun("lebai_lm3_moveit_config", "moveit_execution", MoveItExecution)
    finally:
        moveit_commander.roscpp_shutdown()
