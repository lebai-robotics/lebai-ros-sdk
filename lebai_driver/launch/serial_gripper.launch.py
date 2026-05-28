from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='lebai'),
        DeclareLaunchArgument('port_name', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('gripper_state_publish_rate', default_value='10.0'),
        Node(
            package='lebai_driver',
            executable='serial_gripper',
            name='lebai_serial_gripper',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[{
                'port_name': LaunchConfiguration('port_name'),
                'gripper_state_publish_rate': LaunchConfiguration(
                    'gripper_state_publish_rate',
                ),
            }],
        ),
    ])
