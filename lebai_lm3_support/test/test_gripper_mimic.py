from pathlib import Path
import xml.etree.ElementTree as ET


PACKAGE_DIR = Path(__file__).resolve().parents[1]
GRIPPER_MACRO = PACKAGE_DIR / "urdf" / "gripper_macro.xacro"


def _gripper_joints(root):
    return {
        joint.attrib["name"]: joint
        for joint in root.findall(".//joint")
        if "gripper_" in joint.attrib["name"]
    }


def _assert_mimic(joint, source_joint, multiplier):
    mimic = joint.find("mimic")
    assert mimic is not None
    assert mimic.attrib == {
        "joint": source_joint,
        "multiplier": multiplier,
        "offset": "0.0",
    }


def test_gripper_physical_joints_mimic_single_source_joint():
    root = ET.parse(GRIPPER_MACRO).getroot()
    joints = _gripper_joints(root)

    source_joint = "${prefix}gripper_r_joint1"
    expected_mimic_multipliers = {
        "${prefix}gripper_r_joint2": "-1.0",
        "${prefix}gripper_r_joint_finger": "-1.0",
        "${prefix}gripper_l_joint1": "1.0",
        "${prefix}gripper_l_joint2": "-1.0",
        "${prefix}gripper_l_joint_finger": "-1.0",
    }

    assert joints[source_joint].find("mimic") is None

    for joint_name, multiplier in expected_mimic_multipliers.items():
        _assert_mimic(joints[joint_name], source_joint, multiplier)


def test_gripper_link1_end_connections_remain_fixed():
    root = ET.parse(GRIPPER_MACRO).getroot()
    joints = _gripper_joints(root)

    expected_joints = {
        "${prefix}gripper_l_link1_end_connection_joint": (
            "${prefix}gripper_l_link1",
            "${prefix}gripper_l_link1_end_connection",
        ),
        "${prefix}gripper_r_link1_end_connection_joint": (
            "${prefix}gripper_r_link1",
            "${prefix}gripper_r_link1_end_connection",
        ),
    }

    for joint_name, (parent, child) in expected_joints.items():
        joint = joints[joint_name]
        assert joint.attrib["type"] == "fixed"
        assert joint.find("parent").attrib["link"] == parent
        assert joint.find("child").attrib["link"] == child


def test_gripper_finger_end_connection_joints_mimic_link1_end_connections():
    root = ET.parse(GRIPPER_MACRO).getroot()
    links = {link.attrib["name"] for link in root.findall(".//link")}
    joints = _gripper_joints(root)

    source_joint = "${prefix}gripper_r_joint1"
    expected_joints = {
        "${prefix}gripper_l_link_finger_end_connection_joint": (
            "${prefix}gripper_l_link_finger",
            "${prefix}gripper_l_link_finger_end_connection",
        ),
        "${prefix}gripper_r_link_finger_end_connection_joint": (
            "${prefix}gripper_r_link_finger",
            "${prefix}gripper_r_link_finger_end_connection",
        ),
    }

    for joint_name, (parent, child) in expected_joints.items():
        assert child in links
        joint = joints[joint_name]
        assert joint.attrib["type"] == "revolute"
        assert joint.find("parent").attrib["link"] == parent
        assert joint.find("child").attrib["link"] == child
        assert joint.find("origin").attrib == {
            "xyz": "-0.0135 -0.02 0.0",
            "rpy": "0.0 0.0 0.0",
        }
        assert joint.find("axis").attrib["xyz"] == "0 0 1"
        limit = joint.find("limit")
        assert limit.attrib["lower"] == "0.0"
        assert limit.attrib["upper"] == "${PI/3.0}"
        _assert_mimic(joint, source_joint, "1.0")


def test_gripper_joint_limits_match_zero_to_sixty_degree_motion():
    root = ET.parse(GRIPPER_MACRO).getroot()
    joints = _gripper_joints(root)

    expected_limits = {
        "${prefix}gripper_r_joint1": ("0.0", "${PI/3.0}"),
        "${prefix}gripper_r_joint2": ("${-PI/3.0}", "0.0"),
        "${prefix}gripper_r_joint_finger": ("${-PI/3.0}", "0.0"),
        "${prefix}gripper_l_joint1": ("0.0", "${PI/3.0}"),
        "${prefix}gripper_l_joint2": ("${-PI/3.0}", "0.0"),
        "${prefix}gripper_l_joint_finger": ("${-PI/3.0}", "0.0"),
    }

    for joint_name, (lower, upper) in expected_limits.items():
        limit = joints[joint_name].find("limit")
        assert limit.attrib["lower"] == lower
        assert limit.attrib["upper"] == upper


def test_gripper_tip_uses_virtual_midpoint_chain():
    root = ET.parse(GRIPPER_MACRO).getroot()
    links = {link.attrib["name"] for link in root.findall(".//link")}
    joints = _gripper_joints(root)

    assert "${prefix}gripper_tip_midpoint_arm" in links
    assert "${prefix}gripper_tip_midpoint_counterarm" in links
    assert "${prefix}gripper_tip" in links

    source_joint = "${prefix}gripper_r_joint1"
    arm_joint = joints["${prefix}gripper_tip_midpoint_arm_joint"]
    counterarm_joint = joints["${prefix}gripper_tip_midpoint_counterarm_joint"]
    tip_joint = joints["${prefix}gripper_joint_tip"]

    assert arm_joint.find("parent").attrib["link"] == "${prefix}gripper_base_link"
    assert arm_joint.find("child").attrib["link"] == "${prefix}gripper_tip_midpoint_arm"
    assert arm_joint.find("origin").attrib == {
        "xyz": "0.0 0.0 0.1056",
        "rpy": "0.0 0.0 0.0",
    }
    assert arm_joint.find("axis").attrib["xyz"] == "0 1 0"
    _assert_mimic(arm_joint, source_joint, "1.0")

    assert counterarm_joint.find("parent").attrib["link"] == "${prefix}gripper_tip_midpoint_arm"
    assert counterarm_joint.find("child").attrib["link"] == "${prefix}gripper_tip_midpoint_counterarm"
    assert counterarm_joint.find("origin").attrib == {
        "xyz": "0.0 0.0 0.0265",
        "rpy": "0.0 0.0 0.0",
    }
    assert counterarm_joint.find("axis").attrib["xyz"] == "0 1 0"
    _assert_mimic(counterarm_joint, source_joint, "-2.0")

    assert tip_joint.find("parent").attrib["link"] == "${prefix}gripper_tip_midpoint_counterarm"
    assert tip_joint.find("child").attrib["link"] == "${prefix}gripper_tip"
    assert tip_joint.find("origin").attrib == {
        "xyz": "0.0 0.0 0.0265",
        "rpy": "0.0 0.0 0.0",
    }
    assert tip_joint.find("axis").attrib["xyz"] == "0 1 0"
    _assert_mimic(tip_joint, source_joint, "1.0")
