#!/usr/bin/env python2

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


def SendMoveJoint():
    rospy.wait_for_service("/motion_service/move_joint")
    try:
        move_joint_caller = rospy.ServiceProxy('/motion_service/move_joint', MoveJoint)
        move_common = MoveCommon()
        move_common.is_continous_mode = False
        move_common.vel = 0.2
        move_common.acc = 0.5
        move_common.time = 0.0
        move_common.until = True
        move_common.until_info.io_express_logic = UntilInfo.LOGIC_AND
        express_1= IOConditionalExpress()
        express_1.group = 0
        express_1.type = IOConditionalExpress.TYPE_DIGITAL
        express_1.pin = 4
        express_1.uint_value = 1
        express_1.logic_operation = 2
        
        express_2 = IOConditionalExpress()
        express_2.group = 1
        express_2.type = IOConditionalExpress.TYPE_ANALOG
        express_2.pin = 1
        express_2.float_value= 3.579
        express_2.logic_operation = 3

        move_common.until_info.io_express = [express_1, express_2]
        move_joint_execute_mode = ExecuteMode()
        move_joint_execute_mode.data = ExecuteMode.EXECUTE_MODE_BUFFER

        # Call  the service
        result = move_joint_caller(is_joint_pose = True, joint_pose = [0.1, 0.2, 0.3, 0.4, 0.0, 0.0], 
        common = move_common, execute_mode = move_joint_execute_mode)

        rospy.loginfo("move result %d\n", result.ret)
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

        move_line_cartesian_pose = Pose(position=Point(0.1,0.2,0.3), orientation=Quaternion(0.0, 0.0, 0.0, 1.0))
        # Call  the service
        result = move_line_caller(is_joint_pose = False, cartesian_pose = move_line_cartesian_pose, 
        common = move_common, execute_mode = move_line_execute_mode)

        rospy.loginfo("move result %d\n", result.ret)
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
    SendMoveJoint()
    SendMoveLine()
    SendMoveCircle()
    return

if __name__ == '__main__':
    try:
        rospy.init_node('move_example', anonymous=True)
        Run()
    except rospy.ROSInterruptException:
        pass