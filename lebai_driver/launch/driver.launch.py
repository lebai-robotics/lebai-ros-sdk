from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    parameters = {
        'robot_ip': LaunchConfiguration('robot_ip'),
        'simulator': LaunchConfiguration('simulator'),
        'namespace': LaunchConfiguration('namespace'),
        'joint_state_publish_rate': LaunchConfiguration('joint_state_publish_rate'),
        'robot_state_publish_rate': LaunchConfiguration('robot_state_publish_rate'),
        'joint_motion_publish_rate': LaunchConfiguration('joint_motion_publish_rate'),
        'io_state_publish_rate': LaunchConfiguration('io_state_publish_rate'),
        'gripper_state_publish_rate': LaunchConfiguration('gripper_state_publish_rate'),
        'gripper_joint_name': LaunchConfiguration('gripper_joint_name'),
        'io_state_device': LaunchConfiguration('io_state_device'),
        'io_state_digital_input_count': LaunchConfiguration(
            'io_state_digital_input_count',
        ),
        'io_state_digital_output_count': LaunchConfiguration(
            'io_state_digital_output_count',
        ),
        'io_state_analog_input_count': LaunchConfiguration(
            'io_state_analog_input_count',
        ),
        'io_state_analog_output_count': LaunchConfiguration(
            'io_state_analog_output_count',
        ),
        'io_state_dio_count': LaunchConfiguration('io_state_dio_count'),
    }

    return LaunchDescription([
        DeclareLaunchArgument('robot_ip', default_value='127.0.0.1'),
        DeclareLaunchArgument('simulator', default_value='false'),
        DeclareLaunchArgument('namespace', default_value='lebai'),
        DeclareLaunchArgument('joint_state_publish_rate', default_value='20.0'),
        DeclareLaunchArgument('robot_state_publish_rate', default_value='10.0'),
        DeclareLaunchArgument('joint_motion_publish_rate', default_value='20.0'),
        DeclareLaunchArgument('io_state_publish_rate', default_value='10.0'),
        DeclareLaunchArgument('gripper_state_publish_rate', default_value='10.0'),
        DeclareLaunchArgument('gripper_joint_name', default_value='gripper_r_joint1'),
        DeclareLaunchArgument('io_state_device', default_value='robot'),
        DeclareLaunchArgument('io_state_digital_input_count', default_value='0'),
        DeclareLaunchArgument('io_state_digital_output_count', default_value='0'),
        DeclareLaunchArgument('io_state_analog_input_count', default_value='0'),
        DeclareLaunchArgument('io_state_analog_output_count', default_value='0'),
        DeclareLaunchArgument('io_state_dio_count', default_value='0'),
        Node(
            package='lebai_driver',
            executable='driver',
            name='lebai_driver',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            parameters=[parameters],
        ),
    ])
