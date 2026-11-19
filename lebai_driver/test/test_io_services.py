from io import BytesIO
from unittest.mock import Mock

import pytest

from lebai_interfaces.msg import Result
from lebai_interfaces.srv import (
    GetAnalogInput,
    GetAnalogInputs,
    GetAnalogOutput,
    GetAnalogOutputs,
    GetDigitalInput,
    GetDigitalInputs,
    GetDigitalOutput,
    GetDigitalOutputs,
    GetDioMode,
    SetAnalogOutput,
    SetAnalogOutputs,
    SetDigitalOutput,
    SetDigitalOutputs,
    SetDioMode,
)

from lebai_driver.connection import RobotConnection
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


def _register(fake_rospy, robot, gate=None):
    from lebai_driver.io_services import register_io_services

    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    return register_io_services(RosNodeAdapter(fake_rospy), connection, sdk_gate=gate)


def test_io_services_register_sdk_category_names(fake_rospy):
    services = _register(fake_rospy, object())

    assert services == fake_rospy.services
    assert [(service.name, service.srv_type) for service in services] == [
        ('io/set_do', SetDigitalOutput),
        ('io/get_di', GetDigitalInput),
        ('io/get_do', GetDigitalOutput),
        ('io/set_dos', SetDigitalOutputs),
        ('io/get_dis', GetDigitalInputs),
        ('io/get_dos', GetDigitalOutputs),
        ('io/set_ao', SetAnalogOutput),
        ('io/get_ai', GetAnalogInput),
        ('io/get_ao', GetAnalogOutput),
        ('io/set_aos', SetAnalogOutputs),
        ('io/get_ais', GetAnalogInputs),
        ('io/get_aos', GetAnalogOutputs),
        ('io/set_dio_mode', SetDioMode),
        ('io/get_dio_mode', GetDioMode),
    ]


@pytest.mark.parametrize('method,srv_type,fields,args', [
    ('set_do', SetDigitalOutput, {'value': True}, ('flange', 3, True)),
    ('set_ao', SetAnalogOutput, {'value': 1.25}, ('flange', 3, 1.25)),
    ('set_dio_mode', SetDioMode, {'is_output': False}, ('flange', 3, False)),
])
def test_scalar_io_setters_forward_device_pin_and_value(fake_rospy, method, srv_type, fields, args):
    robot = Mock(spec=[method])
    services = _register(fake_rospy, robot)
    handler = next(service.handler for service in services if service.name == f'io/{method}')

    response = handler(srv_type._request_class(device='flange', pin=3, **fields))

    getattr(robot, method).assert_called_once_with(*args)
    assert isinstance(response, srv_type._response_class)
    assert response.result == Result(success=True, code=0, message='')


@pytest.mark.parametrize('method,srv_type,field,sdk_value,expected', [
    ('get_di', GetDigitalInput, 'value', 4, True),
    ('get_do', GetDigitalOutput, 'value', 0, False),
    ('get_ai', GetAnalogInput, 'value', '1.25', 1.25),
    ('get_ao', GetAnalogOutput, 'value', 3, 3.0),
    ('get_dio_mode', GetDioMode, 'is_output', 2, True),
])
def test_scalar_io_getters_convert_sdk_values_and_serialize(
    fake_rospy, method, srv_type, field, sdk_value, expected,
):
    robot = Mock(spec=[method])
    getattr(robot, method).return_value = sdk_value
    services = _register(fake_rospy, robot)
    handler = next(service.handler for service in services if service.name == f'io/{method}')

    response = handler(srv_type._request_class(device='base', pin=7))

    getattr(robot, method).assert_called_once_with('base', 7)
    assert isinstance(response, srv_type._response_class)
    assert type(getattr(response, field)) is type(expected)
    wire = BytesIO()
    response.serialize(wire)
    decoded = srv_type._response_class().deserialize(wire.getvalue())
    assert decoded.result == Result(success=True, code=0, message='')
    assert getattr(decoded, field) == expected


def test_scalar_io_sdk_error_serializes_and_releases_gate(fake_rospy):
    gate = StatusServiceGate()

    def get_ai(_device, _pin):
        with gate.status_access() as allowed:
            assert allowed is False
        raise RuntimeError('analog input unavailable')

    robot = Mock(spec=['get_ai'])
    robot.get_ai.side_effect = get_ai
    services = _register(fake_rospy, robot, gate)
    handler = next(service.handler for service in services if service.name == 'io/get_ai')

    response = handler(GetAnalogInput._request_class(device='base', pin=7))

    assert isinstance(response, GetAnalogInput._response_class)
    wire = BytesIO()
    response.serialize(wire)
    decoded = GetAnalogInput._response_class().deserialize(wire.getvalue())
    assert decoded.value == 0.0
    assert decoded.result == Result(success=False, code=1, message='analog input unavailable')
    with gate.status_access() as allowed:
        assert allowed is True
