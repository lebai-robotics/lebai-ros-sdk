import rclpy
from lebai_driver.io_service.io_service_interface import IOServiceInterface

def main(args=None):
    rclpy.init(args=None)
    isi = IOServiceInterface()
    rclpy.spin(isi)
    isi.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass