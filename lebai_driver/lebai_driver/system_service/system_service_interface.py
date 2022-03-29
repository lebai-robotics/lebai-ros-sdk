from lebai import LebaiRobot
from std_srvs.srv import Empty
from rclpy.node import Node
from rclpy.parameter import Parameter



class SystemServiceInterface(Node):
    def __init__(self):
        super().__init__('system_service')
        self.declare_parameter("robot_ip_address", "")
        if not self.has_parameter('robot_ip_address'):
            self.get_logger().info('"robot_ip_address" is not assigned.')
            raise ValueError("No 'robot_ip_address' parameter.")
        self.robot_ip_ = self.get_parameter('robot_ip_address').get_parameter_value().string_value
        self.lebai_robot_ = LebaiRobot(self.robot_ip_, False)
        self.srv_emergency_stop_ = self.create_service(Empty, self.get_name()+'/emergency_stop', self.cmd_emergency_stop)
        self.srv_power_on_ = self.create_service(Empty,self.get_name()+'/power_on',  self.cmd_power_on)
        self.srv_power_off_ = self.create_service(Empty,self.get_name()+'/power_off', self.cmd_power_off)
        self.srv_enable_ = self.create_service(Empty, self.get_name()+'/enable', self.cmd_enable)
        self.srv_disable_ = self.create_service(Empty, self.get_name()+'/disable', self.cmd_disable)
        self.srv_pause_motion_ = self.create_service(Empty, self.get_name()+'/disable', self.cmd_pause_motion)
        self.srv_resume_motion_ = self.create_service(Empty, self.get_name()+'/resume_motion', self.cmd_resume_motion)
        self.srv_abort_motion_ = self.create_service(Empty, self.get_name()+'/abort_motion', self.cmd_abort_motion)
        self.srv_entry_teach_mode_ = self.create_service(Empty, self.get_name()+'/entry_teach_mode', self.cmd_entry_teach_mode)
        self.srv_exit_teach_mode_ = self.create_service(Empty, self.get_name()+'/exit_teach_mode', self.cmd_exit_teach_mode)
        self.srv_turn_off_robot_ = self.create_service(Empty, self.get_name()+'/turn_off_robot', self.cmd_turn_off_robot)

    def cmd_emergency_stop(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.estop()        
        return response

    def cmd_power_on(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.start_sys()
        return response

    def cmd_power_off(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.stop_sys()
        return response

    def cmd_enable(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.start_sys()
        return response

    def cmd_disable(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.stop_sys()
        return response

    def cmd_pause_motion(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.pause()
        return response

    def cmd_resume_motion(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.resume()
        return response

    def cmd_abort_motion(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.stop()
        return response
    
    def cmd_entry_teach_mode(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.teach_mode()
        return response

    def cmd_exit_teach_mode(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.end_teach_mode()
        return response
    
    def cmd_turn_off_robot(self, request : Empty.Request, response: Empty.Response):
        self.lebai_robot_.powerdown()
        return response
