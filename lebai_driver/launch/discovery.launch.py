from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='lebai'),
        Node(
            package='lebai_driver',
            executable='discovery',
            name='lebai_discovery',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
        ),
    ])
