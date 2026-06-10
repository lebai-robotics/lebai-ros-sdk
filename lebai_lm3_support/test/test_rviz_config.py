from pathlib import Path

import yaml


PACKAGE_DIR = Path(__file__).resolve().parents[1]
RVIZ_CONFIG = PACKAGE_DIR / "rviz" / "view.rviz"


def test_rviz_robot_model_uses_namespaced_driver_description_topic():
    config = yaml.safe_load(RVIZ_CONFIG.read_text())
    displays = config["Visualization Manager"]["Displays"]

    robot_model = _display(displays, "rviz_default_plugins/RobotModel")
    description_topic = robot_model["Description Topic"]

    assert description_topic["Value"] == "/lebai/robot_description"
    assert description_topic["Durability Policy"] == "Transient Local"


def test_rviz_config_does_not_require_moveit_display_robot_state():
    config = yaml.safe_load(RVIZ_CONFIG.read_text())
    displays = config["Visualization Manager"]["Displays"]

    assert not any(
        display.get("Class") == "moveit_rviz_plugin/RobotState"
        for display in displays
    )


def _display(displays, class_name):
    matches = [
        display
        for display in displays
        if display.get("Class") == class_name
    ]
    assert len(matches) == 1
    return matches[0]
