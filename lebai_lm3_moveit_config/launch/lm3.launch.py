# Copyright 2022-2026 Shanghai Lebai Robotics Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import OpaqueFunction
from launch.actions import RegisterEventHandler
from launch.actions import SetLaunchConfiguration
from launch.event_handlers import OnProcessExit, OnShutdown
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from rclpy.validate_namespace import validate_namespace
import xacro


_MOVEIT_RVIZ_DISPLAY_CLASSES = {
    "moveit_rviz_plugin/MotionPlanning",
    "moveit_rviz_plugin/PlanningScene",
}
_GENERATED_RVIZ_CONFIG_KEY = "_lebai_moveit_rviz_config"


def _move_group_namespace(namespace):
    normalized_namespace = (
        namespace if namespace.startswith("/") else f"/{namespace}"
    )
    validate_namespace(normalized_namespace)
    return "" if normalized_namespace == "/" else normalized_namespace


def _set_move_group_namespace(value, namespace, found_classes):
    if isinstance(value, dict):
        display_class = value.get("Class")
        if display_class in _MOVEIT_RVIZ_DISPLAY_CLASSES:
            if "Move Group Namespace" not in value:
                raise ValueError(
                    f"RViz display {display_class!r} lacks "
                    "'Move Group Namespace'"
                )
            value["Move Group Namespace"] = namespace
            found_classes.add(display_class)

        for nested_value in value.values():
            _set_move_group_namespace(
                nested_value,
                namespace,
                found_classes,
            )
    elif isinstance(value, list):
        for nested_value in value:
            _set_move_group_namespace(
                nested_value,
                namespace,
                found_classes,
            )


def _prepare_rviz_config(context, rviz_config_path, rviz_nodes):
    temporary_path = None
    try:
        namespace = _move_group_namespace(
            LaunchConfiguration("namespace").perform(context)
        )
        with rviz_config_path.open("r", encoding="utf-8") as config_file:
            rviz_config = yaml.safe_load(config_file)

        if not isinstance(rviz_config, dict):
            raise ValueError("RViz config root must be a mapping")

        visualization_manager = rviz_config.get("Visualization Manager")
        if not isinstance(visualization_manager, dict):
            raise ValueError(
                "RViz config 'Visualization Manager' must be a mapping"
            )

        displays = visualization_manager.get("Displays")
        if not isinstance(displays, list):
            raise ValueError(
                "RViz config 'Visualization Manager.Displays' must be a list"
            )

        found_classes = set()
        _set_move_group_namespace(
            displays,
            namespace,
            found_classes,
        )
        missing_classes = _MOVEIT_RVIZ_DISPLAY_CLASSES - found_classes
        if missing_classes:
            missing_list = ", ".join(sorted(missing_classes))
            raise ValueError(f"RViz config is missing displays: {missing_list}")

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".rviz",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            yaml.safe_dump(
                rviz_config,
                temporary_file,
                sort_keys=False,
            )

        def remove_temporary_config(_event, _context):
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass

        return [
            SetLaunchConfiguration(
                _GENERATED_RVIZ_CONFIG_KEY,
                str(temporary_path),
            ),
            *[
                RegisterEventHandler(
                    OnProcessExit(
                        target_action=rviz_node,
                        on_exit=remove_temporary_config,
                    )
                )
                for rviz_node in rviz_nodes
            ],
            RegisterEventHandler(
                OnShutdown(on_shutdown=remove_temporary_config)
            ),
        ]
    except Exception as error:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass
        raise RuntimeError(
            f"Failed to prepare namespaced RViz config: {error}"
        ) from error


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
    rviz_base = Path(
        get_package_share_directory("lebai_lm3_moveit_config")
    ) / "launch"
    canonical_rviz_config = rviz_base / "moveit.rviz"
    rviz_full_config = LaunchConfiguration(_GENERATED_RVIZ_CONFIG_KEY)
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
    prepare_rviz_config = OpaqueFunction(
        function=_prepare_rviz_config,
        args=[
            canonical_rviz_config,
            [gripper_nodes[2], arm_nodes[2]],
        ],
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
            prepare_rviz_config,
            static_tf,
            *gripper_nodes,
            *arm_nodes,
        ]
    )
