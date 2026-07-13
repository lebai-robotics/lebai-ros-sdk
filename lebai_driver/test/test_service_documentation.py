from contextlib import suppress
import math
import os
from pathlib import Path
import re
import shlex

import pytest
import rclpy
import yaml

from lebai_interfaces.srv import MovePvat, SetLed
from rosidl_runtime_py.set_message import set_message_fields


REPO_DIR = Path(__file__).resolve().parents[2]
SERVICE_DOCS = REPO_DIR / 'docs' / 'interfaces' / 'services.rst'
SERVICE_ROW = re.compile(
    r'^   \* - ``(?P<endpoint>/lebai/[^`]+)``\n'
    r'     - ``(?P<service_type>[^`]+)``\n'
    r'     - (?P<purpose>\S.*)$',
    re.MULTILINE,
)
SERVICE_CALL_PREFIX = 'ros2 service call '
CANONICAL_IO_DEVICES = frozenset({
    'ROBOT',
    'FLANGE',
    'EXTRA',
    'ROBOT_BTN',
    'SHOULDER',
    'FLANGE_BTN',
})


def _forbid_io(*_args, **_kwargs):
    raise AssertionError('service registration must not perform device I/O')


def _runtime_services(monkeypatch):
    from lebai_driver.discovery_node import LebaiDiscoveryNode
    from lebai_driver.driver_node import LebaiDriverNode
    from lebai_driver.serial_gripper_node import LebaiSerialGripperNode

    monkeypatch.setenv('ROS_DOMAIN_ID', str(1 + os.getpid() % 230))
    rclpy.init(args=['--ros-args', '-r', '__ns:=/lebai'])
    nodes = []
    try:
        nodes.append(LebaiDriverNode(robot_factory=_forbid_io))
        nodes.append(LebaiDiscoveryNode(discovery_factory=_forbid_io))
        nodes.append(LebaiSerialGripperNode(gripper_factory=_forbid_io))
        services = {}
        for node in nodes:
            namespace = node.get_namespace().rstrip('/')
            for service in node.services:
                service_type = service.srv_type
                module_parts = service_type.__module__.split('.')
                if module_parts[:2] != ['lebai_interfaces', 'srv']:
                    continue
                endpoint = namespace + '/' + service.srv_name.lstrip('/')
                assert endpoint not in services
                services[endpoint] = service_type
        return services
    finally:
        for node in reversed(nodes):
            with suppress(Exception):
                node.destroy_node()
        if rclpy.ok():
            with suppress(Exception):
                rclpy.shutdown()


def _documented_service_inventory():
    rows = list(SERVICE_ROW.finditer(SERVICE_DOCS.read_text()))
    inventory = {
        match.group('endpoint'): match.group('service_type')
        for match in rows
    }
    assert len(inventory) == len(rows), 'duplicate service table endpoint'
    return inventory


def _qualified_service_type(service_type):
    module_parts = service_type.__module__.split('.')
    return '%s/srv/%s' % (module_parts[0], service_type.__name__)


def _service_call_commands(contents):
    commands = []
    command_lines = None
    in_bash_block = False

    def finish_command():
        nonlocal command_lines
        if command_lines is not None:
            commands.append('\n'.join(command_lines))
            command_lines = None

    for line in contents.splitlines():
        if line == '.. code-block:: bash':
            finish_command()
            in_bash_block = True
            continue
        if not in_bash_block:
            continue
        if line and not line.startswith('   '):
            finish_command()
            in_bash_block = False
            continue

        code_line = line[3:] if line.startswith('   ') else ''
        if code_line.startswith(SERVICE_CALL_PREFIX):
            finish_command()
            command_lines = [code_line]
        elif command_lines is not None:
            command_lines.append(code_line)

    finish_command()
    return commands


def _validate_example_semantics(service_type, request):
    if hasattr(request, 'device') and request.device not in CANONICAL_IO_DEVICES:
        raise ValueError('device must use a canonical uppercase SDK name')
    if service_type is MovePvat:
        for field_name in ('positions', 'velocities', 'accelerations'):
            values = getattr(request, field_name)
            if len(values) != 6:
                raise ValueError('%s must contain exactly 6 values' % field_name)
            if any(not math.isfinite(value) for value in values):
                raise ValueError('%s values must be finite' % field_name)
        if not math.isfinite(request.duration) or request.duration <= 0.0:
            raise ValueError('duration must be finite and greater than zero')
    elif service_type is SetLed:
        if request.mode > 6:
            raise ValueError('mode must be between 0 and 6')
        if request.speed > 3:
            raise ValueError('speed must be between 0 and 3')
        if len(request.color) > 4:
            raise ValueError('color must contain at most 4 values')
        if any(value > 15 for value in request.color):
            raise ValueError('color values must be between 0 and 15')


