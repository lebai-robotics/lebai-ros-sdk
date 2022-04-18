#!/usr/bin/env python2

import rospy
from lebai_msgs.msg import MoveCommon
from lebai_msgs.srv import MoveJoint
from lebai_msgs.srv import MoveLine
from lebai_msgs.srv import MoveCircle
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion
import math
from tf.transformations import quaternion_from_euler


def SendMoveJoint(joint_pos):
    rospy.wait_for_service("/motion_service/move_joint")
    try:
        move_joint_caller = rospy.ServiceProxy('/motion_service/move_joint', MoveJoint)
        move_common = MoveCommon()
        move_common.vel = 0.2
        move_common.acc = 0.5
        move_common.time = 0.0
        # Call the service
        result = move_joint_caller(is_joint_pose = True, joint_pose = joint_pos, 
        common = move_common)

        rospy.loginfo("Move joint result %d", result.ret)
        return
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)


def SendMoveLine():
    rospy.wait_for_service("/motion_service/move_line")
    try:
        move_line_caller = rospy.ServiceProxy('/motion_service/move_line', MoveLine)
        move_common = MoveCommon()
        move_common.vel = 0.1
        move_common.acc = 1.0
        move_common.time = 0.0
        pose  = Pose()
        pose.position.x = -0.461
        pose.position.y = -0.253
        pose.position.z = 0.49
        quat_tf = quaternion_from_euler(45.0 / 180.0 *math.pi, -51  / 180.0 *math.pi, 0.0)
        pose.orientation = Quaternion(*quat_tf)

        result = move_line_caller(is_joint_pose = False, cartesian_pose = pose, 
        common = move_common)
        rospy.loginfo("Move line result %d\n", result.ret)
        return
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)

def SendMoveCircle():
    rospy.wait_for_service("/motion_service/move_circle")
    try:
        move_circle_caller = rospy.ServiceProxy('/motion_service/move_circle', MoveCircle)
        move_common = MoveCommon()
        move_common.vel = 0.1
        move_common.acc = 1.0
        move_common.time = 0.0

        # Call  the service
        result = move_circle_caller(way_point_is_joint_pose = True, way_point_joint_pose=[0.1, 0.1, 0.1, 0.1,0.1, 0.1], 
        end_point_is_joint_pose = True, 
        end_point_joint_pose = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2], 
        circle_angle = 0.3,
        common = move_common)

        rospy.loginfo("Move result %d\n", result.ret)
        return
    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s", e)
    
def Run():
    SendMoveJoint([0, 0.0, 0.0, 0, math.pi/4, 0])
    SendMoveJoint([0, -1.2, math.pi/6, 0, math.pi/4, 0])
    SendMoveLine()
    # SendMoveCircle()
    return

if __name__ == '__main__':
    try:
        rospy.init_node('move_example', anonymous=True)
        Run()
    except rospy.ROSInterruptException:
        pass
