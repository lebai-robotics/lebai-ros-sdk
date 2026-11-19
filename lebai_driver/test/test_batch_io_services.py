from io import BytesIO
from unittest.mock import Mock

import pytest

from lebai_interfaces.msg import Result
from lebai_interfaces.srv import (
    GetAnalogInputs,
    GetAnalogOutputs,
    GetDigitalInputs,
    GetDigitalOutputs,
    SetAnalogOutputs,
    SetDigitalOutputs,
)

from lebai_driver.connection import RobotConnection
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


def _register(fake_rospy, robot, gate=None):
    from lebai_driver.io_services import register_io_services

    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    return register_io_services(RosNodeAdapter(fake_rospy), connection, sdk_gate=gate)


@pytest.mark.parametrize('method,srv_type,values,expected', [
    ('set_dos', SetDigitalOutputs, (True, False, True), [True, False, True]),
    ('set_aos', SetAnalogOutputs, (1.25, 2.5), [1.25, 2.5]),
])
def test_batch_io_setters_forward_lists(fake_rospy, method, srv_type, values, expected):
    robot = Mock(spec=[method])
    services = _register(fake_rospy, robot)
    handler = next(service.handler for service in services if service.name == f'io/{method}')

    response = handler(srv_type._request_class(device='flange', pin=4, values=values))

    getattr(robot, method).assert_called_once_with('flange', 4, expected)
    assert isinstance(response, srv_type._response_class)
    assert response.result == Result(success=True, code=0, message='')


@pytest.mark.parametrize('method,srv_type,sdk_values,expected', [
    ('get_dis', GetDigitalInputs, (4, 0, None), [True, False, False]),
    ('get_dos', GetDigitalOutputs, (0, 1, 2), [False, True, True]),
    ('get_ais', GetAnalogInputs, (1, '2.5', 3.75), [1.0, 2.5, 3.75]),
    ('get_aos', GetAnalogOutputs, ('-1.25', 0, 1.5), [-1.25, 0.0, 1.5]),
])
def test_batch_io_getters_convert_sdk_values_and_serialize(
    fake_rospy, method, srv_type, sdk_values, expected,
):
    robot = Mock(spec=[method])
    getattr(robot, method).return_value = iter(sdk_values)
    services = _register(fake_rospy, robot)
    handler = next(service.handler for service in services if service.name == f'io/{method}')

    response = handler(srv_type._request_class(device='base', pin=7, num=3))

    getattr(robot, method).assert_called_once_with('base', 7, 3)
    assert isinstance(response, srv_type._response_class)
    assert response.values == expected
    assert all(type(value) is type(expected[0]) for value in response.values)
    wire = BytesIO()
    response.serialize(wire)
    decoded = srv_type._response_class().deserialize(wire.getvalue())
    assert decoded.result == Result(success=True, code=0, message='')
    assert list(decoded.values) == expected


def test_batch_io_sdk_error_serializes_and_releases_gate(fake_rospy):
    gate = StatusServiceGate()

    def get_dis(_device, _pin, _num):
        with gate.status_access() as allowed:
            assert allowed is False
        raise RuntimeError('digital inputs unavailable')

    robot = Mock(spec=['get_dis'])
    robot.get_dis.side_effect = get_dis
    services = _register(fake_rospy, robot, gate)
    handler = next(service.handler for service in services if service.name == 'io/get_dis')

    response = handler(GetDigitalInputs._request_class(device='base', pin=7, num=3))

    assert isinstance(response, GetDigitalInputs._response_class)
    wire = BytesIO()
    response.serialize(wire)
    decoded = GetDigitalInputs._response_class().deserialize(wire.getvalue())
    assert not decoded.values
    assert decoded.result == Result(success=False, code=1, message='digital inputs unavailable')
    with gate.status_access() as allowed:
        assert allowed is True