def _documented_service_examples(runtime_services):
    inventory = {}
    commands = _service_call_commands(SERVICE_DOCS.read_text())
    for command in commands:
        tokens = shlex.split(command)
        if tokens[:3] != ['ros2', 'service', 'call'] or len(tokens) not in (5, 6):
            raise ValueError('invalid ros2 service call example: %s' % command)

        endpoint, qualified_type = tokens[3:5]
        assert endpoint not in inventory, 'duplicate service example endpoint'
        service_type = runtime_services[endpoint]
        request_values = yaml.safe_load(tokens[5]) if len(tokens) == 6 else {}
        if request_values is None:
            request_values = {}
        request = service_type.Request()
        set_message_fields(request, request_values)
        _validate_example_semantics(service_type, request)
        inventory[endpoint] = qualified_type
    return inventory


def _use_mutated_service_docs(monkeypatch, tmp_path, old, new):
    contents = SERVICE_DOCS.read_text()
    assert contents.count(old) == 1
    mutated_docs = tmp_path / 'services.rst'
    mutated_docs.write_text(contents.replace(old, new))
    monkeypatch.setitem(globals(), 'SERVICE_DOCS', mutated_docs)


def test_service_examples_reject_unknown_request_field(monkeypatch, tmp_path):
    _use_mutated_service_docs(
        monkeypatch,
        tmp_path,
        '{directory: tools}',
        '{directory: tools, unknown: true}',
    )

    with pytest.raises(AttributeError, match='unknown'):
        _validate_service_documentation(monkeypatch)


def test_service_examples_reject_unterminated_shell_quote(monkeypatch, tmp_path):
    _use_mutated_service_docs(
        monkeypatch,
        tmp_path,
        '"{directory: tools}"',
        '"{directory: tools}',
    )

    with pytest.raises(ValueError, match='No closing quotation'):
        _validate_service_documentation(monkeypatch)


def test_service_examples_reject_noncanonical_io_device(monkeypatch, tmp_path):
    _use_mutated_service_docs(
        monkeypatch,
        tmp_path,
        '{device: ROBOT, pin: 0, value: true}',
        '{device: robot, pin: 0, value: true}',
    )

    with pytest.raises(ValueError, match='device'):
        _validate_service_documentation(monkeypatch)


@pytest.mark.parametrize(
    ('old', 'new', 'error_match'),
    [
        (
            'MovePvat "{positions: [0.0, -0.5, 0.5, 0.0, 0.5, 0.0]',
            'MovePvat "{positions: [0.0, -0.5, 0.5, 0.0, 0.5]',
            'positions',
        ),
        (
            'velocities: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]',
            'velocities: [0.0, 0.0, 0.0, 0.0, 0.0, .nan]',
            'velocities',
        ),
        (
            'accelerations: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]',
            'accelerations: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]',
            'accelerations',
        ),
        ('duration: 0.1', 'duration: 0.0', 'duration'),
        ('duration: 0.1', 'duration: .inf', 'duration'),
    ],
)
def test_service_examples_reject_invalid_pvat_semantics(
    monkeypatch,
    tmp_path,
    old,
    new,
    error_match,
):
    _use_mutated_service_docs(monkeypatch, tmp_path, old, new)

    with pytest.raises(ValueError, match=error_match):
        _validate_service_documentation(monkeypatch)


@pytest.mark.parametrize(
    ('old', 'new', 'error_match'),
    [
        ('mode: 2', 'mode: 7', 'mode'),
        ('speed: 0', 'speed: 4', 'speed'),
        ('color: [3]', 'color: [0, 1, 2, 3, 4]', 'color'),
        ('color: [3]', 'color: [16]', 'color'),
    ],
)
def test_service_examples_reject_invalid_led_semantics(
    monkeypatch,
    tmp_path,
    old,
    new,
    error_match,
):
    _use_mutated_service_docs(monkeypatch, tmp_path, old, new)

    with pytest.raises(ValueError, match=error_match):
        _validate_service_documentation(monkeypatch)


def _validate_service_documentation(monkeypatch):
    runtime_services = _runtime_services(monkeypatch)
    runtime_inventory = {
        endpoint: _qualified_service_type(service_type)
        for endpoint, service_type in runtime_services.items()
    }
    assert _documented_service_inventory() == runtime_inventory
    assert _documented_service_examples(runtime_services) == runtime_inventory


def test_service_tables_and_examples_match_runtime_registration(monkeypatch):
    _validate_service_documentation(monkeypatch)
