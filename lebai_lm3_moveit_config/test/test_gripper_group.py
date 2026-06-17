from pathlib import Path
import os
import xml.etree.ElementTree as ET

import pytest
import yaml
import xacro


PACKAGE_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = PACKAGE_DIR.parent
SUPPORT_DIR = REPO_DIR / "lebai_lm3_support"

ROBOT_CONFIGS = [
    (
        PACKAGE_DIR / "config" / "lebai_lm3.srdf",
        SUPPORT_DIR / "urdf" / "lm3_with_gripper.xacro",
    ),
    (
        PACKAGE_DIR / "config" / "lebai_lm3_l1.srdf",
        SUPPORT_DIR / "urdf" / "lm3_l1_with_gripper.xacro",
    ),
]


@pytest.mark.parametrize(("srdf_path", "xacro_path"), ROBOT_CONFIGS)
def test_gripper_group_references_existing_active_joint(srdf_path, xacro_path, tmp_path):
    srdf = ET.parse(srdf_path).getroot()
    robot_joints = _robot_joint_names(xacro_path, tmp_path)

    gripper_group = _required_group(srdf, "gripper")
    group_joints = [
        joint.attrib["name"]
        for joint in gripper_group.findall("joint")
    ]

    assert group_joints == ["gripper_r_joint1"]
    assert set(group_joints).issubset(robot_joints)


@pytest.mark.parametrize(("srdf_path", "_xacro_path"), ROBOT_CONFIGS)
def test_gripper_group_has_named_open_and_closed_states(srdf_path, _xacro_path):
    srdf = ET.parse(srdf_path).getroot()

    states = {
        state.attrib["name"]: state
        for state in srdf.findall("group_state")
        if state.attrib.get("group") == "gripper"
    }

    assert set(states) == {"open", "closed"}
    assert _single_joint_value(states["open"]) == ("gripper_r_joint1", "0.0")
    assert _single_joint_value(states["closed"]) == ("gripper_r_joint1", "1.0471975512")


@pytest.mark.parametrize(("srdf_path", "_xacro_path"), ROBOT_CONFIGS)
def test_gripper_group_is_registered_as_manipulator_end_effector(srdf_path, _xacro_path):
    srdf = ET.parse(srdf_path).getroot()

    end_effectors = [
        end_effector.attrib
        for end_effector in srdf.findall("end_effector")
        if end_effector.attrib.get("name") == "gripper"
    ]

    assert end_effectors == [{
        "name": "gripper",
        "parent_link": "tool0",
        "group": "gripper",
        "parent_group": "manipulator",
    }]


def test_moveit_launches_load_gripper_robot_models():
    lm3_launch = (PACKAGE_DIR / "launch" / "lm3.launch.py").read_text()
    lm3_l1_launch = (PACKAGE_DIR / "launch" / "lm3_l1.launch.py").read_text()

    assert "lm3_with_gripper.xacro" in lm3_launch
    assert "lm3_l1_with_gripper.xacro" in lm3_l1_launch
    assert "driver.launch.py" in lm3_launch
    assert "driver.launch.py" in lm3_l1_launch
    assert "'publish_robot_description': \"false\"" in lm3_launch
    assert "'publish_robot_description': \"false\"" in lm3_l1_launch
    assert "'robot_model': \"lm3_with_gripper.xacro\"" in lm3_launch
    assert "'robot_model': \"lm3_l1_with_gripper.xacro\"" in lm3_l1_launch


def test_moveit_config_declares_driver_launch_dependency():
    package_manifest = ET.parse(PACKAGE_DIR / "package.xml").getroot()
    exec_dependencies = [
        dependency.text
        for dependency in package_manifest.findall("exec_depend")
    ]

    assert "lebai_driver" in exec_dependencies


def test_joint_limits_include_active_gripper_joint():
    joint_limits = yaml.safe_load(
        (PACKAGE_DIR / "config" / "joint_limits.yaml").read_text()
    )["joint_limits"]

    assert joint_limits["gripper_r_joint1"] == {
        "has_velocity_limits": True,
        "max_velocity": 1.0,
        "has_acceleration_limits": False,
        "max_acceleration": 1.0,
    }


def _required_group(srdf, name):
    groups = [
        group
        for group in srdf.findall("group")
        if group.attrib.get("name") == name
    ]
    assert len(groups) == 1
    return groups[0]


def _single_joint_value(group_state):
    joints = group_state.findall("joint")
    assert len(joints) == 1
    joint = joints[0]
    return joint.attrib["name"], joint.attrib["value"]


def _robot_joint_names(xacro_path, tmp_path):
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
    robot = ET.fromstring(document.toxml())
    return {
        joint.attrib["name"]
        for joint in robot.findall("joint")
    }


def _write_package_index(prefix_path):
    resource_index = (
        prefix_path / "share" / "ament_index" / "resource_index" / "packages"
    )
    resource_index.mkdir(parents=True)
    packages = {
        "lebai_lm3_support": SUPPORT_DIR,
        "lebai_resources": REPO_DIR / "lebai_resources",
    }

    for package_name, package_dir in packages.items():
        (resource_index / package_name).write_text("")
        share_dir = prefix_path / "share" / package_name
        share_dir.mkdir(parents=True)
        for subdir in ("urdf", "meshes", "config", "rviz", "launch"):
            source = package_dir / subdir
            if source.exists():
                (share_dir / subdir).symlink_to(source, target_is_directory=True)
