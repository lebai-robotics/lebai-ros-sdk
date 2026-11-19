#!/usr/bin/env python3

import argparse

import rospy
from lebai_interfaces.msg import CartesianPose, MotionParams, MotionTarget
from lebai_interfaces.srv import MoveJoint, MoveLinear, WaitMove

from lebai_tutorials_common import checked_response, parse_six_numbers


def main():
    parser = argparse.ArgumentParser(description='Send a joint or Cartesian target to the driver.')
    targets = parser.add_mutually_exclusive_group(required=True)
    targets.add_argument('--joints', type=parse_six_numbers, help='six comma-separated joint positions in radians')
    targets.add_argument('--pose', type=parse_six_numbers, help='comma-separated x,y,z,rx,ry,rz')
    parser.add_argument('--wait', action='store_true', help='block in wait_move until the SDK returns')
    args = parser.parse_args(rospy.myargv()[1:])

    rospy.init_node('move_example')
    if args.joints is not None:
        name, service = '/lebai/motion/movej', MoveJoint
        target = MotionTarget(is_joint_pose=True, joint_positions=args.joints)
    else:
        name, service = '/lebai/motion/movel', MoveLinear
        target = MotionTarget(cartesian_pose=CartesianPose(*args.pose))
    params = MotionParams(acceleration=1.0, velocity=0.1)

    try:
        rospy.wait_for_service(name, timeout=5.0)
        move = rospy.ServiceProxy(name, service)
        response = checked_response(name, move(target=target, params=params))
        rospy.loginfo('Motion ID is %s', response.motion_id)
        if args.wait:
            wait_name = '/lebai/motion/wait_move'
            rospy.wait_for_service(wait_name, timeout=5.0)
            wait_move = rospy.ServiceProxy(wait_name, WaitMove)
            checked_response(wait_name, wait_move(motion_id=response.motion_id))
            rospy.loginfo('Motion %s completed', response.motion_id)
    except (rospy.ROSException, rospy.ServiceException, RuntimeError) as exc:
        rospy.logerr('%s', exc)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
