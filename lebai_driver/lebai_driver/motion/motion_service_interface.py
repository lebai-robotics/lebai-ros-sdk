from lebai import LebaiRobot
from rclpy.node import Node
from rclpy.parameter import Parameter
from lebai_driver.motion.tp_trajectory_handler import TPTrajectoryHandler
from lebai_driver.param_utils import get_joint_names
# from urdf_parser_py.urdf import URDF


class MotionServiceInterface(Node):
    def __init__(self):
        super().__init__("motion_service")
        self.declare_parameter("controller_joint_names", Parameter.Type.STRING_ARRAY)
        self.declare_parameter("robot_ip_address", "")
        self.joints_name_ = get_joint_names(self, 'controller_joint_names', "robot_description")
        if not self.joints_name_:
            self.get_logger().error('controller_joint_names is not assigned!')
            raise ValueError("No 'controller_joint_names' parameter.")
        if not self.has_parameter('robot_ip_address'):
            self.get_logger().info('"robot_ip_address" is not assigned.')
            raise ValueError("No 'robot_ip_address' parameter.")
        self.robot_ip_ = self.get_parameter('robot_ip_address').get_parameter_value().string_value
        self.lebai_robot_ = LebaiRobot(self.robot_ip_, False)
        self.tp_traj_handler_ = TPTrajectoryHandler(self, self.lebai_robot_)
        # self.xxx_ = MinimalActionServer(self)
        # self.joint_trajectory_action_server_ = JointTrajectoryActionServer(self, self.lebai_robot_, self.joints_name_)
        # self.tp_stream_traj_handler_ = TPStreamTrajectoryHandler(self.lebai_robot_, self.joints_name_)
        

    # def __del__(self):
    #     self.destroy_node()
