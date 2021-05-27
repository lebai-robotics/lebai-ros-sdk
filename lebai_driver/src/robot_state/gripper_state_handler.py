from lebai_msgs.msg import GripperStatus
import rospy



class GripperStateHandler:
    def __init__(self, lebai_robot):
        self.lebai_robot_ = lebai_robot
        self.gripper_state_pub_ = rospy.Publisher('gripper_status', GripperStatus, queue_size=1)

    def run(self):
        gripper_status = GripperStatus()
        gripper_status.force = self.lebai_robot_.get_claw_aio('force')
        gripper_status.position = self.lebai_robot_.get_claw_aio('amplitude')
        self.gripper_state_pub_.publish(gripper_status)
