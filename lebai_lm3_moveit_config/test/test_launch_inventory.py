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
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_path
from launch import LaunchContext, LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import pytest


PACKAGE_DIR = Path(__file__).resolve().parents[1]
PACKAGE_XML = PACKAGE_DIR / "package.xml"
SOURCE_LAUNCH_DIR = PACKAGE_DIR / "launch"
INSTALLED_LAUNCH_DIR = get_package_share_path(
    "lebai_lm3_moveit_config"
) / "launch"
SUPPORTED_LAUNCHES = {
    "lm3.launch.py",
    "lm3_l1.launch.py",
}
FORBIDDEN_REFERENCES = (
    "Panda",
    "panda",
    "moveit2_tutorials",
    "moveit_resources_panda",
)


def _python_launch_names(launch_dir):
    return {
        path.name
        for path in launch_dir.glob("*.launch.py")
    }


@pytest.mark.parametrize(
    ("location", "launch_dir"),
    [
        ("source", SOURCE_LAUNCH_DIR),
        ("installed", INSTALLED_LAUNCH_DIR),
    ],
)
def test_supported_launch_inventory_is_exact(location, launch_dir):
    assert _python_launch_names(launch_dir) == SUPPORTED_LAUNCHES, location


@pytest.mark.parametrize("launch_name", sorted(SUPPORTED_LAUNCHES))
def test_supported_installed_launch_descriptions_load(launch_name):
    description = PythonLaunchDescriptionSource(
        str(INSTALLED_LAUNCH_DIR / launch_name)
    ).get_launch_description(LaunchContext())

    assert isinstance(description, LaunchDescription)


@pytest.mark.parametrize(
    ("location", "launch_dir"),
    [
        ("source", SOURCE_LAUNCH_DIR),
        ("installed", INSTALLED_LAUNCH_DIR),
    ],
)
def test_launch_sources_do_not_reference_panda_resources(location, launch_dir):
    launch_source = "\n".join(
        path.read_text()
        for path in sorted(launch_dir.glob("*.launch.py"))
    )

    for reference in FORBIDDEN_REFERENCES:
        assert reference not in launch_source, (
            f"{location} launch files reference {reference}"
        )


def test_package_description_is_lebai_specific():
    description = ET.parse(PACKAGE_XML).getroot().find("description")
    description_text = " ".join(description.itertext()).strip()

    assert "Lebai" in description_text
    for reference in FORBIDDEN_REFERENCES:
        assert reference not in description_text
