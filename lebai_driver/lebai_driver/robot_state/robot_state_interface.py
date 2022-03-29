# import os, sys
import rclpy
from rclpy.node import Node
from lebai import LebaiRobot
# from sensor_msgs.msg import JointState
from lebai_driver.robot_state.joint_state_handler import JointStateHandler
from lebai_driver.robot_state.robot_state_handler import RobotStateHandler
from lebai_driver.robot_state.io_state_handler import IOStateHandler
from lebai_driver.robot_state.gripper_state_handler import GripperStateHandler


# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)
from lebai_driver.param_utils import get_joint_names
from urdf_parser_py.urdf import URDF

class RobotStateInterface(Node):
    def __init__(self):
        super().__init__("robot_state")
        self.declare_parameter("gripper_joint_names", rclpy.Parameter.Type.STRING_ARRAY)
        self.declare_parameter("controller_joint_names", rclpy.Parameter.Type.STRING_ARRAY)
        self.declare_parameter("robot_ip_address", "")
        self.declare_parameter("has_gripper", rclpy.Parameter.Type.BOOL)
        # self.declare_parameter("robot_description", rclpy.Parameter.Type.STRING)
        self.has_gripper_ = self.get_parameter("has_gripper").get_parameter_value().bool_value
        self.joints_name_ = get_joint_names(self, 'controller_joint_names', "robot_description")
        if not self.joints_name_:
            self.get_logger().error('controller_joint_names is not assigned!')
            raise ValueError("No 'controller_joint_names' parameter.")
        if self.has_gripper_ and self.has_parameter("gripper_joint_names"):
            self.gripper_name_ = self.get_parameter_or("gripper_joint_names").get_parameter_value().string_array_value
        else:
            self.gripper_name_ = list()
        if not self.has_parameter('robot_ip_address'):
            self.get_logger().info('"robot_ip_address" is not assigned.')
            raise ValueError("No 'robot_ip_address' parameter.")
        self.robot_ip_ = self.get_parameter('robot_ip_address').get_parameter_value().string_value
        self.get_logger().info("'robot_ip_address' is: '%s'."%self.robot_ip_)
        self.lebai_robot_ = LebaiRobot(self.robot_ip_, False)
       
        self.joint_state_handler_ = JointStateHandler(self, self.lebai_robot_, self.joints_name_, self.gripper_name_)
        self.robot_state_handler_ = RobotStateHandler(self, self.lebai_robot_)
        self.io_state_handler_ = IOStateHandler(self, self.lebai_robot_)
        if self.has_gripper_:
            self.gripper_state_handler_ = GripperStateHandler(self, self.lebai_robot_)


    # def update_joint_state_handler(self):
    #     self.joint_state_handler_.run()

    # def update_io_state_handler(self):
    #     self.io_state_handler_.run()        

    # def update_gripper_state_handler(self):
    #     self.gripper_state_handler_.run()

    # def update_robot_state_handler(self):
    #      self.robot_state_handler_.run()

    # def run(self):
    #     self.update_joint_state_handler()
    #     self.update_io_state_handler()
    #     self.update_gripper_state_handler()
    #     self.update_robot_state_handler()
