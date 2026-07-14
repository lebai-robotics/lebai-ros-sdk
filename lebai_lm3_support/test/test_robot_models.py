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
EXPECTED_DYNAMICS = {
    "lm3.xacro": [
        {
            "mass": 2.147,
            "com_x": 0.0,
            "com_y": -0.011,
            "com_z": -0.015,
            "Ixx": 0.0082391363,
            "Ixy": 0.0,
            "Ixz": 0.0,
            "Iyy": 0.0076087775,
            "Iyz": 0.00032383729,
            "Izz": 0.0032573589,
        },
        {
            "mass": 1.972,
            "com_x": -0.134,
            "com_y": 0.0,
            "com_z": 0.094,
            "Ixx": 0.0017128976,
            "Ixy": 0.0,
            "Ixz": 0.000073751933,
            "Iyy": 0.033612233,
            "Iyz": 0.0,
            "Izz": 0.03384798,
        },
        {
            "mass": 1.668,
            "com_x": -0.102,
            "com_y": 0.0,
            "com_z": 0.019,
            "Ixx": 0.0017092842,
            "Ixy": 0.0,
            "Ixz": -0.002750573,
            "Iyy": 0.022563964,
            "Iyz": 0.0,
            "Izz": 0.022383877,
        },
        {
            "mass": 0.969,
            "com_x": 0.0,
            "com_y": 0.011,
            "com_z": -0.039,
            "Ixx": 0.0018744072,
            "Ixy": 0.0,
            "Ixz": 0.0,
            "Iyy": 0.0017809517,
            "Iyz": -0.00040039676,
            "Izz": 0.00079617326,
        },
        {
            "mass": 0.969,
            "com_x": 0.0,
            "com_y": -0.011,
            "com_z": -0.039,
            "Ixx": 0.0018744072,
            "Ixy": 0.0,
            "Ixz": 0.0,
            "Iyy": 0.0017809517,
            "Iyz": 0.00040039676,
            "Izz": 0.00079617326,
        },
        {
            "mass": 0.584,
            "com_x": 0.0,
            "com_y": 0.0,
            "com_z": -0.049,
            "Ixx": 0.00050434988,
            "Ixy": 0.0,
            "Ixz": 0.0,
            "Iyy": 0.0005155908,
            "Iyz": 0.0,
            "Izz": 0.0004119313,
        },
    ],
    "lm3_l1.xacro": [
        {
            "mass": 2.31,
            "com_x": 0.0,
            "com_y": -0.004834,
            "com_z": -0.008972,
            "Ixx": 0.0093,
            "Ixy": 0.0,
            "Ixz": 0.0,
            "Iyy": 0.00913,
            "Iyz": 0.0,
            "Izz": 0.00303,
        },
        {
            "mass": 2.1612,
            "com_x": -0.18435,
            "com_y": 0.0,
            "com_z": 0.09428,
            "Ixx": 0.0211,
            "Ixy": 0.0,
            "Ixz": 0.03767,
            "Iyy": 0.1554,
            "Iyz": 0.0,
            "Izz": 0.13643,
        },
        {
            "mass": 1.8508,
            "com_x": -0.14386,
            "com_y": 0.0,
            "com_z": 0.01892,
            "Ixx": 0.002519,
            "Ixy": 0.0,
            "Ixz": 0.00121,
            "Iyy": 0.08222,
            "Iyz": 0.0,
            "Izz": 0.08138,
        },
        {
            "mass": 0.93256,
            "com_x": 0.0,
            "com_y": 0.011,
            "com_z": -0.03772,
            "Ixx": 0.0032645,
            "Ixy": 0.0,
            "Ixz": 0.0,
            "Iyy": 0.003061,
            "Iyz": 0.0,
            "Izz": 0.000866,
        },
        {
            "mass": 0.93256,
            "com_x": 0.0,
            "com_y": -0.011,
            "com_z": -0.03772,
            "Ixx": 0.0032645,
            "Ixy": 0.0,
            "Ixz": 0.0,
            "Iyy": 0.003061,
            "Iyz": 0.0,
            "Izz": 0.000866,
        },
        {
            "mass": 0.5782,
            "com_x": 0.0,
            "com_y": 0.0,
            "com_z": -0.04882,
            "Ixx": 0.001883,
            "Ixy": 0.0,
            "Ixz": 0.0,
            "Iyy": 0.0018889,
            "Iyz": 0.0,
            "Izz": 0.000404,
        },
    ],
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


@pytest.mark.parametrize(
    ("model_name", "expected_links"),
    EXPECTED_DYNAMICS.items(),
)
def test_expanded_arm_dynamics_match_controller(
    model_name,
    expected_links,
    tmp_path,
):
    robot = _robot_from_xacro(SUPPORT_DIR / "urdf" / model_name, tmp_path)

    for joint_number, expected in enumerate(expected_links, start=1):
        inertial = robot.find(
            f"./link[@name='link_{joint_number}']/inertial"
        )
        assert inertial is not None
        mass = inertial.find("mass")
        origin = inertial.find("origin")
        inertia = inertial.find("inertia")
        assert mass is not None
        assert origin is not None
        assert inertia is not None

        com = [float(value) for value in origin.attrib["xyz"].split()]
        actual = {
            "mass": float(mass.attrib["value"]),
            "com_x": com[0],
            "com_y": com[1],
            "com_z": com[2],
            "Ixx": float(inertia.attrib["ixx"]),
            "Ixy": float(inertia.attrib["ixy"]),
            "Ixz": float(inertia.attrib["ixz"]),
            "Iyy": float(inertia.attrib["iyy"]),
            "Iyz": float(inertia.attrib["iyz"]),
            "Izz": float(inertia.attrib["izz"]),
        }
        assert actual.keys() == expected.keys()
        for field, expected_value in expected.items():
            assert actual[field] == pytest.approx(
                expected_value,
                rel=0,
                abs=1e-9,
            ), f"{model_name} link_{joint_number} {field}"


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
