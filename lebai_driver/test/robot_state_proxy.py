import rospy
from industrial_msgs.msg import RobotStatus
from sensor_msgs.msg import JointState
# from std_srvs.srv import Empty, EmptyRequest

class RobotStateProxy:
    def __init__(self):
        # rospy.wait_for_service('/system_service/enable')
        # rospy.wait_for_service('/system_service/enable')
        rospy.Subscriber("robot_status", RobotStatus, self.robot_status_cb)
        rospy.Subscriber("joint_states", JointState, self.joint_states_cb)
        self.robot_status_ = RobotStatus()
        self.joint_states_ = JointState()

       
    
    def robot_status_cb(self, msg):
        self.robot_status_ = msg

    def joint_states_cb(self, msg):
        self.joint_states_ = msg

