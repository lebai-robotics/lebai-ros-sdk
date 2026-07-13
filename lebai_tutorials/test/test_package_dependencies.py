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

import ast
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


PACKAGE_DIR = Path(__file__).resolve().parents[1]
EXPECTED_RUNTIME_DEPENDENCIES = {
    "control_msgs",
    "geometry_msgs",
    "lebai_interfaces",
    "moveit_msgs",
    "rclpy",
    "sensor_msgs",
}


def _dependency_names(package_root, *tags):
    return {
        element.text.strip()
        for tag in tags
        for element in package_root.findall(tag)
    }


def _script_import_roots():
    roots = set()
    for path in sorted((PACKAGE_DIR / "scripts").glob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])

    return roots - set(sys.stdlib_module_names) - {
        "lebai_tutorials_common"
    }


def test_tutorial_runtime_dependencies_match_direct_imports():
    package_root = ET.parse(PACKAGE_DIR / "package.xml").getroot()

    assert _dependency_names(package_root, "buildtool_depend") == {
        "ament_cmake"
    }
    assert _dependency_names(
        package_root, "depend", "exec_depend"
    ) == EXPECTED_RUNTIME_DEPENDENCIES
    assert _script_import_roots() == EXPECTED_RUNTIME_DEPENDENCIES


def test_tutorial_pytest_dependency_is_declared():
    package_root = ET.parse(PACKAGE_DIR / "package.xml").getroot()

    assert _dependency_names(package_root, "test_depend") == {
        "python3-pytest"
    }
