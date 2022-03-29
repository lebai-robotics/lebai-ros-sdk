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
    has_gripper_arg = DeclareLaunchArgument(name='has_gripper', default_value='false', choices=['true', 'false'],
                                            description='mount gripper on the end')
    # launch.actions.substitutions.
    has_gripper = LaunchConfiguration('has_gripper')
    robot_ip_arg = DeclareLaunchArgument(name='robot_ip', default_value=str(),
                                         description='Robot ip address to connect.')

    robot_ip = LaunchConfiguration('robot_ip')
    io_service_node = Node(
        package='lebai_driver',
        executable='io_service',
        parameters=[{"robot_ip_address": robot_ip},{"has_gripper": has_gripper}],
        output='screen',
    )

    return LaunchDescription([
        has_gripper_arg,
        robot_ip_arg,
        io_service_node,
        # robot_state_with_gripper_node
    ])
