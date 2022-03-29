from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    lm3_joint_names = PathJoinSubstitution([
        FindPackageShare('lebai_driver'),
        'config',
        'joint_names_lm3.yaml'
    ])
    robot_ip_arg = DeclareLaunchArgument(name='robot_ip', default_value=str(),
                                         description='Robot ip address to connect.')

    robot_ip = LaunchConfiguration('robot_ip')
    motion_node = Node(
        package='lebai_driver',
        executable='motion',
        parameters=[lm3_joint_names, {"robot_ip_address": robot_ip}],
        output='screen',
    )

    return LaunchDescription([
        robot_ip_arg,
        motion_node,
    ])
