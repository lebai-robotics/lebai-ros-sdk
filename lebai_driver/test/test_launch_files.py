from importlib.util import module_from_spec, spec_from_file_location
import os
from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command
from launch_ros.actions import Node


def test_driver_launch_file_imports_and_generates_description():
    description = _load_launch('driver.launch.py').generate_launch_description()

    assert isinstance(description, LaunchDescription)
    assert _launch_argument_names(description) >= {
        'gripper_joint_name',
        'publish_robot_description',
        'robot_model',
    }
    assert 'joint_names' not in _launch_argument_names(description)
    assert _node_specs(description) == [
        ('lebai_driver', 'driver'),
        ('robot_state_publisher', 'robot_state_publisher'),
    ]
    robot_state_publisher = description.entities[-1]
    driver = description.entities[-2]
    assert 'joint_names' not in _node_parameters(driver)
    assert 'gripper_joint_name' in _node_parameters(driver)
    assert ('joint_states', 'model/joint_states') in _node_remappings(robot_state_publisher)
    assert isinstance(
        _node_parameters(robot_state_publisher)['robot_description']._ParameterValue__value[0],
        Command,
    )


def test_discovery_launch_file_imports_and_generates_description():
    description = _load_launch('discovery.launch.py').generate_launch_description()

    assert isinstance(description, LaunchDescription)


def test_serial_gripper_launch_file_imports_and_generates_description():
    description = _load_launch('serial_gripper.launch.py').generate_launch_description()

    assert isinstance(description, LaunchDescription)


def test_legacy_joint_name_config_files_are_not_shipped():
    repository = Path(__file__).resolve().parents[2]
    package_names = ('lebai_driver', 'lebai_lm3_support')
    legacy_files = {
        'joint_names_gripper.yaml',
        'joint_names_lm3.yaml',
        'joint_names_two_lm3.yaml',
    }

    for package_name in package_names:
        source_config = repository / package_name / 'config'
        assert not legacy_files.intersection(_file_names(source_config))

    for package_name in package_names:
        installed_share = _active_installed_share(package_name)
        if installed_share is not None:
            installed_config = installed_share / 'config'
            assert not legacy_files.intersection(_file_names(installed_config))


def _load_launch(filename):
    path = Path(__file__).resolve().parents[1] / 'launch' / filename
    spec = spec_from_file_location(filename.replace('.', '_'), path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _file_names(directory):
    if not directory.is_dir():
        return set()
    return {path.name for path in directory.iterdir()}


def _active_installed_share(package_name):
    for prefix in os.environ.get('AMENT_PREFIX_PATH', '').split(os.pathsep):
        package_marker = (
            Path(prefix)
            / 'share'
            / 'ament_index'
            / 'resource_index'
            / 'packages'
            / package_name
        )
        if package_marker.exists():
            return Path(prefix) / 'share' / package_name
    return None


def _launch_argument_names(description):
    return {
        entity.name
        for entity in description.entities
        if isinstance(entity, DeclareLaunchArgument)
    }


def _node_specs(description):
    return [
        (entity.node_package, entity.node_executable)
        for entity in description.entities
        if isinstance(entity, Node)
    ]


def _node_remappings(node):
    return [
        (_substitution_text(source), _substitution_text(target))
        for source, target in node._Node__remappings
    ]


def _node_parameters(node):
    return {
        _substitution_text(name): value
        for name, value in node._Node__parameters[0].items()
    }


def _substitution_text(substitutions):
    return ''.join(substitution.text for substitution in substitutions)
