import rospy
from std_srvs.srv import Empty, EmptyRequest

class SystemServiceProxy:
    def __init__(self):
        rospy.wait_for_service('/system_service/enable')
        rospy.wait_for_service('/system_service/disable')
        rospy.wait_for_service('/system_service/emergency_stop')
    
    def enable(self):
        srv = rospy.ServiceProxy('/system_service/enable', Empty)        
        try:
            resp = srv(EmptyRequest())
            return True
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            return False

    def disable(self):
        srv = rospy.ServiceProxy('/system_service/disable', Empty)        
        try:
            resp = srv(EmptyRequest())
            return True
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            return False

    def emergency_stop(self):
        srv = rospy.ServiceProxy('/system_service/emergency_stop', Empty)        
        try:
            resp = srv(EmptyRequest())
            return True
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            return False

    def power_on(self):
        srv = rospy.ServiceProxy('/system_service/power_on', Empty)        
        try:
            resp = srv(EmptyRequest())
            return True
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
            return False