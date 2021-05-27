import rospy
from lebai_msgs.srv import MoveLine, MoveLineRequest, MoveLineResponse
from lebai_msgs.srv import MoveJoint, MoveJointRequest, MoveJointResponse
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
import tf
import math

class MotionServiceProxy:
    def __init__(self):
        rospy.wait_for_service('/motion_service/move_joint')
        rospy.wait_for_service('/motion_service/move_line')
    
    def move_joint(self, joint_pos):
        # rospy.logerr("move joint")
        srv = rospy.ServiceProxy('/motion_service/move_joint', MoveJoint)        
        try:
            move_joint_req = MoveJointRequest()
            move_joint_req.common.vel = 0.5
            move_joint_req.common.acc = 1.0
            move_joint_req.is_joint_pose = True
            move_joint_req.joint_pose = joint_pos
            resp = srv(move_joint_req)
            return True
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            return False


    def move_line(self):
        # rospy.logerr("move line")
        srv = rospy.ServiceProxy('/motion_service/move_line', MoveLine)
        try:
            move_line_req = MoveLineRequest()
            move_line_req.common.vel = 0.3
            move_line_req.common.acc = 1.0            
            pose  = Pose()
            pose.position.x = -0.461
            pose.position.y = -0.253
            pose.position.z = 0.49
            quat_tf = tf.transformations.quaternion_from_euler(45.0 / 180.0 *math.pi, -51  / 180.0 *math.pi, 0.0)
            pose.orientation = Quaternion(*quat_tf)
            move_line_req.is_joint_pose = False
            move_line_req.cartesian_pose = pose
            resp = srv(move_line_req)
            return True
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            return False
