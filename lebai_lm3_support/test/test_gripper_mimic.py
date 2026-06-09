from pathlib import Path
import xml.etree.ElementTree as ET


PACKAGE_DIR = Path(__file__).resolve().parents[1]
GRIPPER_MACRO = PACKAGE_DIR / "urdf" / "gripper_macro.xacro"


def test_gripper_has_one_independent_joint_and_five_mimic_joints():
    root = ET.parse(GRIPPER_MACRO).getroot()
    joints = {
        joint.attrib["name"]: joint
        for joint in root.findall(".//joint")
        if "gripper_" in joint.attrib["name"]
    }

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
        mimic = joints[joint_name].find("mimic")
        assert mimic is not None
        assert mimic.attrib == {
            "joint": source_joint,
            "multiplier": multiplier,
            "offset": "0.0",
        }


def test_gripper_joint_limits_match_zero_to_sixty_degree_motion():
    root = ET.parse(GRIPPER_MACRO).getroot()
    joints = {
        joint.attrib["name"]: joint
        for joint in root.findall(".//joint")
        if "gripper_" in joint.attrib["name"]
    }

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
