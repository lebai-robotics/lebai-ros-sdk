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

from pathlib import Path

import pytest
import yaml


PACKAGE_DIR = Path(__file__).resolve().parents[1]
RVIZ_CONFIG = PACKAGE_DIR / "rviz" / "view.rviz"
GRIPPER_RVIZ_CONFIG = PACKAGE_DIR / "rviz" / "gripper.rviz"
DISPLAY_GRIPPER_LAUNCH = PACKAGE_DIR / "launch" / "display_gripper.launch"
DISPLAY_GRIPPER_PY = PACKAGE_DIR / "launch" / "display_gripper.py"


def test_rviz_robot_model_uses_relative_description_topic():
    config = yaml.safe_load(RVIZ_CONFIG.read_text())
    displays = config["Visualization Manager"]["Displays"]

    robot_model = _display(displays, "rviz_default_plugins/RobotModel")
    description_topic = robot_model["Description Topic"]

    assert description_topic["Value"] == "robot_description"
    assert description_topic["Durability Policy"] == "Transient Local"


def test_rviz_fixed_frame_matches_standalone_arm_root():
    config = yaml.safe_load(RVIZ_CONFIG.read_text())
    global_options = config["Visualization Manager"]["Global Options"]

    assert global_options["Fixed Frame"] == "base_link"


def test_rviz_config_does_not_require_moveit_display_robot_state():
    config = yaml.safe_load(RVIZ_CONFIG.read_text())
    displays = config["Visualization Manager"]["Displays"]

    assert not any(
        display.get("Class") == "moveit_rviz_plugin/RobotState"
        for display in displays
    )


def test_gripper_rviz_uses_relative_description_topic_for_display_launch():
    config = yaml.safe_load(GRIPPER_RVIZ_CONFIG.read_text())
    displays = config["Visualization Manager"]["Displays"]

    robot_model = _display(displays, "rviz_default_plugins/RobotModel")
    description_topic = robot_model["Description Topic"]

    assert description_topic["Value"] == "robot_description"
    assert description_topic["Durability Policy"] == "Transient Local"


def test_gripper_rviz_fixed_frame_matches_standalone_gripper_root():
    config = yaml.safe_load(GRIPPER_RVIZ_CONFIG.read_text())
    global_options = config["Visualization Manager"]["Global Options"]

    assert global_options["Fixed Frame"] == "gripper_base_link"


@pytest.mark.parametrize(
    "launch_path",
    [DISPLAY_GRIPPER_LAUNCH, DISPLAY_GRIPPER_PY],
)
def test_gripper_display_launch_defaults_to_gripper_rviz_config(launch_path):
    launch_source = launch_path.read_text()

    assert "rviz/gripper.rviz" in launch_source


def _display(displays, class_name):
    matches = [
        display
        for display in displays
        if display.get("Class") == class_name
    ]
    assert len(matches) == 1
    return matches[0]
