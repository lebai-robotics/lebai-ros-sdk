import os
import yaml
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import xacro


def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return yaml.safe_load(file)
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None


def moveit_robot_description(robot_model, srdf_file):
    robot_description_config = xacro.process_file(
        os.path.join(
            get_package_share_directory("lebai_lm3_support"),
            "urdf",
            robot_model,
        )
    )
    robot_description = {"robot_description": robot_description_config.toxml()}

    robot_description_semantic_config = load_file(
        "lebai_lm3_moveit_config", f"config/{srdf_file}"
    )
    robot_description_semantic = {
        "robot_description_semantic": robot_description_semantic_config
    }

    return robot_description, robot_description_semantic


def moveit_nodes(
    robot_description,
    robot_description_semantic,
    robot_description_planning,
    robot_ip,
    simulator,
    namespace,
    robot_model,
    condition,
    joint_state_remappings,
    kinematics_yaml,
    ompl_planning_pipeline_config,
    trajectory_execution,
    moveit_controllers,
    planning_scene_monitor_parameters,
    rviz_full_config,
):
    robot_interface_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('lebai_driver'),
                'launch',
                'driver.launch.py'
            ])
        ]),
        launch_arguments={
            'publish_robot_description': "false",
            'robot_ip': robot_ip,
            'simulator': simulator,
            'namespace': namespace,
            'robot_model': robot_model,
        }.items(),
        condition=condition,
    )

    run_move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        namespace=namespace,
        output="screen",
        parameters=[
            robot_description,
            robot_description_semantic,
            robot_description_planning,
            kinematics_yaml,
            ompl_planning_pipeline_config,
            trajectory_execution,
            moveit_controllers,
            planning_scene_monitor_parameters,
        ],
        remappings=joint_state_remappings,
        condition=condition,
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        namespace=namespace,
        output="log",
        arguments=["-d", rviz_full_config],
        parameters=[
            robot_description,
            robot_description_semantic,
            ompl_planning_pipeline_config,
            kinematics_yaml,
        ],
        remappings=joint_state_remappings,
        condition=condition,
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        namespace=namespace,
        output="both",
        parameters=[robot_description],
        remappings=joint_state_remappings,
        condition=condition,
    )

    return [
        robot_interface_node,
        run_move_group_node,
        rviz_node,
        robot_state_publisher,
    ]


