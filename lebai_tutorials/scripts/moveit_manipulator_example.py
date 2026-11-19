#!/usr/bin/env python3

import argparse
import sys

import moveit_commander
import rospy

from lebai_tutorials_common import parse_six_numbers


def main():
    parser = argparse.ArgumentParser(description='Plan a joint-space goal for the LM3 arm.')
    parser.add_argument('--joints', type=parse_six_numbers, default='-0.35,-1.0,1.2,-1.1,-0.6,0.0',
                        help='six comma-separated joint positions in radians')
    parser.add_argument('--execute', action='store_true', help='execute the plan after planning')
    args = parser.parse_args(rospy.myargv()[1:])

    moveit_commander.roscpp_initialize(sys.argv)
    try:
        rospy.init_node('moveit_manipulator_example')
        arm = moveit_commander.MoveGroupCommander('manipulator', wait_for_servers=10.0)
        arm.set_max_velocity_scaling_factor(0.2)
        arm.set_max_acceleration_scaling_factor(0.2)
        arm.set_start_state_to_current_state()
        arm.set_joint_value_target(args.joints)
        planned, trajectory, _, error = arm.plan()
        if not planned:
            rospy.logerr('MoveIt planning failed with error code %d', error.val)
            return 1
        if args.execute and not arm.execute(trajectory, wait=True):
            rospy.logerr('MoveIt trajectory execution failed')
            return 1
        rospy.loginfo('Manipulator trajectory %s', 'executed' if args.execute else 'planned')
    except (RuntimeError, moveit_commander.MoveItCommanderException) as exc:
        rospy.logerr('%s', exc)
        return 1
    finally:
        moveit_commander.roscpp_shutdown()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
