from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from lebai_interfaces.msg import ClawState, Result
from lebai_interfaces.srv import Command, GetClaw, SetClaw

from lebai_driver.connection import RobotConnection
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


def _register(fake_rospy, robot, gate=None):
    from lebai_driver.claw_services import register_claw_services

    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    return register_claw_services(RosNodeAdapter(fake_rospy), connection, sdk_gate=gate)


def _get_claw_response(fake_rospy, robot, gate=None):
    services = _register(fake_rospy, robot, gate)
    handler = next(service.handler for service in services if service.name == 'claw/get_claw')
    response = handler(GetClaw._request_class())
    assert isinstance(response, GetClaw._response_class)
    wire = BytesIO()
    response.serialize(wire)
    return GetClaw._response_class().deserialize(wire.getvalue())


def test_claw_services_register_sdk_category_names(fake_rospy):
    services = _register(fake_rospy, object())

    assert services == fake_rospy.services
    assert [(service.name, service.srv_type) for service in services] == [
        ('claw/init_claw', Command),
        ('claw/set_claw', SetClaw),
        ('claw/get_claw', GetClaw),
    ]


@pytest.mark.parametrize('method,srv_type,request_fields,args', [
    ('init_claw', Command, {}, (False,)),
    ('set_claw', SetClaw, {'force': 42.0, 'amplitude': 73.0}, (42.0, 73.0)),
])
def test_claw_commands_forward_sdk_arguments(fake_rospy, method, srv_type, request_fields, args):
    robot = Mock(spec=[method])
    services = _register(fake_rospy, robot)
    handler = next(service.handler for service in services if service.name == f'claw/{method}')

    response = handler(srv_type._request_class(**request_fields))

    getattr(robot, method).assert_called_once_with(*args)
    assert isinstance(response, srv_type._response_class)
    assert response.result == Result(success=True, code=0, message='')


@pytest.mark.parametrize('sdk_state', [
    pytest.param({'force': '12.5', 'amplitude': 88, 'hold_on': 1}, id='named-dict'),
    pytest.param({0: '12.5', 1: 88, 2: 1}, id='positional-dict'),
    pytest.param(['12.5', 88, 1], id='list'),
    pytest.param(SimpleNamespace(force='12.5', amplitude=88, hold_on=1), id='object'),
])
def test_get_claw_converts_sdk_state_and_serializes(fake_rospy, sdk_state):
    robot = Mock(spec=['get_claw'])
    robot.get_claw.return_value = sdk_state

    decoded = _get_claw_response(fake_rospy, robot)

    robot.get_claw.assert_called_once_with()
    assert decoded.result == Result(success=True, code=0, message='')
    assert decoded.state == ClawState(connected=True, force=12.5, amplitude=88.0, hold_on=True)


def test_get_claw_preserves_defaults_for_missing_fields(fake_rospy):
    robot = Mock(spec=['get_claw'])
    robot.get_claw.return_value = [12.5]

    decoded = _get_claw_response(fake_rospy, robot)

    assert decoded.result == Result(success=True, code=0, message='')
    assert decoded.state == ClawState(connected=True, force=12.5)


def test_claw_sdk_error_serializes_and_releases_gate(fake_rospy):
    gate = StatusServiceGate()

    def get_claw():
        with gate.status_access() as allowed:
            assert allowed is False
        raise RuntimeError('claw unavailable')

    robot = Mock(spec=['get_claw'])
    robot.get_claw.side_effect = get_claw

    decoded = _get_claw_response(fake_rospy, robot, gate)

    assert decoded.state == ClawState()
    assert decoded.result == Result(success=False, code=1, message='claw unavailable')
    with gate.status_access() as allowed:
        assert allowed is True
