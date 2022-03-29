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
        self.node_.get_logger().info("xxxxx")
        
        if pose_is_joint_angle:
            self.lebai_robot_.movej(JointPose(request.joint_pose), acc, vel, time, radius)
        else:
            quat_msg = request.cartesian_pose.orientation
            quat_tf = [quat_msg.x, quat_msg.y,quat_msg.z, quat_msg.w]            
            euler = tf_transformations.euler_from_quaternion(quat_tf)
            pose = CartesianPose(request.cartesian_pose.position.x, request.cartesian_pose.position.y, request.cartesian_pose.position.z
            ,euler[2],euler[1],euler[0])            
            self.lebai_robot_.movej(pose, acc, vel, time, radius)            
        self.node_.get_logger().info("yyyyy")
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

        # ros2 service call /motion_service/move_line lebai_interfaces/srv/MoveLine "{is_joint_pose: false, cartesian_pose: {position: {x: -0.50, y: -0.2, z: 0.3}, orientation: {x: 0.7003041,  y: 0.0317545, z: -0.1042439, w: 0.7054779}}, common: {vel: 0.1, acc: 0.5}}"
        # ros2 service call /motion_service/move_line lebai_interfaces/srv/MoveLine "{is_joint_pose: true, joint_pose: [0.0, -0.6, 0.8, -0.3, 0.1, -0.1], common: {vel: 0.1, acc: 0.5}}"

    # def cmd_move_circle(self, req):
    #     res = MoveCircleResponse()
    #     res.ret = True
    #     return res
