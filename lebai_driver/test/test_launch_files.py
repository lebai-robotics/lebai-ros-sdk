from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command
from launch_ros.actions import Node


def test_driver_launch_file_imports_and_generates_description():
    description = _load_launch('driver.launch.py').generate_launch_description()

    assert isinstance(description, LaunchDescription)
    assert _launch_argument_names(description) >= {
        'publish_robot_description',
        'robot_model',
    }
    assert _node_specs(description) == [
        ('lebai_driver', 'driver'),
        ('robot_state_publisher', 'robot_state_publisher'),
    ]
    robot_state_publisher = description.entities[-1]
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


def _load_launch(filename):
    path = Path(__file__).resolve().parents[1] / 'launch' / filename
    spec = spec_from_file_location(filename.replace('.', '_'), path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
