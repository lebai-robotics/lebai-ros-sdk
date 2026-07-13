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

import pytest


REPOSITORY_DIR = Path(__file__).resolve().parents[2]
DRIVER_DIR = REPOSITORY_DIR / "lebai_driver"
SUPPORT_DIR = REPOSITORY_DIR / "lebai_lm3_support"
RESOURCES_DIR = REPOSITORY_DIR / "lebai_resources"

DRIVER_RUNTIME_DEPENDENCIES = {
    "control_msgs",
    "geometry_msgs",
    "launch",
    "launch_ros",
    "lebai_interfaces",
    "lebai_lm3_support",
    "rclpy",
    "robot_state_publisher",
    "sensor_msgs",
    "tf_transformations",
    "xacro",
}
DRIVER_TEST_DEPENDENCIES = {
    "ament_copyright",
    "ament_flake8",
    "ament_pep257",
    "builtin_interfaces",
    "python3-packaging",
    "python3-pytest",
    "python3-setuptools",
    "python3-yaml",
    "rosidl_runtime_py",
    "trajectory_msgs",
}
SUPPORT_RUNTIME_DEPENDENCIES = {
    "ament_index_python",
    "joint_state_publisher_gui",
    "launch",
    "launch_ros",
    "lebai_resources",
    "robot_state_publisher",
    "rviz2",
    "xacro",
}
SUPPORT_TEST_DEPENDENCIES = {
    "ament_lint_auto",
    "ament_lint_common",
    "launch_testing",
    "launch_testing_ros",
    "python3-pytest",
    "python3-pytest-xvfb",
    "python3-yaml",
    "rclpy",
    "rmw_cyclonedds_cpp",
    "std_msgs",
}
SUPPORT_PUBLIC_PYTHON_LAUNCHES = frozenset(
    {
        "display_gripper.launch",
        "display_gripper.py",
        "display_lm3.launch.py",
        "display_lm3_l1.launch.py",
        "display_lm3_l1_with_gripper.launch.py",
        "display_lm3_with_gripper.launch.py",
        "standalone_lm3.launch.py",
    }
)
COMMAND_DEPENDENCIES = {
    "xacro": "xacro",
}

DRIVER_TEST_IMPORT_DEPENDENCIES = {
    "ament_copyright": "ament_copyright",
    "ament_flake8": "ament_flake8",
    "ament_pep257": "ament_pep257",
    "builtin_interfaces": "builtin_interfaces",
    "packaging": "python3-packaging",
    "pytest": "python3-pytest",
    "rosidl_runtime_py": "rosidl_runtime_py",
    "setuptools": "python3-setuptools",
    "trajectory_msgs": "trajectory_msgs",
    "yaml": "python3-yaml",
}
DRIVER_TEST_RUNTIME_IMPORTS = {
    "control_msgs",
    "geometry_msgs",
    "launch",
    "launch_ros",
    "lebai_interfaces",
    "pylebai",
    "rclpy",
    "sensor_msgs",
}
SUPPORT_TEST_IMPORT_DEPENDENCIES = {
    "launch_testing": "launch_testing",
    "launch_testing_ros": "launch_testing_ros",
    "pytest": "python3-pytest",
    "pytest_xvfb": "python3-pytest-xvfb",
    "rclpy": "rclpy",
    "std_msgs": "std_msgs",
    "yaml": "python3-yaml",
}


def _package_root(package_dir):
    return ET.parse(package_dir / "package.xml").getroot()


def _dependency_names(package_root, *tags):
    return {
        element.text.strip()
        for tag in tags
        for element in package_root.findall(tag)
    }


def _runtime_dependencies(package_root):
    return _dependency_names(package_root, "depend", "exec_depend")


def _python_trees(*sources):
    paths = []
    for source in sources:
        if source.is_dir():
            paths.extend(source.rglob("*.py"))
        else:
            assert source.is_file(), f"Python source does not exist: {source}"
            paths.append(source)

    paths = sorted(set(paths))
    return [ast.parse(path.read_text(), filename=str(path)) for path in paths]


