from lebai.type import JointPose, JointPose, CartesianPose
from lebai_msgs.srv import MoveJoint, MoveJointRequest, MoveJointResponse
from lebai_msgs.srv import MoveLine, MoveLineRequest, MoveLineResponse
# from lebai_msgs.srv import MoveCircle, MoveCircleRequest, MoveCircleResponse
import rospy
import tf




class TPTrajectoryHandler:
    def __init__(self, lebai_robot):
        self.lebai_robot_ = lebai_robot
        self.srv_move_joint_ = rospy.Service(rospy.resolve_name('~move_joint'), MoveJoint, self.cmd_move_joint)
        self.srv_move_line_ = rospy.Service(rospy.resolve_name('~move_line'), MoveLine, self.cmd_move_line)
        # self.srv_move_circle_ = rospy.Service(rospy.resolve_name('~move_circle'), MoveCircle, self.cmd_move_circle)

    def cmd_move_joint(self, req):
        res = MoveJointResponse()
        pose_is_joint_angle = req.is_joint_pose
        acc = req.common.acc
        vel = req.common.vel
        time = req.common.time
        radius = req.common.radius
        
        if pose_is_joint_angle:
            self.lebai_robot_.movej(JointPose(req.joint_pose), acc, vel, time, radius)
        else:
            quat_msg = req.cartesian_pose.orientation
            quat_tf = [quat_msg.x, quat_msg.y,quat_msg.z, quat_msg.w]            
            euler = tf.transformations.euler_from_quaternion(quat_tf)
            pose = CartesianPose(req.cartesian_pose.position.x, req.cartesian_pose.position.y, req.cartesian_pose.position.z
            ,euler[2],euler[1],euler[0])            
            self.lebai_robot_.movej(pose, acc, vel, time, radius)            
        res.ret = True
        return res

    def cmd_move_line(self, req):
        res = MoveLineResponse()
        pose_is_joint_angle = req.is_joint_pose
        acc = req.common.acc
        vel = req.common.vel
        time = req.common.time
        radius = req.common.radius
        if pose_is_joint_angle:
            self.lebai_robot_.movel(JointPose(req.joint_pose), acc, vel, time, radius)
        else:
            quat_msg = req.cartesian_pose.orientation
            quat_tf = [quat_msg.x, quat_msg.y,quat_msg.z, quat_msg.w]            
            euler = tf.transformations.euler_from_quaternion(quat_tf)
            pose = CartesianPose(req.cartesian_pose.position.x, req.cartesian_pose.position.y, req.cartesian_pose.position.z
            ,euler[2],euler[1],euler[0])
            self.lebai_robot_.movel(pose, acc, vel, time, radius)
        res.ret = True
        return res

    # def cmd_move_circle(self, req):
    #     res = MoveCircleResponse()
    #     res.ret = True
    #     return res
