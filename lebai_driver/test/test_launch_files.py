from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from launch import LaunchDescription


def test_driver_launch_file_imports_and_generates_description():
    description = _load_launch('driver.launch.py').generate_launch_description()

    assert isinstance(description, LaunchDescription)


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