def _import_roots(trees, local_roots=()):
    roots = set()
    for tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])

    return roots - set(sys.stdlib_module_names) - set(local_roots)


def _call_name(call):
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return None


def _literal_string(node, description):
    assert (
        isinstance(node, ast.Constant)
        and isinstance(node.value, str)
    ), f"{description} must be a string literal"
    return node.value


def _literal_node_packages(trees):
    packages = set()
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or _call_name(node) != "Node":
                continue
            package_keywords = [
                keyword
                for keyword in node.keywords
                if keyword.arg == "package"
            ]
            assert len(package_keywords) == 1, (
                "Node package must be provided by one keyword argument"
            )
            packages.add(
                _literal_string(
                    package_keywords[0].value,
                    "Node package",
                )
            )
    return packages


def _literal_call_arguments(trees, call_names):
    arguments = set()
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            call_name = _call_name(node)
            if call_name not in call_names:
                continue
            assert node.args, (
                f"{call_name} package lookup must use a positional argument"
            )
            arguments.add(
                _literal_string(
                    node.args[0],
                    f"{call_name} package lookup",
                )
            )
    return arguments


def _command_dependencies(trees):
    dependencies = set()
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or _call_name(node) != "Command":
                continue
            assert len(node.args) == 1 and not node.keywords, (
                "Command executable must use one positional sequence"
            )
            command_parts = node.args[0]
            assert (
                isinstance(command_parts, (ast.List, ast.Tuple))
                and command_parts.elts
            ), "Command executable must start a nonempty literal sequence"
            executable_parts = _literal_string(
                command_parts.elts[0],
                "Command executable",
            ).strip().split()
            assert executable_parts, "Command executable must not be empty"
            executable = executable_parts[0]
            assert executable in COMMAND_DEPENDENCIES, (
                f"Command executable is not mapped: {executable}"
            )
            dependencies.add(COMMAND_DEPENDENCIES[executable])
    return dependencies


def _xacro_find_packages(xacro_dir):
    packages = set()
    marker = "$(find "
    for path in sorted(xacro_dir.glob("*.xacro")):
        root = ET.parse(path).getroot()
        for element in root.iter():
            for value in element.attrib.values():
                _, found, remainder = value.partition(marker)
                if not found:
                    continue
                package, closing, _ = remainder.partition(")")
                if closing:
                    packages.add(package.strip())
    return packages


def test_support_dependency_scan_covers_exact_public_launch_inventory():
    launch_dir = SUPPORT_DIR / "launch"
    source_launches = {
        path.name
        for path in launch_dir.iterdir()
        if path.is_file() or path.is_symlink()
    }
    launch_trees = _python_trees(
        *(
            launch_dir / launch_name
            for launch_name in sorted(SUPPORT_PUBLIC_PYTHON_LAUNCHES)
        )
    )

    assert source_launches == SUPPORT_PUBLIC_PYTHON_LAUNCHES
    assert len(launch_trees) == len(SUPPORT_PUBLIC_PYTHON_LAUNCHES)


def test_node_package_scan_rejects_nonliteral_packages():
    trees = [ast.parse("Node(package=package_name)")]

    with pytest.raises(AssertionError, match="Node package"):
        _literal_node_packages(trees)


@pytest.mark.parametrize(
    "call_name",
    ["FindPackageShare", "get_package_share_directory"],
)
def test_package_share_scan_rejects_nonliteral_packages(call_name):
    trees = [ast.parse(f"{call_name}(package_name)")]

    with pytest.raises(AssertionError, match="package lookup"):
        _literal_call_arguments(trees, {call_name})


@pytest.mark.parametrize(
    "source",
    [
        "Command([executable, model_path])",
        'Command(["unsupported-command ", model_path])',
    ],
)
def test_command_scan_rejects_unhandled_executables(source):
    trees = [ast.parse(source)]

    with pytest.raises(AssertionError, match="Command executable"):
        _command_dependencies(trees)


def test_driver_exports_ament_python_without_build_tool_dependency():
    package_root = _package_root(DRIVER_DIR)
    build_type = package_root.find("export/build_type")

    assert build_type is not None
    assert build_type.text.strip() == "ament_python"
    assert _dependency_names(package_root, "buildtool_depend") == set()


