import os
import yaml
from ament_index_python.packages import get_package_share_path, get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return yaml.safe_load(file)
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def generate_launch_description():
    lebai_lm3_support_path = get_package_share_path('lebai_lm3_support')
    robot_ip_arg = DeclareLaunchArgument(name='robot_ip',
                                         description='IP of L-Master controller.')
    has_gripper_arg = DeclareLaunchArgument(name='has_gripper', default_value='false', choices=['true', 'false'],
                                            description='mount gripper on the end')
    rviz2_arg = DeclareLaunchArgument(name='rviz2', default_value='false', choices=['true', 'false'],
                                            description='Open a basic rviz2 display node')

    lm3_model_path = lebai_lm3_support_path / 'urdf/lm3.xacro'
    lm3_with_gripper_model_path = lebai_lm3_support_path / 'urdf/lm3_with_gripper.xacro'
    default_rviz_config_path = lebai_lm3_support_path / 'rviz/view.rviz'

    lm3_rd = ParameterValue(Command(['xacro ', str(lm3_model_path)]),
                            value_type=str)
    lm3_with_gripper_rd = ParameterValue(Command(['xacro ', str(lm3_with_gripper_model_path)]),
                            value_type=str)
    robot_ip = LaunchConfiguration('robot_ip')
    has_gripper = LaunchConfiguration('has_gripper')
    robot_interface_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('lebai_driver'),
                'launch',
                'robot_interface.launch.py'
            ])
        ]),
        launch_arguments={
            'has_gripper': has_gripper,
            'robot_ip': robot_ip
        }.items()
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': lm3_rd}],
        condition=UnlessCondition(has_gripper)
    )
    robot_state_publisher_with_gripper_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': lm3_with_gripper_rd}],
        condition=IfCondition(has_gripper)
    )

    rviz2 = LaunchConfiguration('rviz2')

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', str(default_rviz_config_path)],
        condition=IfCondition(rviz2)
    )

    return LaunchDescription([
        robot_ip_arg,
        has_gripper_arg,
        rviz2_arg,
        robot_interface_node,
        robot_state_publisher_node,
        robot_state_publisher_with_gripper_node,
        rviz2_node
    ])
