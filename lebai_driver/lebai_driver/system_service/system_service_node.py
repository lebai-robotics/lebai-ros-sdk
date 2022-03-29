import rclpy
from lebai_driver.system_service.system_service_interface import SystemServiceInterface

def main(args=None):
    rclpy.init(args=None)
    ssi = SystemServiceInterface()
    rclpy.spin(ssi)
    ssi.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass
