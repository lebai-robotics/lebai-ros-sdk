#!/usr/bin/env python

import lebai_msgs
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from lebai_msgs.msg import ExecuteMode
from lebai_msgs.msg import MoveCommon
from lebai_msgs.msg import UntilInfo
from lebai_msgs.msg import IOConditionalExpress
from lebai_msgs.srv import MoveJoint
from lebai_msgs.srv import MoveLine
from lebai_msgs.srv import MoveCircle
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
import math
# import tf2_geometry_msgs
# import tf2_ros
# import tf2_msgs
import tf
from tf.transformations import quaternion_from_euler


def SendMoveJoint(joint_pos):
    rospy.wait_for_service("/motion_service/move_joint")
    try:
        move_joint_caller = rospy.ServiceProxy('/motion_service/move_joint', MoveJoint)
        move_common = MoveCommon()
        move_common.is_continous_mode = False
        move_common.vel = 0.2
        move_common.acc = 0.5
        move_common.time = 0.0
        move_common.until = False
        # move_common.until_info.io_express_logic = UntilInfo.LOGIC_AND
        # express_1= IOConditionalExpress()
        # express_1.group = 0
        # express_1.type = IOConditionalExpress.TYPE_DIGITAL
        # express_1.pin = 4
        # express_1.uint_value = 1
        # express_1.logic_operation = 2        
        # express_2 = IOConditionalExpress()
        # express_2.group = 1
        # express_2.type = IOConditionalExpress.TYPE_ANALOG
        # express_2.pin = 1
        # express_2.float_value= 3.579
        # express_2.logic_operation = 3
        # move_common.until_info.io_express = [express_1, express_2]

        move_joint_execute_mode = ExecuteMode()
        move_joint_execute_mode.data = ExecuteMode.EXECUTE_MODE_BUFFER

        # Call  the service
        result = move_joint_caller(is_joint_pose = True, joint_pose = joint_pos, 
        common = move_common, execute_mode = move_joint_execute_mode)

        rospy.loginfo("move joint result %d\n", result.ret)
        return
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


def SendMoveLine():
    rospy.wait_for_service("/motion_service/move_line")
    try:
        move_line_caller = rospy.ServiceProxy('/motion_service/move_line', MoveLine)
        move_common = MoveCommon()
        move_common.is_continous_mode = False
        move_common.vel = 0.1
        move_common.acc = 1.0
        move_common.time = 0.0
        move_common.until = False
        move_line_execute_mode = ExecuteMode()
        move_line_execute_mode.data = ExecuteMode.EXECUTE_MODE_BUFFER
        pose  = Pose()
        pose.position.x = -0.461
        pose.position.y = -0.253
        pose.position.z = 0.49
        quat_tf = quaternion_from_euler(45.0 / 180.0 *math.pi, -51  / 180.0 *math.pi, 0.0)
        pose.orientation = Quaternion(*quat_tf)

        result = move_line_caller(is_joint_pose = False, cartesian_pose = pose, 
        common = move_common, execute_mode = move_line_execute_mode)
        rospy.loginfo("move line result %d\n", result.ret)
        return
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def SendMoveCircle():
    rospy.wait_for_service("/motion_service/move_circle")
    try:
        move_circle_caller = rospy.ServiceProxy('/motion_service/move_circle', MoveCircle)
        move_common = MoveCommon()
        move_common.is_continous_mode = False
        move_common.vel = 0.1
        move_common.acc = 1.0
        move_common.time = 0.0
        move_common.until = False
        move_circle_execute_mode = ExecuteMode()
        move_circle_execute_mode.data = ExecuteMode.EXECUTE_MODE_BUFFER
        # Call  the service
        result = move_circle_caller(way_point_is_joint_pose = True, way_point_joint_pose=[0.1, 0.1, 0.1, 0.1,0.1, 0.1], 
        end_point_is_joint_pose = True, 
        end_point_joint_pose = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2], 
        circle_angle = 0.3,
        common = move_common, execute_mode = move_circle_execute_mode)

        rospy.loginfo("move result %d\n", result.ret)
        return
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    
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