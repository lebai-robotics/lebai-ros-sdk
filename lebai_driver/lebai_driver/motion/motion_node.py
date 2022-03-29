import rclpy
from rclpy.executors import MultiThreadedExecutor
from lebai_driver.motion.motion_service_interface import MotionServiceInterface
from lebai_driver.motion.trajectory_action_server import TrajectoryActionServer

def main(args=None):
    rclpy.init(args=None)
    executor = MultiThreadedExecutor()
    msi = MotionServiceInterface()
    tas = TrajectoryActionServer()

    executor.add_node(msi)
    executor.add_node(tas)
    executor.spin()

    tas.destroy_node()
    msi.destroy_node()
    
    rclpy.shutdown()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass