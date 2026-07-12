import ast
from importlib.util import module_from_spec, spec_from_file_location
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
import pytest
import yaml


PACKAGE_DIR = Path(__file__).resolve().parents[1]
EXPECTED_RUNTIME_DEPENDENCIES = {
    "ament_index_python",
    "launch",
    "launch_ros",
    "lebai_driver",
    "lebai_lm3_support",
    "moveit_kinematics",
    "moveit_planners_ompl",
    "moveit_ros_move_group",
    "moveit_ros_visualization",
    "moveit_simple_controller_manager",
    "python3-yaml",
    "robot_state_publisher",
    "rviz2",
    "rviz_default_plugins",
    "tf2_ros",
    "xacro",
}
REJECTED_DEPENDENCIES = {
    "backward_ros",
    "joint_state_publisher",
    "joint_state_publisher_gui",
    "moveit2_tutorials",
    "moveit_resources_panda_moveit_config",
}
IMPORT_DEPENDENCIES = {
    "ament_index_python": "ament_index_python",
    "launch": "launch",
    "launch_ros": "launch_ros",
    "xacro": "xacro",
    "yaml": "python3-yaml",
}
PLUGIN_DEPENDENCIES = {
    "default_planner_request_adapters/": "moveit_ros_move_group",
    "kdl_kinematics_plugin/": "moveit_kinematics",
    "moveit_rviz_plugin/": "moveit_ros_visualization",
    "moveit_simple_controller_manager/": "moveit_simple_controller_manager",
    "ompl_interface/": "moveit_planners_ompl",
    "rviz_common/": "rviz2",
    "rviz_default_plugins/": "rviz_default_plugins",
}
PLUGIN_IDENTIFIER_ALLOWLIST = {""}
AST_PLUGIN_FIELDS = {
    "moveit_controller_manager",
    "planning_plugin",
}
AST_PLUGIN_LIST_FIELDS = {"request_adapters"}
PLUGIN_CONFIG_FIELDS = {
    PACKAGE_DIR / "config" / "kinematics.yaml": {"kinematics_solver"},
    PACKAGE_DIR / "config" / "lm3_controllers.yaml": {
        "moveit_controller_manager"
    },
    PACKAGE_DIR / "launch" / "moveit.rviz": {"Class"},
}
EXPECTED_PLUGIN_DEPENDENCIES = {
    "moveit_kinematics",
    "moveit_planners_ompl",
    "moveit_ros_move_group",
    "moveit_ros_visualization",
    "moveit_simple_controller_manager",
    "rviz2",
    "rviz_default_plugins",
}
EXPECTED_ACTIVE_PLUGIN_PREFIXES = {
    "default_planner_request_adapters/",
    "kdl_kinematics_plugin/",
    "moveit_rviz_plugin/",
    "moveit_simple_controller_manager/",
    "ompl_interface/",
    "rviz_common/",
    "rviz_default_plugins/",
}
EXPECTED_LAUNCH_PACKAGE_SHARES = {
    "lebai_driver",
    "lebai_lm3_moveit_config",
    "lebai_lm3_support",
}


def _dependency_names(package_root, *tags):
    return {
        element.text.strip()
        for tag in tags
        for element in package_root.findall(tag)
    }


def _launch_trees():
    return [
        ast.parse(path.read_text(), filename=str(path))
        for path in sorted((PACKAGE_DIR / "launch").glob("*.launch.py"))
    ]


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


def _import_dependencies(trees):
    roots = set()
    for tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])

    external_roots = roots - set(sys.stdlib_module_names)
    assert external_roots == set(IMPORT_DEPENDENCIES)
    return {IMPORT_DEPENDENCIES[name] for name in external_roots}


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


def _load_launch_module(launch_path):
    module_name = "_dependency_scan_" + launch_path.stem.replace(".", "_")
    spec = spec_from_file_location(module_name, launch_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    with patch.object(sys, "dont_write_bytecode", True):
        spec.loader.exec_module(module)
    return module


def _launch_package_shares(launch_path):
    packages = set()

    def record_directory(package_name):
        assert isinstance(package_name, str), (
            "get_package_share_directory requires a string package name"
        )
        packages.add(package_name)
        return get_package_share_directory(package_name)

    def record_substitution(package_name):
        assert isinstance(package_name, str), (
            "FindPackageShare requires a string package name"
        )
        packages.add(package_name)
        return FindPackageShare(package_name)

    module = _load_launch_module(launch_path)
    directory_names = [
        name
        for name, value in vars(module).items()
        if value is get_package_share_directory
    ]
    substitution_names = [
        name
        for name, value in vars(module).items()
        if value is FindPackageShare
    ]
    for name in directory_names:
        setattr(module, name, record_directory)
    for name in substitution_names:
        setattr(module, name, record_substitution)

    with TemporaryDirectory() as log_dir:
        with patch.dict(os.environ, {"ROS_LOG_DIR": log_dir}):
            generator = getattr(module, "generate_launch_description", None)
            assert callable(generator), (
                f"launch module has no generator: {launch_path.name}"
            )
            assert generator() is not None

    return packages


def _yaml_plugin_identifiers(value, fields):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            if key in fields:
                assert isinstance(nested_value, str), (
                    f"plugin identifier for {key} must be a string"
                )
                yield nested_value
            yield from _yaml_plugin_identifiers(nested_value, fields)
    elif isinstance(value, list):
        for nested_value in value:
            yield from _yaml_plugin_identifiers(nested_value, fields)


def _ast_plugin_identifiers(trees):
    identifiers = set()
    plugin_fields = AST_PLUGIN_FIELDS | AST_PLUGIN_LIST_FIELDS
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            for key, value in zip(node.keys, node.values):
                if (
                    not isinstance(key, ast.Constant)
                    or key.value not in plugin_fields
                ):
                    continue
                configured_value = _literal_string(
                    value,
                    f"plugin identifier for {key.value}",
                )
                if key.value in AST_PLUGIN_LIST_FIELDS:
                    configured_identifiers = configured_value.split()
                    assert configured_identifiers, (
                        f"plugin identifier list for {key.value} is empty"
                    )
                    identifiers.update(configured_identifiers)
                else:
                    identifiers.add(configured_value)
    return identifiers


def _active_plugin_identifiers(trees):
    identifiers = _ast_plugin_identifiers(trees)
    for path, fields in PLUGIN_CONFIG_FIELDS.items():
        identifiers.update(
            _yaml_plugin_identifiers(
                yaml.safe_load(path.read_text()),
                fields,
            )
        )
    return identifiers


def _plugin_dependency(identifier):
    if identifier in PLUGIN_IDENTIFIER_ALLOWLIST:
        return None

    dependency_matches = [
        dependency
        for prefix, dependency in PLUGIN_DEPENDENCIES.items()
        if identifier.startswith(prefix)
    ]
    assert len(dependency_matches) == 1, (
        f"plugin identifier has an unrecognized prefix: {identifier}"
    )
    return dependency_matches[0]


def _active_plugin_dependencies(trees):
    dependencies = set()
    for identifier in _active_plugin_identifiers(trees):
        dependency = _plugin_dependency(identifier)
        if dependency:
            dependencies.add(dependency)
    return dependencies


def test_node_package_scan_rejects_nonliteral_packages():
    trees = [ast.parse("Node(package=package_name)")]

    with pytest.raises(AssertionError, match="Node package"):
        _literal_node_packages(trees)


@pytest.mark.parametrize(
    "launch_name",
    ["lm3.launch.py", "lm3_l1.launch.py"],
)
def test_launch_package_share_scan_executes_public_lookup_apis(launch_name):
    launch_path = PACKAGE_DIR / "launch" / launch_name

    assert _launch_package_shares(launch_path) == (
        EXPECTED_LAUNCH_PACKAGE_SHARES
    )


def test_launch_package_share_scan_observes_python_aliases(tmp_path):
    launch_path = tmp_path / "aliased.launch.py"
    launch_path.write_text(
        """
from ament_index_python.packages import get_package_share_directory as lookup
from launch_ros.substitutions import FindPackageShare as finder


def generate_launch_description():
    local_lookup = lookup
    local_lookup("lebai_lm3_support")
    finder("lebai_driver")
    return object()
"""
    )

    packages = _launch_package_shares(launch_path)

    assert packages == {
        "lebai_driver",
        "lebai_lm3_support",
    }
    assert not (tmp_path / "__pycache__").exists()


@pytest.mark.parametrize(
    "plugin_value",
    ['"vendor_planner/Planner"', "plugin_name"],
)
def test_plugin_scan_rejects_unhandled_identifiers(plugin_value):
    trees = [
        ast.parse(
            f'config = {{"planning_plugin": {plugin_value}}}'
        )
    ]

    with pytest.raises(AssertionError, match="plugin identifier"):
        _active_plugin_dependencies(trees)


def test_plugin_scan_ignores_strings_outside_dependency_fields():
    trees = [
        ast.parse(
            'config = {"description": "vendor_planner/not-a-plugin"}'
        )
    ]

    assert _active_plugin_dependencies(trees) == (
        EXPECTED_PLUGIN_DEPENDENCIES
        - {"moveit_planners_ompl", "moveit_ros_move_group"}
    )


def test_active_plugin_prefixes_map_to_approved_dependencies():
    launch_trees = _launch_trees()
    identifiers = _active_plugin_identifiers(launch_trees)
    active_prefixes = {
        f"{identifier.split('/', maxsplit=1)[0]}/"
        for identifier in identifiers
        if identifier
    }

    assert active_prefixes == EXPECTED_ACTIVE_PLUGIN_PREFIXES
    assert _active_plugin_dependencies(launch_trees) == (
        EXPECTED_PLUGIN_DEPENDENCIES
    )


def test_moveit_runtime_dependencies_are_direct_and_exact():
    package_root = ET.parse(PACKAGE_DIR / "package.xml").getroot()

    assert _dependency_names(package_root, "buildtool_depend") == {
        "ament_cmake"
    }
    assert _dependency_names(
        package_root, "depend", "exec_depend"
    ) == EXPECTED_RUNTIME_DEPENDENCIES


def test_moveit_rejects_obsolete_and_panda_dependencies():
    package_root = ET.parse(PACKAGE_DIR / "package.xml").getroot()
    declared = _dependency_names(
        package_root,
        "build_depend",
        "build_export_depend",
        "depend",
        "exec_depend",
        "test_depend",
    )

    assert not (declared & REJECTED_DEPENDENCIES)


def test_moveit_test_dependencies_are_direct_and_exact():
    package_root = ET.parse(PACKAGE_DIR / "package.xml").getroot()

    assert _dependency_names(package_root, "test_depend") == {
        "launch_testing",
        "launch_testing_ros",
        "python3-pytest",
        "rcl_interfaces",
        "rclpy",
    }


def test_moveit_sources_explain_every_runtime_dependency():
    launch_trees = _launch_trees()
    package_shares = set().union(*(
        _launch_package_shares(path)
        for path in sorted((PACKAGE_DIR / "launch").glob("*.launch.py"))
    )) - {"lebai_lm3_moveit_config"}
    evidence = (
        _import_dependencies(launch_trees)
        | _literal_node_packages(launch_trees)
        | package_shares
        | _active_plugin_dependencies(launch_trees)
    )

    assert evidence == EXPECTED_RUNTIME_DEPENDENCIES
