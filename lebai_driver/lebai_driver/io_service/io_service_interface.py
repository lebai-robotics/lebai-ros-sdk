from lebai import LebaiRobot
from rclpy.node import Node
from rclpy.parameter import Parameter
from lebai_interfaces.srv import SetAO
from lebai_interfaces.srv import SetDO
from lebai_interfaces.srv import SetAMode
from lebai_interfaces.srv import SetGripper


class IOServiceInterface(Node):
    def __init__(self):
        super().__init__('io_service')
        
        self.declare_parameter("robot_ip_address", "")
        self.declare_parameter("has_gripper", Parameter.Type.BOOL)        
        if not self.has_parameter('robot_ip_address'):
            self.get_logger().info('"robot_ip_address" is not assigned.')
            raise ValueError("No 'robot_ip_address' parameter.")
        self.has_gripper_ = self.get_parameter("has_gripper").get_parameter_value().bool_value
        self.robot_ip_ = self.get_parameter('robot_ip_address').get_parameter_value().string_value
        self.lebai_robot_ = LebaiRobot(self.robot_ip_, False)
        
        
        self.srv_set_robot_do_ = self.create_service(SetDO, self.get_name()+'/set_robot_do', self.cmd_set_robot_do)
        self.srv_set_robot_ao_ = self.create_service(SetAO, self.get_name()+'/set_robot_ao', self.cmd_set_robot_ao)
        
        self.srv_set_robot_ao_mode_ = self.create_service(SetAMode, self.get_name()+'/set_robot_ao_mode', self.cmd_set_robot_ao_mode)
        self.srv_set_robot_ai_mode_ = self.create_service(SetAMode, self.get_name()+'/set_robot_ai_mode', self.cmd_set_robot_ai_mode)
        
        self.srv_set_extend_do_ = self.create_service(SetDO, self.get_name()+'/set_extend_do', self.cmd_set_extend_do)        
        self.srv_set_extend_ao_ = self.create_service(SetAO, self.get_name()+'/set_extend_ao', self.cmd_set_extend_ao)
        
        self.srv_set_flange_do_ = self.create_service(SetDO, self.get_name()+'/set_flange_do', self.cmd_set_flange_do)
        if self.has_gripper_:
            self.srv_set_gripper_position_ = self.create_service(SetGripper, self.get_name()+'/set_gripper_position', self.cmd_set_gripper_position)
            self.srv_set_gripper_force_ = self.create_service(SetGripper, self.get_name()+'/set_gripper_force', self.cmd_set_gripper_force)

    def cmd_set_robot_do(self, request: SetDO.Request, response: SetDO.Response):
        self.lebai_robot_.set_do(request.pin, request.value)
        response.code  = True
        return response

    def cmd_set_robot_ao(self, request: SetAO.Request, response: SetAO.Response):
        self.lebai_robot_.set_ao(request.pin, request.value)
        response.code  = True
        return response

    def cmd_set_extend_do(self, request: SetDO.Request, response: SetDO.Response):
        self.lebai_robot_.set_extra_do(request.pin, request.value)
        response.code  = True
        return response

    def cmd_set_extend_ao(self, request: SetAO.Request, response: SetAO.Response):
        self.lebai_robot_.set_extra_ao(request.pin, request.value)
        response.code  = True
        return response

    def cmd_set_robot_ao_mode(self, request: SetAMode.Request, response: SetAMode.Response):
        self.lebai_robot_.set_ao_mode(request.pin, request.mode)
        response.code  = True
        return response

    def cmd_set_robot_ai_mode(self, request: SetAMode.Request, response: SetAMode.Response):
        self.lebai_robot_.set_ai_mode(request.pin, request.mode)
        request.code  = True
        return request

    def cmd_set_flange_do(self, request: SetDO.Request, response: SetDO.Response):
        self.lebai_robot_.set_flange_do(request.pin, request.value)
        response.code  = True   
        return response

    def cmd_set_gripper_position(self, request: SetGripper.Request, response: SetGripper.Response):
        self.lebai_robot_.set_claw(amplitude = request.val)
        response.ret = True
        return response

    def cmd_set_gripper_force(self, request: SetGripper.Request, response: SetGripper.Response):
        self.lebai_robot_.set_claw(force = request.val)
        response.ret = True
        return response


