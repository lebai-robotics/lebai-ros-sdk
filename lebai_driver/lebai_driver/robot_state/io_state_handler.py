from lebai_interfaces.msg import IOStatus
from rclpy.node import Node
from lebai import LebaiRobot



class IOStateHandler:
    def __init__(self, node: Node, lebai_robot: LebaiRobot):
        self.node_ = node
        self.lebai_robot_ = lebai_robot
        self.io_state_pub_ = self.node_.create_publisher(IOStatus,'io_status', 1)
        self.timer_ = self.node_.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        io_status = IOStatus()
        # self.lebai_robot_.set
        for i in range(4):
            io_status.robot_din.append(bool(self.lebai_robot_.get_di(i)))
        ain_type_data = list()
        for i in range(2):
            io_status.robot_ain.append(self.lebai_robot_.get_ai(i))
            ain_type_data.append(self.lebai_robot_.get_ai_mode(i))
        io_status.robot_ain_type = ain_type_data
        # flange_di_data = list()
        for i in range(2):
            io_status.flange_din.append(bool(self.lebai_robot_.get_flange_di(i)))
        self.io_state_pub_.publish(io_status)
        for i in range(2):
            io_status.extend_din.append(bool(self.lebai_robot_.get_extra_di(i)))
            io_status.extend_ain.append(self.lebai_robot_.get_extra_ai(i))
        self.io_state_pub_.publish(io_status)
        