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

from importlib.util import module_from_spec, spec_from_file_location
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from launch import LaunchContext
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitution import Substitution
from launch.utilities import perform_substitutions
from launch_ros.actions import Node
import pytest
import yaml


PACKAGE_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PACKAGE_DIR.parent
PUBLIC_LAUNCHES = ("lm3.launch.py", "lm3_l1.launch.py")
INTEGRATION_TEST_PATH = PACKAGE_DIR / "test" / "test_namespaced_stack_integration.py"


def _load_launch_description(launch_name):
    launch_path = PACKAGE_DIR / "launch" / launch_name
    module_name = "_namespace_contract_" + launch_name.replace(".", "_")
    spec = spec_from_file_location(module_name, launch_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(sys, "dont_write_bytecode", True)
        spec.loader.exec_module(module)
        monkeypatch.setattr(
            module,
            "get_package_share_directory",
            lambda package_name: str({
                "lebai_lm3_moveit_config": PACKAGE_DIR,
                "lebai_lm3_support": REPO_DIR / "lebai_lm3_support",
            }[package_name]),
        )
        with TemporaryDirectory() as log_dir:
            monkeypatch.setenv("ROS_LOG_DIR", log_dir)
            return module.generate_launch_description()


def _load_integration_test_module():
    spec = spec_from_file_location(
        "_namespaced_stack_integration_contract",
        INTEGRATION_TEST_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module", params=PUBLIC_LAUNCHES)
def public_launch(request):
    return request.param, _load_launch_description(request.param)


def _render(value, context=None):
    context = context or LaunchContext()
    if isinstance(value, Substitution):
        return value.perform(context)
    if isinstance(value, (list, tuple)):
        return perform_substitutions(context, list(value))
    return str(value)


def _namespace_context(namespace="robot_1"):
    context = LaunchContext()
    context.launch_configurations["namespace"] = namespace
    return context


def _nodes(launch_description):
    return [
        entity
        for entity in launch_description.entities
        if isinstance(entity, Node)
    ]


def _includes(launch_description):
    return [
        entity
        for entity in launch_description.entities
        if isinstance(entity, IncludeLaunchDescription)
    ]


def _remappings(node, context):
    return [
        (_render(source, context), _render(target, context))
        for source, target in node._Node__remappings
    ]


def _values_for_key(value, target_key):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == target_key:
                yield nested
            yield from _values_for_key(nested, target_key)
    elif isinstance(value, list):
        for nested in value:
            yield from _values_for_key(nested, target_key)


def test_public_launch_declares_one_default_namespace(public_launch):
    _launch_name, launch_description = public_launch
    namespace_arguments = [
        entity
        for entity in launch_description.entities
        if isinstance(entity, DeclareLaunchArgument)
        and entity.name == "namespace"
    ]

    assert len(namespace_arguments) == 1
    assert _render(namespace_arguments[0].default_value) == "lebai"


def test_public_launch_forwards_namespace_to_both_driver_includes(public_launch):
    _launch_name, launch_description = public_launch
    context = _namespace_context()
    driver_includes = _includes(launch_description)

    assert len(driver_includes) == 2
    for driver_include in driver_includes:
        arguments = dict(driver_include.launch_arguments)
        assert _render(arguments["namespace"], context) == "robot_1"


def test_public_launch_applies_namespace_to_every_node(public_launch):
    _launch_name, launch_description = public_launch
    context = _namespace_context()
    nodes = _nodes(launch_description)

    assert [node.node_package for node in nodes].count("moveit_ros_move_group") == 2
    assert [node.node_package for node in nodes].count("rviz2") == 2
    assert [node.node_package for node in nodes].count("robot_state_publisher") == 2
    assert [node.node_package for node in nodes].count("tf2_ros") == 1
    assert all(
        _render(node._Node__node_namespace, context) == "robot_1"
        for node in nodes
    )


def test_public_launch_uses_relative_joint_state_remaps(public_launch):
    _launch_name, launch_description = public_launch
    context = _namespace_context()
    remappings = [
        remapping
        for node in _nodes(launch_description)
        if node.node_package in {
            "moveit_ros_move_group",
            "robot_state_publisher",
            "rviz2",
        }
        for remapping in _remappings(node, context)
    ]

    assert remappings.count(("joint_states", "model/joint_states")) == 3
    assert remappings.count(("joint_states", "status/joint_states")) == 3
    assert all(not target.startswith("/") for _source, target in remappings)


def test_moveit_controller_action_names_are_relative_to_the_stack_namespace():
    controllers = yaml.safe_load(
        (PACKAGE_DIR / "config" / "lm3_controllers.yaml").read_text()
    )

    assert controllers["lebai_trajectory_controller"]["action_ns"] == (
        "follow_joint_trajectory"
    )
    assert controllers["lebai_gripper_controller"]["action_ns"] == "gripper_cmd"


def test_moveit_rviz_topics_are_relative_to_the_stack_namespace():
    config = yaml.safe_load(
        (PACKAGE_DIR / "launch" / "moveit.rviz").read_text()
    )
    trajectory_topics = list(_values_for_key(config, "Trajectory Topic"))
    planning_scene_topics = list(
        _values_for_key(config, "Planning Scene Topic")
    )
    robot_descriptions = list(_values_for_key(config, "Robot Description"))

    assert trajectory_topics == ["display_planned_path"] * 2
    assert planning_scene_topics == ["monitored_planning_scene"] * 2
    assert robot_descriptions
    assert set(robot_descriptions) == {"robot_description"}


def test_moveit_namespace_tests_are_registered_with_cmake():
    cmake = (PACKAGE_DIR / "CMakeLists.txt").read_text()

    assert "NAME test_namespaced_launch" in cmake
    assert "test/test_namespaced_launch.py" in cmake
    assert "NAME test_namespaced_stack_integration" in cmake
    assert "test/test_namespaced_stack_integration.py" in cmake


def test_integration_generator_skip_does_not_change_ros_domain(monkeypatch):
    monkeypatch.delenv("LEBAI_TEST_ROBOT_IP", raising=False)
    monkeypatch.setenv("ROS_DOMAIN_ID", "77")
    module = _load_integration_test_module()

    with pytest.raises(pytest.skip.Exception, match="LEBAI_TEST_ROBOT_IP"):
        module.generate_test_description()

    assert os.environ["ROS_DOMAIN_ID"] == "77"


def test_integration_generator_sets_domain_before_building_stacks(monkeypatch):
    monkeypatch.setenv("LEBAI_TEST_ROBOT_IP", "127.0.0.1")
    monkeypatch.setenv("ROS_DOMAIN_ID", "77")
    module = _load_integration_test_module()
    monkeypatch.setattr(module.os, "getpid", lambda: 461)
    observed_domains = []

    def package_share_path(_package_name):
        observed_domains.append(os.environ.get("ROS_DOMAIN_ID"))
        return PACKAGE_DIR

    monkeypatch.setattr(module, "get_package_share_path", package_share_path)

    launch_description = module.generate_test_description()

    assert launch_description is not None
    assert observed_domains == ["2"]
    assert os.environ["ROS_DOMAIN_ID"] == "2"
    assert 1 <= int(os.environ["ROS_DOMAIN_ID"]) <= 230
