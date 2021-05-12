from lebai_msgs.msg import IOStatus
import rospy



class IOStateHandler:
    def __init__(self, lebai_robot):
        self.lebai_robot_ = lebai_robot
        self.io_state_pub_ = rospy.Publisher('io_status', IOStatus, queue_size=1)

    def run(self):
        io_status = IOStatus()
        for i in range(8):
            io_status.robot_din.append(self.lebai_robot_.get_di(i))
        ain_type_data = list()
        for i in range(2):
            io_status.robot_ain.append(self.lebai_robot_.get_ai(i))
            ain_type_data.append(self.lebai_robot_.get_ai_mode(i))
        io_status.robot_ain_type = ain_type_data
        # flange_di_data = list()
        for i in range(2):
            io_status.flange_din.append(self.lebai_robot_.get_flange_di(i))
        self.io_state_pub_.publish(io_status)