def generate_launch_description():

    # Command-line arguments
    # tutorial_arg = DeclareLaunchArgument(
    #     "rviz_tutorial", default_value="False", description="Tutorial flag"
    # )

    # db_arg = DeclareLaunchArgument(
    #     "db", default_value="False", description="Database flag"
    # )
    robot_ip_arg = DeclareLaunchArgument(
        name='robot_ip',
        description='IP of L-Master controller.',
    )
    simulator_arg = DeclareLaunchArgument(
        name='simulator',
        default_value='false',
        description='Use pylebai simulator mode.',
    )
    namespace_arg = DeclareLaunchArgument(
        name='namespace',
        default_value='lebai',
        description='ROS namespace for the complete driver and MoveIt stack.',
    )
    has_gripper_arg = DeclareLaunchArgument(
        name='has_gripper',
        default_value='true',
        choices=['true', 'false'],
        description='Load the robot model and MoveIt config with a mounted gripper.',
    )
    robot_ip = LaunchConfiguration('robot_ip')
    simulator = LaunchConfiguration('simulator')
    namespace = LaunchConfiguration('namespace')
    has_gripper = LaunchConfiguration('has_gripper')
    gripper_joint_state_remappings = [
        ('joint_states', 'model/joint_states'),
    ]
    arm_joint_state_remappings = [
        ('joint_states', 'status/joint_states'),
    ]
    # planning_context
    gripper_robot_description, gripper_robot_description_semantic = (
        moveit_robot_description("lm3_with_gripper.xacro", "lebai_lm3.srdf")
    )
    arm_robot_description, arm_robot_description_semantic = (
        moveit_robot_description("lm3.xacro", "lebai_lm3_no_gripper.srdf")
    )

    kinematics_yaml = load_yaml(
        "lebai_lm3_moveit_config", "config/kinematics.yaml"
    )
    robot_description_planning = {
        "robot_description_planning": load_yaml(
            "lebai_lm3_moveit_config",
            "config/joint_limits.yaml",
        )
    }

    # Planning Functionality
    ompl_planning_pipeline_config = {
        "move_group": {
            "planning_plugin": "ompl_interface/OMPLPlanner",
            "request_adapters": (
                "default_planner_request_adapters/AddTimeOptimalParameterization "
                "default_planner_request_adapters/ResolveConstraintFrames "
                "default_planner_request_adapters/FixWorkspaceBounds "
                "default_planner_request_adapters/FixStartStateBounds "
                "default_planner_request_adapters/FixStartStateCollision "
                "default_planner_request_adapters/FixStartStatePathConstraints"
            ),
            "start_state_max_bounds_error": 0.1,
        }
    }
    ompl_planning_yaml = load_yaml(
        "lebai_lm3_moveit_config", "config/ompl_planning.yaml"
    )
    ompl_planning_pipeline_config["move_group"].update(ompl_planning_yaml)

    # Trajectory Execution Functionality
    moveit_simple_controllers_yaml = load_yaml(
        "lebai_lm3_moveit_config", "config/lm3_controllers.yaml"
    )
    moveit_controllers = {
        "moveit_simple_controller_manager": moveit_simple_controllers_yaml,
        "moveit_controller_manager": (
            "moveit_simple_controller_manager/MoveItSimpleControllerManager"
        ),
    }

    trajectory_execution = {
        "moveit_manage_controllers": True,
        "trajectory_execution.allowed_execution_duration_scaling": 1.25,
        "trajectory_execution.allowed_goal_duration_margin": 5.0,
        "trajectory_execution.allowed_start_tolerance": 0.01,
    }

    planning_scene_monitor_parameters = {
        "publish_planning_scene": True,
        "publish_geometry_updates": True,
        "publish_state_updates": True,
        "publish_transforms_updates": True,
    }

    # # RViz
    # tutorial_mode = LaunchConfiguration("rviz_tutorial")
    rviz_base = os.path.join(get_package_share_directory("lebai_lm3_moveit_config"), "launch")
    rviz_full_config = os.path.join(rviz_base, "moveit.rviz")
    # rviz_empty_config = os.path.join(rviz_base, "moveit_empty.rviz")
    # rviz_node_tutorial = Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     name="rviz2",
    #     output="log",
    #     arguments=["-d", rviz_empty_config],
    #     parameters=[
    #         robot_description,
    #         robot_description_semantic,
    #         ompl_planning_pipeline_config,
    #         kinematics_yaml,
    #     ],
    #     condition=IfCondition(tutorial_mode),
    # )
    gripper_nodes = moveit_nodes(
        gripper_robot_description,
        gripper_robot_description_semantic,
        robot_description_planning,
        robot_ip,
        simulator,
        namespace,
        "lm3_with_gripper.xacro",
        IfCondition(has_gripper),
        gripper_joint_state_remappings,
        kinematics_yaml,
        ompl_planning_pipeline_config,
        trajectory_execution,
        moveit_controllers,
        planning_scene_monitor_parameters,
        rviz_full_config,
    )
    arm_nodes = moveit_nodes(
        arm_robot_description,
        arm_robot_description_semantic,
        robot_description_planning,
        robot_ip,
        simulator,
        namespace,
        "lm3.xacro",
        UnlessCondition(has_gripper),
        arm_joint_state_remappings,
        kinematics_yaml,
        ompl_planning_pipeline_config,
        trajectory_execution,
        moveit_controllers,
        planning_scene_monitor_parameters,
        rviz_full_config,
    )

    # Static TF
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        namespace=namespace,
        output="log",
        arguments=["0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "world", "base_link"],
    )

    return LaunchDescription(
        [
            robot_ip_arg,
            simulator_arg,
            namespace_arg,
            has_gripper_arg,
            static_tf,
            *gripper_nodes,
            *arm_nodes,
        ]
    )
