from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    has_gripper_arg = DeclareLaunchArgument(name='has_gripper', default_value='false', choices=['true', 'false'],
                                            description='mount gripper on the end')
    # launch.actions.substitutions.
    has_gripper = LaunchConfiguration('has_gripper')
    robot_ip_arg = DeclareLaunchArgument(name='robot_ip',
                                         description='Robot ip address to connect.')
    robot_ip = LaunchConfiguration('robot_ip')

    robot_state_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('lebai_driver'),
                'launch',
                'robot_state.launch.py'
            ])
        ]),
        launch_arguments={
            'has_gripper': has_gripper,
            'robot_ip': robot_ip
        }.items()
    )

    io_service_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('lebai_driver'),
                'launch',
                'io_service.launch.py'
            ])
        ]),
        launch_arguments={
            'has_gripper': has_gripper,
            'robot_ip': robot_ip
        }.items()
    )

    system_service_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('lebai_driver'),
                'launch',
                'system_service.launch.py'
            ])
        ]),
        launch_arguments={
            'robot_ip': robot_ip
        }.items()
    )

    motion_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('lebai_driver'),
                'launch',
                'motion.launch.py'
            ])
        ]),
        launch_arguments={
            'robot_ip': robot_ip
        }.items()
    )

    return LaunchDescription([
        has_gripper_arg,
        robot_ip_arg,
        robot_state_node,
        io_service_node,
        system_service_node,
        motion_node
    ])
