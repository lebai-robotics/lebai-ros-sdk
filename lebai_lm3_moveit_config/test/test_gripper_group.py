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
        True,
    ),
    (
        PACKAGE_DIR / "config" / "lebai_lm3_l1.srdf",
        SUPPORT_DIR / "urdf" / "lm3_l1_with_gripper.xacro",
        True,
    ),
    (
        PACKAGE_DIR / "config" / "lebai_lm3_no_gripper.srdf",
        SUPPORT_DIR / "urdf" / "lm3.xacro",
        False,
    ),
    (
        PACKAGE_DIR / "config" / "lebai_lm3_l1_no_gripper.srdf",
        SUPPORT_DIR / "urdf" / "lm3_l1.xacro",
        False,
    ),
]


@pytest.mark.parametrize(("srdf_path", "xacro_path", "has_gripper"), ROBOT_CONFIGS)
def test_srdf_groups_reference_existing_active_joints(srdf_path, xacro_path, has_gripper, tmp_path):
    srdf = ET.parse(srdf_path).getroot()
    robot_joints = _robot_joint_names(xacro_path, tmp_path)

    manipulator_group = _required_group(srdf, "manipulator")
    chain = manipulator_group.find("chain")
    assert chain is not None
    assert chain.attrib == {"base_link": "base_link", "tip_link": "tool0"}

    if not has_gripper:
        assert _find_group(srdf, "gripper") is None
        return

    gripper_group = _required_group(srdf, "gripper")
    group_joints = [
        joint.attrib["name"]
        for joint in gripper_group.findall("joint")
    ]

    assert group_joints == ["gripper_r_joint1"]
    assert set(group_joints).issubset(robot_joints)


@pytest.mark.parametrize(("srdf_path", "_xacro_path", "has_gripper"), ROBOT_CONFIGS)
def test_gripper_group_has_named_open_and_closed_states(srdf_path, _xacro_path, has_gripper):
    srdf = ET.parse(srdf_path).getroot()

    states = {
        state.attrib["name"]: state
        for state in srdf.findall("group_state")
        if state.attrib.get("group") == "gripper"
    }

    if not has_gripper:
        assert states == {}
        return

    assert set(states) == {"open", "closed"}
    assert _single_joint_value(states["open"]) == ("gripper_r_joint1", "1.0471975512")
    assert _single_joint_value(states["closed"]) == ("gripper_r_joint1", "0.0")


@pytest.mark.parametrize(("srdf_path", "_xacro_path", "has_gripper"), ROBOT_CONFIGS)
def test_gripper_group_is_registered_as_manipulator_end_effector(srdf_path, _xacro_path, has_gripper):
    srdf = ET.parse(srdf_path).getroot()

    end_effectors = [
        end_effector.attrib
        for end_effector in srdf.findall("end_effector")
        if end_effector.attrib.get("name") == "gripper"
    ]

    if not has_gripper:
        assert end_effectors == []
        return

    assert end_effectors == [{
        "name": "gripper",
        "parent_link": "tool0",
        "group": "gripper",
        "parent_group": "manipulator",
    }]


@pytest.mark.parametrize(("srdf_path", "_xacro_path", "has_gripper"), ROBOT_CONFIGS)
def test_gripper_mount_self_collisions_are_disabled_only_when_gripper_is_loaded(
    srdf_path,
    _xacro_path,
    has_gripper,
):
    srdf = ET.parse(srdf_path).getroot()
    disabled_pairs = _disabled_collision_pairs(srdf)
    gripper_pairs = {
        frozenset(("link_6", "tool0")),
        frozenset(("tool0", "gripper_base_link")),
        frozenset(("link_6", "gripper_base_link")),
    }

    if has_gripper:
        assert gripper_pairs.issubset(disabled_pairs)
    else:
        assert not any(
            "gripper" in link
            for pair in disabled_pairs
            for link in pair
        )


@pytest.mark.parametrize(("srdf_path", "xacro_path", "has_gripper"), ROBOT_CONFIGS)
def test_gripper_internal_collisions_are_disabled_only_when_gripper_is_loaded(
    srdf_path,
    xacro_path,
    has_gripper,
    tmp_path,
):
    srdf = ET.parse(srdf_path).getroot()
    disabled_pairs = _disabled_collision_pairs(srdf)

    if has_gripper:
        gripper_pairs = _all_pairs(_gripper_collision_links(xacro_path, tmp_path))
        assert gripper_pairs.issubset(disabled_pairs)
    else:
        assert not any(
            "gripper" in link
            for pair in disabled_pairs
            for link in pair
        )


