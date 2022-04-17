from lebai.type import JointPose, JointPose, CartesianPose
from lebai_interfaces.srv import MoveJoint
from lebai_interfaces.srv import MoveLine
# from lebai_interfaces.srv import MoveCircle
from rclpy.node import Node
from lebai import LebaiRobot
import tf_transformations




class TPTrajectoryHandler:
    def __init__(self, node: Node, lebai_robot: LebaiRobot):
        self.node_ = node
        self.lebai_robot_ = lebai_robot
        self.srv_move_joint_ = self.node_.create_service(MoveJoint, self.node_.get_name()+'/move_joint', self.cmd_move_joint)
        self.srv_move_line_ = self.node_.create_service(MoveLine, self.node_.get_name()+'/move_line', self.cmd_move_line)
        # self.srv_move_circle_ = rospy.Service(rospy.resolve_name('~move_circle'), MoveCircle, self.cmd_move_circle)

    def cmd_move_joint(self, request: MoveJoint.Request, response: MoveJoint.Response):
        pose_is_joint_angle = request.is_joint_pose
        acc = request.common.acc
        vel = request.common.vel
        time = request.common.time
        radius = request.common.radius
        
        if pose_is_joint_angle:
            self.lebai_robot_.movej(JointPose(request.joint_pose), acc, vel, time, radius)
        else:
            quat_msg = request.cartesian_pose.orientation
            quat_tf = [quat_msg.x, quat_msg.y,quat_msg.z, quat_msg.w]            
            euler = tf_transformations.euler_from_quaternion(quat_tf)
            pose = CartesianPose(request.cartesian_pose.position.x, request.cartesian_pose.position.y, request.cartesian_pose.position.z
            ,euler[2],euler[1],euler[0])            
            self.lebai_robot_.movej(pose, acc, vel, time, radius)            
        response.ret = True
        return response

    def cmd_move_line(self, request: MoveLine.Request, response: MoveLine.Response):
        pose_is_joint_angle = request.is_joint_pose
        acc = request.common.acc
        vel = request.common.vel
        time = request.common.time
        radius = request.common.radius
        if pose_is_joint_angle:
            self.lebai_robot_.movel(JointPose(request.joint_pose), acc, vel, time, radius)
        else:
            quat_msg = request.cartesian_pose.orientation
            quat_tf = [quat_msg.x, quat_msg.y,quat_msg.z, quat_msg.w]            
            euler = tf_transformations.euler_from_quaternion(quat_tf)
            pose = CartesianPose(request.cartesian_pose.position.x, request.cartesian_pose.position.y, request.cartesian_pose.position.z
            ,euler[2],euler[1],euler[0])
            self.lebai_robot_.movel(pose, acc, vel, time, radius)
        response.ret = True
        return response