from pathlib import Path
import os
import xml.etree.ElementTree as ET

import pytest
import xacro


REPOSITORY_DIR = Path(__file__).resolve().parents[2]
SUPPORT_DIR = REPOSITORY_DIR / "lebai_lm3_support"
EXPECTED_LIMITS = {
    "joint_1": (-12.57, 12.57, 3.49),
    "joint_2": (-4.71, 1.57, 3.49),
    "joint_3": (-3.14, 3.14, 3.49),
    "joint_4": (-12.57, 12.57, 3.49),
    "joint_5": (-12.57, 12.57, 3.49),
    "joint_6": (-12.57, 12.57, 3.49),
}
MODEL_JOINT_PREFIXES = {
    "lm3.xacro": ("",),
    "lm3_with_gripper.xacro": ("",),
    "lm3_l1.xacro": ("",),
    "lm3_l1_with_gripper.xacro": ("",),
    "two_lm3.xacro": ("robot1_", "robot2_"),
}


@pytest.mark.parametrize(
    ("model_name", "prefixes"),
    MODEL_JOINT_PREFIXES.items(),
)
def test_expanded_arm_limits_match_controller(model_name, prefixes, tmp_path):
    robot = _robot_from_xacro(SUPPORT_DIR / "urdf" / model_name, tmp_path)
    joints = {joint.attrib["name"]: joint for joint in robot.findall("joint")}
    expected_joint_names = {
        prefix + joint_name
        for prefix in prefixes
        for joint_name in EXPECTED_LIMITS
    }

    assert expected_joint_names.issubset(joints)
    for prefix in prefixes:
        for joint_name, expected in EXPECTED_LIMITS.items():
            joint = joints[prefix + joint_name]
            assert joint.attrib["type"] == "revolute"
            limit = joint.find("limit")
            assert limit is not None
            actual = tuple(
                float(limit.attrib[field])
                for field in ("lower", "upper", "velocity")
            )
            assert actual == pytest.approx(expected)


def test_lm3_variants_include_one_shared_arm_limits_definition():
    for macro_name in ("lm3_macro.xacro", "lm3_l1_macro.xacro"):
        macro = ET.parse(SUPPORT_DIR / "urdf" / macro_name).getroot()
        includes = [
            include.attrib["filename"]
            for include in macro.findall("{http://ros.org/wiki/xacro}include")
        ]

        assert includes.count(
            "$(find lebai_lm3_support)/urdf/lm3_joint_limits.xacro"
        ) == 1


def _robot_from_xacro(xacro_path, tmp_path):
    _write_package_index(tmp_path)
    previous_prefix_path = os.environ.get("AMENT_PREFIX_PATH")
    os.environ["AMENT_PREFIX_PATH"] = str(tmp_path)
    try:
        document = xacro.process_file(str(xacro_path))
    finally:
        if previous_prefix_path is None:
            os.environ.pop("AMENT_PREFIX_PATH", None)
        else:
            os.environ["AMENT_PREFIX_PATH"] = previous_prefix_path
    return ET.fromstring(document.toxml())


def _write_package_index(prefix_path):
    resource_index = (
        prefix_path / "share" / "ament_index" / "resource_index" / "packages"
    )
    resource_index.mkdir(parents=True)
    packages = {
        "lebai_lm3_support": SUPPORT_DIR,
        "lebai_resources": REPOSITORY_DIR / "lebai_resources",
    }

    for package_name, package_dir in packages.items():
        (resource_index / package_name).write_text("")
        share_dir = prefix_path / "share" / package_name
        share_dir.mkdir(parents=True)
        for subdir in ("urdf", "meshes", "config", "rviz", "launch"):
            source = package_dir / subdir
            if source.exists():
                (share_dir / subdir).symlink_to(source, target_is_directory=True)
