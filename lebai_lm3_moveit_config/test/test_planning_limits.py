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
from pathlib import Path
from unittest.mock import patch
import sys

from launch import LaunchContext
from launch.utilities import perform_substitutions
from launch_ros.actions import Node
from launch_ros.utilities import evaluate_parameters
import pytest
import yaml


PACKAGE_DIR = Path(__file__).resolve().parents[1]
ARM_JOINT_NAMES = [f"joint_{index}" for index in range(1, 7)]
EXPECTED_ARM_LIMIT = {
    "has_velocity_limits": True,
    "max_velocity": 3.0,
    "has_acceleration_limits": True,
    "max_acceleration": 6.0,
}
EXPECTED_GRIPPER_LIMIT = {
    "has_velocity_limits": True,
    "max_velocity": 1.0,
    "has_acceleration_limits": False,
    "max_acceleration": 1.0,
}


def test_planning_limits_are_conservative_and_complete():
    config = yaml.safe_load(
        (PACKAGE_DIR / "config" / "joint_limits.yaml").read_text()
    )

    assert config["default_velocity_scaling_factor"] == 0.2
    assert config["default_acceleration_scaling_factor"] == 0.2
    for joint_name in ARM_JOINT_NAMES:
        assert config["joint_limits"][joint_name] == EXPECTED_ARM_LIMIT
    assert config["joint_limits"]["gripper_r_joint1"] == EXPECTED_GRIPPER_LIMIT


@pytest.mark.parametrize("launch_name", ["lm3.launch.py", "lm3_l1.launch.py"])
def test_both_move_group_variants_receive_planning_limits(launch_name, monkeypatch):
    module = _load_launch_module(PACKAGE_DIR / "launch" / launch_name)
    joint_limits = {
        "default_velocity_scaling_factor": 0.2,
        "default_acceleration_scaling_factor": 0.2,
        "joint_limits": {"joint_1": EXPECTED_ARM_LIMIT},
    }

    def fake_load_yaml(_package_name, file_path):
        if file_path == "config/joint_limits.yaml":
            return joint_limits
        return {}

    monkeypatch.setattr(module, "load_yaml", fake_load_yaml)
    monkeypatch.setattr(
        module,
        "moveit_robot_description",
        lambda *_args: (
            {"robot_description": "urdf"},
            {"robot_description_semantic": "srdf"},
        ),
    )
    monkeypatch.setattr(
        module,
        "get_package_share_directory",
        lambda _package_name: str(PACKAGE_DIR),
    )

    description = module.generate_launch_description()
    context = LaunchContext()
    move_group_nodes = [
        entity
        for entity in description.entities
        if isinstance(entity, Node)
        and _node_package(entity, context) == "moveit_ros_move_group"
    ]

    assert len(move_group_nodes) == 2
    expected = _flatten_parameters({"robot_description_planning": joint_limits})
    for node in move_group_nodes:
        parameters = evaluate_parameters(context, node._Node__parameters)
        assert expected in parameters


def _load_launch_module(launch_path):
    module_name = "_planning_limits_" + launch_path.stem.replace(".", "_")
    spec = spec_from_file_location(module_name, launch_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    with patch.object(sys, "dont_write_bytecode", True):
        spec.loader.exec_module(module)
    return module


def _node_package(node, context):
    package = node._Node__package
    if isinstance(package, str):
        return package
    return perform_substitutions(context, package)


def _flatten_parameters(values, prefix=""):
    flattened = {}
    for name, value in values.items():
        qualified_name = prefix + name
        if isinstance(value, dict):
            flattened.update(
                _flatten_parameters(value, prefix=qualified_name + ".")
            )
        else:
            flattened[qualified_name] = value
    return flattened
