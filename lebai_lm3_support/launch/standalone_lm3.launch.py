import os
from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
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
    has_gripper_condition = LaunchConfiguration('has_gripper')
    display_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('lebai_lm3_support'),
                'launch',
                'display_lm3.launch.py'
            ])
        ]),
        launch_arguments={
            'joint_state_publisher': 'true'
        }.items(),
        condition=UnlessCondition(has_gripper_condition)
    )
    display_with_gripper_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('lebai_lm3_support'),
                'launch',
                'display_lm3_with_gripper.launch.py'
            ])
        ]),
        launch_arguments={
            'joint_state_publisher': 'true'
        }.items(),
        condition=IfCondition(has_gripper_condition)
    )

    return LaunchDescription([
        has_gripper_arg,
        display_node,
        display_with_gripper_node,
    ])