def test_driver_runtime_dependencies_are_direct_and_exact():
    package_root = _package_root(DRIVER_DIR)

    assert _runtime_dependencies(package_root) == DRIVER_RUNTIME_DEPENDENCIES


def test_driver_test_dependencies_cover_direct_test_imports():
    package_root = _package_root(DRIVER_DIR)
    test_trees = _python_trees(DRIVER_DIR / "test")
    imported = _import_roots(
        test_trees,
        {"fakes", "lebai_driver", "linter_paths"},
    )

    assert imported == (
        set(DRIVER_TEST_IMPORT_DEPENDENCIES)
        | DRIVER_TEST_RUNTIME_IMPORTS
    )
    assert {
        DRIVER_TEST_IMPORT_DEPENDENCIES[name]
        for name in imported
        if name in DRIVER_TEST_IMPORT_DEPENDENCIES
    } == DRIVER_TEST_DEPENDENCIES
    assert _dependency_names(
        package_root, "test_depend"
    ) == DRIVER_TEST_DEPENDENCIES


def test_driver_runtime_sources_explain_direct_dependencies():
    runtime_trees = _python_trees(
        DRIVER_DIR / "lebai_driver",
        DRIVER_DIR / "launch",
    )
    imports = _import_roots(runtime_trees, {"lebai_driver", "pylebai"})
    nodes = _literal_node_packages(runtime_trees) - {"lebai_driver"}
    package_shares = _literal_call_arguments(
        runtime_trees, {"FindPackageShare"}
    ) - {"lebai_driver"}
    evidence = imports | nodes | package_shares | _command_dependencies(
        runtime_trees
    )

    assert evidence == DRIVER_RUNTIME_DEPENDENCIES


def test_support_runtime_dependencies_are_direct_and_exact():
    package_root = _package_root(SUPPORT_DIR)

    assert _dependency_names(package_root, "buildtool_depend") == {
        "ament_cmake"
    }
    assert _runtime_dependencies(package_root) == SUPPORT_RUNTIME_DEPENDENCIES


def test_support_test_dependencies_cover_direct_test_imports():
    package_root = _package_root(SUPPORT_DIR)
    test_trees = _python_trees(SUPPORT_DIR / "test")
    imported = _import_roots(test_trees)

    assert set(SUPPORT_TEST_IMPORT_DEPENDENCIES) <= imported
    assert {
        SUPPORT_TEST_IMPORT_DEPENDENCIES[name]
        for name in imported
        if name in SUPPORT_TEST_IMPORT_DEPENDENCIES
    } <= SUPPORT_TEST_DEPENDENCIES
    assert _dependency_names(
        package_root, "test_depend"
    ) == SUPPORT_TEST_DEPENDENCIES


def test_support_runtime_sources_explain_direct_dependencies():
    launch_trees = _python_trees(
        *(
            SUPPORT_DIR / "launch" / launch_name
            for launch_name in sorted(SUPPORT_PUBLIC_PYTHON_LAUNCHES)
        )
    )
    imports = _import_roots(launch_trees)
    nodes = _literal_node_packages(launch_trees) - {"lebai_lm3_support"}
    xacro_includes = _xacro_find_packages(SUPPORT_DIR / "urdf") - {
        "lebai_lm3_support"
    }
    evidence = imports | nodes | xacro_includes | _command_dependencies(
        launch_trees
    )

    assert evidence == SUPPORT_RUNTIME_DEPENDENCIES


def test_resources_runtime_dependency_matches_xacro_sources():
    package_root = _package_root(RESOURCES_DIR)
    xacro_namespace = "{http://ros.org/wiki/xacro}"
    has_xacro_elements = any(
        element.tag.startswith(xacro_namespace)
        for path in sorted((RESOURCES_DIR / "urdf").glob("*.xacro"))
        for element in ET.parse(path).getroot().iter()
    )

    assert has_xacro_elements
    assert _dependency_names(package_root, "buildtool_depend") == {
        "ament_cmake"
    }
    assert _runtime_dependencies(package_root) == {"xacro"}
