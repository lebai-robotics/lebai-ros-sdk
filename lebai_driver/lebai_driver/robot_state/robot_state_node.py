#!/usr/bin/python3
import rclpy
from lebai_driver.robot_state.robot_state_interface import RobotStateInterface


def main(args=None):
    rclpy.init(args=None)
    rsi = RobotStateInterface()
    rclpy.spin(rsi)
    rsi.destroy_node()
    rclpy.shutdown()    
   
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass
