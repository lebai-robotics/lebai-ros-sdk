from lebai import LebaiRobot
import asyncio
from std_srvs.srv import Empty, EmptyResponse, EmptyRequest
import rospy



class SystemServiceInterface:
    def __init__(self, ip):
        self.lebai_robot_ = LebaiRobot(ip, False)
        self.srv_emergency_stop_ = rospy.Service(rospy.resolve_name('~emergency_stop'), Empty, self.cmd_emergency_stop)
        self.srv_power_on_ = rospy.Service(rospy.resolve_name('~power_on'), Empty, self.cmd_power_on)
        self.srv_power_off_ = rospy.Service(rospy.resolve_name('~power_off'), Empty, self.cmd_power_off)
        self.srv_enable_ = rospy.Service(rospy.resolve_name('~enable'), Empty, self.cmd_enable)
        self.srv_disable_ = rospy.Service(rospy.resolve_name('~disable'), Empty, self.cmd_disable)
        self.srv_pause_motion_ = rospy.Service(rospy.resolve_name('~pause_motion'), Empty, self.cmd_pause_motion)
        self.srv_resume_motion_ = rospy.Service(rospy.resolve_name('~resume_motion'), Empty, self.cmd_resume_motion)
        self.srv_abort_motion_ = rospy.Service(rospy.resolve_name('~abort_motion'), Empty, self.cmd_abort_motion)
        self.srv_entry_teach_mode_ = rospy.Service(rospy.resolve_name('~entry_teach_mode'), Empty, self.cmd_entry_teach_mode)
        self.srv_exit_teach_mode_ = rospy.Service(rospy.resolve_name('~exit_teach_mode'), Empty, self.cmd_exit_teach_mode)
        self.srv_turn_off_robot_ = rospy.Service(rospy.resolve_name('~turn_off_robot'), Empty, self.cmd_turn_off_robot)

    def cmd_emergency_stop(self, req):
        self.lebai_robot_.estop()        
        return EmptyResponse()

    def cmd_power_on(self, req):
        self.lebai_robot_.start_sys()
        return EmptyResponse()

    def cmd_power_off(self, req):
        self.lebai_robot_.stop_sys()
        return EmptyResponse()

    def cmd_enable(self, req):
        self.lebai_robot_.start_sys()
        return EmptyResponse()

    def cmd_disable(self, req):
        self.lebai_robot_.stop_sys()
        return EmptyResponse()

    def cmd_pause_motion(self, req):
        self.lebai_robot_.pause()
        return EmptyResponse()

    def cmd_resume_motion(self, req):
        self.lebai_robot_.resume()
        return EmptyResponse()

    def cmd_abort_motion(self, req):
        self.lebai_robot_.stop()
        return EmptyResponse()
    
    def cmd_entry_teach_mode(self, req):
        self.lebai_robot_.teach_mode()
        return EmptyResponse()

    def cmd_exit_teach_mode(self, req):
        self.lebai_robot_.end_teach_mode()
        return EmptyResponse()
    
    def cmd_turn_off_robot(self, req):
        self.lebai_robot_.powerdown()
        return EmptyResponse()
