from unittest.mock import Mock

import pytest

from lebai_interfaces.msg import Result
from lebai_interfaces.srv import Command, CommandRequest, CommandResponse

from lebai_driver.connection import RobotConnection
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


COMMANDS = (
    'start_sys',
    'stop_sys',
    'powerdown',
    'stop',
    'estop',
    'start_teach_mode',
    'end_teach_mode',
    'pause_move',
    'resume_move',
    'reboot',
)


def _register(fake_rospy, robot, gate=None):
    from lebai_driver.start_stop_services import register_start_stop_services

    node = RosNodeAdapter(fake_rospy)
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    return register_start_stop_services(node, connection, sdk_gate=gate)


def test_start_stop_services_register_sdk_category_names(fake_rospy):
    services = _register(fake_rospy, object())

    assert services == fake_rospy.services
    assert [(service.srv_type, service.name) for service in services] == [
        (Command, f'start_stop/{name}') for name in COMMANDS
    ]


@pytest.mark.parametrize('name', COMMANDS)
def test_start_stop_service_calls_sdk_method_and_returns_generated_response(fake_rospy, name):
    robot = Mock(spec=COMMANDS)
    services = _register(fake_rospy, robot)
    service = next(service for service in services if service.name == f'start_stop/{name}')

    response = service.handler(CommandRequest())

    getattr(robot, name).assert_called_once_with()
    assert len(robot.mock_calls) == 1
    assert isinstance(response, CommandResponse)
    assert response.result == Result(success=True, code=0, message='')


@pytest.mark.parametrize('name', COMMANDS)
def test_start_stop_service_returns_generated_response_on_sdk_exception(fake_rospy, name):
    robot = Mock(spec=COMMANDS)
    getattr(robot, name).side_effect = RuntimeError('controller offline')
    services = _register(fake_rospy, robot)
    service = next(service for service in services if service.name == f'start_stop/{name}')

    response = service.handler(CommandRequest())

    assert isinstance(response, CommandResponse)
    assert response.result == Result(success=False, code=1, message='controller offline')


def test_start_stop_service_holds_exclusive_gate_during_sdk_call(fake_rospy):
    gate = StatusServiceGate()

    def stop_sys():
        with gate.status_access() as allowed:
            assert allowed is False

    robot = Mock(spec=COMMANDS)
    robot.stop_sys.side_effect = stop_sys
    services = _register(fake_rospy, robot, gate)
    service = next(service for service in services if service.name == 'start_stop/stop_sys')

    response = service.handler(CommandRequest())

    assert response.result == Result(success=True, code=0, message='')
    with gate.status_access() as allowed:
        assert allowed is True
