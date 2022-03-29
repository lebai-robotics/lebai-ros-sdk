# from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
# from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_ip_arg = DeclareLaunchArgument(name='robot_ip', default_value=str(),
                                         description='Robot ip address to connect.')

    robot_ip = LaunchConfiguration('robot_ip')
    system_service_node = Node(
        package='lebai_driver',
        executable='system_service',
        parameters=[{"robot_ip_address": robot_ip}],
        remappings=[("system_service", "ss")],
        output='screen',
    )

    return LaunchDescription([
        robot_ip_arg,
        system_service_node,
    ])
