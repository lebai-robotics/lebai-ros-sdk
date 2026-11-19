#!/usr/bin/env python3

import argparse
import math

import actionlib
import rospy
from actionlib_msgs.msg import GoalStatus
from control_msgs.msg import GripperCommandAction, GripperCommandGoal

from lebai_tutorials_common import amplitude_to_gripper_joint


def main():
    parser = argparse.ArgumentParser(
        description='Command the LM3 claw through its controller action. Requires has_gripper:=true.',
    )
    parser.add_argument('--amplitude', type=float, required=True, help='claw opening in percent, 0 through 100')
    parser.add_argument('--max-effort', type=float, default=50.0)
    parser.add_argument('--action-name', default='/lebai_gripper_controller/gripper_cmd')
    args = parser.parse_args(rospy.myargv()[1:])
    if not math.isfinite(args.max_effort):
        parser.error('--max-effort must be finite')

    try:
        position = amplitude_to_gripper_joint(args.amplitude)
    except ValueError as exc:
        parser.error(str(exc))

    rospy.init_node('moveit_gripper_amplitude_example')
    client = actionlib.SimpleActionClient(args.action_name, GripperCommandAction)
    if not client.wait_for_server(rospy.Duration(5.0)):
        rospy.logerr('Action server %s is unavailable', args.action_name)
        return 1

    goal = GripperCommandGoal()
    goal.command.position = position
    goal.command.max_effort = args.max_effort
    client.send_goal(goal)
    if not client.wait_for_result(rospy.Duration(10.0)):
        client.cancel_goal()
        rospy.logerr('Timed out waiting for the gripper action result')
        return 1

    result = client.get_result()
    if client.get_state() != GoalStatus.SUCCEEDED or result is None or not result.reached_goal:
        rospy.logerr('The claw did not reach the requested amplitude')
        return 1
    rospy.loginfo('Claw joint reached %.3f rad with effort %.1f', result.position, result.effort)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