def test_moveit_launches_select_robot_models_by_has_gripper_argument():
    lm3_launch = (PACKAGE_DIR / "launch" / "lm3.launch.py").read_text()
    lm3_l1_launch = (PACKAGE_DIR / "launch" / "lm3_l1.launch.py").read_text()

    assert "name='has_gripper'" in lm3_launch
    assert "name='has_gripper'" in lm3_l1_launch
    assert "IfCondition(has_gripper)" in lm3_launch
    assert "IfCondition(has_gripper)" in lm3_l1_launch
    assert "UnlessCondition(has_gripper)" in lm3_launch
    assert "UnlessCondition(has_gripper)" in lm3_l1_launch
    assert "lm3_with_gripper.xacro" in lm3_launch
    assert "lm3_l1_with_gripper.xacro" in lm3_l1_launch
    assert "lm3.xacro" in lm3_launch
    assert "lm3_l1.xacro" in lm3_l1_launch
    assert "lebai_lm3_no_gripper.srdf" in lm3_launch
    assert "lebai_lm3_l1_no_gripper.srdf" in lm3_l1_launch
    assert "driver.launch.py" in lm3_launch
    assert "driver.launch.py" in lm3_l1_launch
    assert "'publish_robot_description': \"false\"" in lm3_launch
    assert "'publish_robot_description': \"false\"" in lm3_l1_launch


def test_moveit_launches_forward_simulator_and_selects_joint_state_topic_by_gripper_mode():
    lm3_launch = (PACKAGE_DIR / "launch" / "lm3.launch.py").read_text()
    lm3_l1_launch = (PACKAGE_DIR / "launch" / "lm3_l1.launch.py").read_text()

    for launch_file in (lm3_launch, lm3_l1_launch):
        assert "name='simulator'" in launch_file
        assert "simulator = LaunchConfiguration('simulator')" in launch_file
        assert "'simulator': simulator" in launch_file
        assert (
            "gripper_joint_state_remappings = [\n"
            "        ('joint_states', '/lebai/model/joint_states'),\n"
            "    ]"
        ) in launch_file
        assert (
            "arm_joint_state_remappings = [\n"
            "        ('joint_states', '/lebai/status/joint_states'),\n"
            "    ]"
        ) in launch_file
        assert launch_file.count("remappings=joint_state_remappings") == 3


def test_moveit_config_declares_driver_launch_dependency():
    package_manifest = ET.parse(PACKAGE_DIR / "package.xml").getroot()
    exec_dependencies = [
        dependency.text
        for dependency in package_manifest.findall("exec_depend")
    ]

    assert "lebai_driver" in exec_dependencies


def test_moveit_controller_config_declares_arm_and_gripper_action_servers():
    controllers = yaml.safe_load(
        (PACKAGE_DIR / "config" / "lm3_controllers.yaml").read_text()
    )

    assert controllers["controller_names"] == [
        "lebai_trajectory_controller",
        "lebai_gripper_controller",
    ]
    assert controllers["lebai_trajectory_controller"] == {
        "action_ns": "",
        "type": "FollowJointTrajectory",
        "default": True,
        "joints": [
            "joint_1",
            "joint_2",
            "joint_3",
            "joint_4",
            "joint_5",
            "joint_6",
        ],
    }
    assert controllers["lebai_gripper_controller"] == {
        "action_ns": "gripper_cmd",
        "type": "GripperCommand",
        "default": True,
        "joints": ["gripper_r_joint1"],
    }


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
    group = _find_group(srdf, name)
    assert group is not None
    return group


def _find_group(srdf, name):
    groups = [
        group
        for group in srdf.findall("group")
        if group.attrib.get("name") == name
    ]
    if not groups:
        return None
    assert len(groups) == 1
    return groups[0]


def _disabled_collision_pairs(srdf):
    return {
        frozenset((
            entry.attrib["link1"],
            entry.attrib["link2"],
        ))
        for entry in srdf.findall("disable_collisions")
    }


def _single_joint_value(group_state):
    joints = group_state.findall("joint")
    assert len(joints) == 1
    joint = joints[0]
    return joint.attrib["name"], joint.attrib["value"]


def _robot_joint_names(xacro_path, tmp_path):
    robot = _robot_from_xacro(xacro_path, tmp_path)
    return {
        joint.attrib["name"]
        for joint in robot.findall("joint")
    }


def _gripper_collision_links(xacro_path, tmp_path):
    robot = _robot_from_xacro(xacro_path, tmp_path)
    return {
        link.attrib["name"]
        for link in robot.findall("link")
        if link.attrib["name"].startswith("gripper_")
        and link.find("collision") is not None
    }


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


def _all_pairs(values):
    ordered_values = sorted(values)
    return {
        frozenset((first, second))
        for first_index, first in enumerate(ordered_values)
        for second in ordered_values[first_index + 1:]
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
