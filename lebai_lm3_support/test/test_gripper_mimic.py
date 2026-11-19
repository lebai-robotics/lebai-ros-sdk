import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import pytest


SOURCE_JOINT = "gripper_r_joint1"
STROKE = math.pi / 3


@pytest.fixture(scope="module")
def gripper_model():
    xacro_file = Path(__file__).resolve().parents[1] / "urdf" / "lm3_with_gripper.xacro"
    return ET.fromstring(subprocess.check_output(["xacro", str(xacro_file)]))


@pytest.fixture(scope="module")
def joints(gripper_model):
    return {joint.attrib["name"]: joint for joint in gripper_model.findall("joint")}


def test_gripper_has_one_independent_movable_joint(joints):
    independent = {
        name
        for name, joint in joints.items()
        if name.startswith("gripper_")
        and joint.attrib["type"] != "fixed"
        and joint.find("mimic") is None
    }
    assert independent == {SOURCE_JOINT}


def test_source_joint_matches_driver_range(joints):
    source = joints[SOURCE_JOINT]
    assert source.attrib["type"] == "revolute"
    limit = source.find("limit")
    assert limit is not None
    assert float(limit.attrib["lower"]) == pytest.approx(0.0)
    assert float(limit.attrib["upper"]) == pytest.approx(STROKE)


@pytest.mark.parametrize(
    "name,multiplier,lower,upper",
    [
        ("gripper_r_joint2", -1, -STROKE, 0),
        ("gripper_r_joint_finger", -1, -STROKE, 0),
        ("gripper_r_link_finger_end_connection_joint", 1, 0, STROKE),
        ("gripper_l_joint1", 1, 0, STROKE),
        ("gripper_l_joint2", -1, -STROKE, 0),
        ("gripper_l_joint_finger", -1, -STROKE, 0),
        ("gripper_l_link_finger_end_connection_joint", 1, 0, STROKE),
        ("gripper_tip_midpoint_arm_joint", 1, -math.pi, math.pi),
        ("gripper_tip_midpoint_counterarm_joint", -2, -math.pi, math.pi),
        ("gripper_joint_tip", 1, -math.pi, math.pi),
    ],
)
def test_mimic_joint_follows_source_with_humble_limits(joints, name, multiplier, lower, upper):
    assert name in joints
    joint = joints[name]
    assert joint.attrib["type"] == "revolute"
    mimic = joint.find("mimic")
    assert mimic is not None
    assert mimic.attrib["joint"] == SOURCE_JOINT
    assert float(mimic.attrib["multiplier"]) == multiplier
    assert float(mimic.attrib.get("offset", "0")) == 0
    limit = joint.find("limit")
    assert limit is not None
    assert float(limit.attrib["lower"]) == pytest.approx(lower)
    assert float(limit.attrib["upper"]) == pytest.approx(upper)


@pytest.mark.parametrize("side", ["r", "l"])
def test_link1_end_connection_is_fixed_to_link1(joints, side):
    link = f"gripper_{side}_link1"
    end = f"{link}_end_connection"
    name = f"{end}_joint"
    assert name in joints
    joint = joints[name]
    assert joint.attrib["type"] == "fixed"
    assert joint.find("mimic") is None
    assert joint.find("parent").attrib["link"] == link
    assert joint.find("child").attrib["link"] == end


def test_all_mimic_targets_exist(joints):
    for name, joint in joints.items():
        mimic = joint.find("mimic")
        if mimic is not None:
            assert mimic.attrib["joint"] in joints, name


def test_tip_is_connected_through_virtual_midpoint_chain(gripper_model, joints):
    links = {link.attrib["name"] for link in gripper_model.findall("link")}
    chain = [
        ("gripper_tip_midpoint_arm_joint", "gripper_base_link", "gripper_tip_midpoint_arm"),
        ("gripper_tip_midpoint_counterarm_joint", "gripper_tip_midpoint_arm", "gripper_tip_midpoint_counterarm"),
        ("gripper_joint_tip", "gripper_tip_midpoint_counterarm", "gripper_tip"),
    ]
    for name, parent, child in chain:
        assert name in joints
        assert parent in links
        assert child in links
        assert joints[name].find("parent").attrib["link"] == parent
        assert joints[name].find("child").attrib["link"] == child
