from lebai import LebaiRobot
from lebai_msgs.srv import SetAO, SetAOResponse, SetAORequest
from lebai_msgs.srv import  SetDO, SetDOResponse, SetDORequest
from lebai_msgs.srv import   SetAMode, SetAModeResponse, SetAModeRequest
from lebai_msgs.srv import   SetGripper, SetGripperResponse, SetGripperRequest
import rospy
from industrial_msgs.msg import ServiceReturnCode



class IOServiceInterface:
    def __init__(self, ip):
        self.lebai_robot_ = LebaiRobot(ip, False)
        self.srv_set_robot_do_ = rospy.Service(rospy.resolve_name('~set_robot_do'), SetDO, self.cmd_set_robot_do)
        self.srv_set_robot_ao_ = rospy.Service(rospy.resolve_name('~set_robot_ao'), SetAO, self.cmd_set_robot_ao)
        self.srv_set_robot_ao_mode_ = rospy.Service(rospy.resolve_name('~set_robot_ao_mode'), SetAMode, self.cmd_set_robot_ao_mode)
        self.srv_set_robot_ai_mode_ = rospy.Service(rospy.resolve_name('~set_robot_ai_mode'), SetAMode, self.cmd_set_robot_ai_mode)
        self.srv_set_flange_do_ = rospy.Service(rospy.resolve_name('~set_flange_do'), SetDO, self.cmd_set_flange_do)
        self.srv_set_gripper_position_ = rospy.Service(rospy.resolve_name('~set_gripper_position'), SetGripper, self.cmd_set_gripper_position)
        self.srv_set_gripper_force_ = rospy.Service(rospy.resolve_name('~set_gripper_force'), SetGripper, self.cmd_set_gripper_force)

    def cmd_set_robot_do(self, req):
        res = SetDOResponse()
        self.lebai_robot_.set_do(req.pin, req.value)
        res.code.val  = ServiceReturnCode.SUCCESS
        return res

    def cmd_set_robot_ao(self, req):
        res = SetAOResponse()
        self.lebai_robot_.set_ao(req.pin, req.value)
        res.code.val  = ServiceReturnCode.SUCCESS
        return res

    def cmd_set_robot_ao_mode(self, req):
        res = SetAModeResponse()
        self.lebai_robot_.set_ao_mode(req.pin, req.mode)
        res.code.val  = ServiceReturnCode.SUCCESS
        return res

    def cmd_set_robot_ai_mode(self, req):
        res = SetAModeResponse()
        self.lebai_robot_.set_ai_mode(req.pin, req.mode)
        res.code.val  = ServiceReturnCode.SUCCESS
        return res

    def cmd_set_flange_do(self, req):
        res = SetDOResponse()        
        self.lebai_robot_.set_flange_do(req.pin, req.value)
        res.code.val  = ServiceReturnCode.SUCCESS   
        return res

    def cmd_set_gripper_position(self, req):
        res = SetGripperResponse()
        self.lebai_robot_.set_claw(amplitude = req.val)
        res.ret = True
        return res

    def cmd_set_gripper_force(self, req):
        res = SetGripperResponse()
        self.lebai_robot_.set_claw(force = req.val)
        res.ret = True
        return res


