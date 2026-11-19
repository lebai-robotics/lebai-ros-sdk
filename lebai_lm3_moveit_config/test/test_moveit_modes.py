"""Check the two supported LM3 configurations without starting a ROS master."""

import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import pytest
import roslaunch
import yaml


PACKAGE = Path(__file__).resolve().parents[1]
CONFIG = PACKAGE / "config"
LAUNCH = PACKAGE / "launch"
URDF = PACKAGE.parent / "lebai_lm3_support" / "urdf"
ARM = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]
FINGER = "gripper_r_joint1"
MODES = [
    (False, "lm3.xacro", "lebai_lm3_no_gripper.srdf",
     "/lebai/status/joint_states", "controllers_arm_only.yaml"),
    (True, "lm3_with_gripper.xacro", "lebai_lm3.srdf",
     "/lebai/model/joint_states", "controllers.yaml"),
]


def expand(model):
    return ET.fromstring(subprocess.check_output(["xacro", str(URDF / model)]))


@pytest.mark.parametrize("has_gripper,model,semantic,topic,controllers", MODES)
def test_semantic_model(has_gripper, model, semantic, topic, controllers):
    assert (CONFIG / semantic).is_file()
    srdf = ET.parse(str(CONFIG / semantic)).getroot()
    urdf = expand(model)
    assert srdf.get("name") == urdf.get("name")
    links = {link.get("name") for link in urdf.findall("link")}
    active = {joint.get("name") for joint in urdf.findall("joint")
              if joint.get("type") != "fixed" and joint.find("mimic") is None}
    assert active == set(ARM + ([FINGER] if has_gripper else []))
    assert {joint.get("name") for joint in srdf.iter("joint")} <= active
    groups = {group.get("name") for group in srdf.findall("group")}
    assert groups == ({"manipulator", "gripper"} if has_gripper else {"manipulator"})
    chain = srdf.find("group[@name='manipulator']/chain")
    assert chain.attrib == {"base_link": "base_link", "tip_link": "tool0"}
    child_joints = {j.find("child").get("link"): j for j in urdf.findall("joint")}
    chain_joints = []
    link = chain.get("tip_link")
    while link != chain.get("base_link"):
        joint = child_joints[link]
        if joint.get("name") in active:
            chain_joints.append(joint.get("name"))
        link = joint.find("parent").get("link")
    assert chain_joints[::-1] == ARM
    collisions = [(c.get("link1"), c.get("link2")) for c in srdf.findall("disable_collisions")]
    assert all(a in links and b in links for a, b in collisions)
    assert any("gripper" in a or "gripper" in b for a, b in collisions) == has_gripper
    states = {s.get("name"): s for s in srdf.findall("group_state[@group='gripper']")}
    assert set(states) == ({"open", "closed"} if has_gripper else set())
    effectors = [e.attrib for e in srdf.findall("end_effector")]
    assert effectors == ([dict(name="gripper", group="gripper", parent_link="tool0",
                               parent_group="manipulator")] if has_gripper else [])
    if has_gripper:
        assert [j.get("name") for j in srdf.findall("group[@name='gripper']/joint")] == [FINGER]
        for state, position in [("open", math.pi / 3), ("closed", 0.0)]:
            joints = states[state].findall("joint")
            assert [j.get("name") for j in joints] == [FINGER]
            assert float(joints[0].get("value")) == pytest.approx(position)


@pytest.mark.parametrize("has_gripper,model,semantic,topic,controllers", MODES)
def test_controller_endpoints(has_gripper, model, semantic, topic, controllers):
    assert (CONFIG / controllers).is_file()
    specs = yaml.safe_load((CONFIG / controllers).read_text())["controller_list"]
    endpoints = [(s["name"], s["action_ns"], s["type"], s["joints"]) for s in specs]
    expected = [("/lebai_trajectory_controller", "", "FollowJointTrajectory", ARM)]
    if has_gripper:
        expected.append(("/lebai_gripper_controller", "gripper_cmd", "GripperCommand", [FINGER]))
    assert endpoints == expected


def launch_config(*args):
    entry = LAUNCH / "lm3.launch"
    assert entry.is_file()
    return roslaunch.config.load_config_default([(str(entry), list(args))], None)


def test_move_group_uses_driver_execution_window():
    params = launch_config("launch_driver:=false", "use_rviz:=false").params
    prefix = "/move_group/trajectory_execution/"
    assert params[prefix + "allowed_execution_duration_scaling"].value == 1.25
    assert params[prefix + "allowed_goal_duration_margin"].value == 5.0
    assert params[prefix + "allowed_start_tolerance"].value == 0.01


@pytest.mark.parametrize("has_gripper,model,semantic,topic,controllers", MODES)
def test_launch_selects_consistent_assets(has_gripper, model, semantic, topic, controllers):
    config = launch_config("has_gripper:=" + str(has_gripper).lower(),
                           "launch_driver:=false", "use_rviz:=false")
    params = {name: p.value for name, p in config.params.items()}
    assert ET.tostring(ET.fromstring(params["/robot_description"])) == ET.tostring(expand(model))
    assert ET.tostring(ET.fromstring(params["/robot_description_semantic"])) == ET.tostring(
        ET.parse(str(CONFIG / semantic)).getroot())
    assert params["/move_group/controller_list"] == yaml.safe_load(
        (CONFIG / controllers).read_text())["controller_list"]
    if has_gripper:
        limit = "/robot_description_planning/joint_limits/gripper_r_joint1/"
        assert params[limit + "has_velocity_limits"] is True
        assert params[limit + "max_velocity"] == 1.0
    assert {node.type for node in config.nodes} == {"robot_state_publisher", "move_group"}
    for node in config.nodes:
        assert dict(node.remap_args)["joint_states"] == topic


def test_default_launch_starts_driver_forwards_connection_and_selects_gripper():
    config = launch_config("robot_ip:=192.0.2.33", "simulator:=true")
    assert sorted(node.package for node in config.nodes) == [
        "lebai_driver", "moveit_ros_move_group", "robot_state_publisher", "rviz"]
    assert config.params["/lebai/lebai_driver/robot_ip"].value == "192.0.2.33"
    assert config.params["/lebai/lebai_driver/simulator"].value is True
    assert len(config.params["/move_group/controller_list"].value) == 2
    assert not (LAUNCH / "real_robot.launch").exists()
    assert not any("lm3_l1" in p.name.lower().replace("-", "_")
                   for folder in (CONFIG, LAUNCH) for p in folder.rglob("*"))
