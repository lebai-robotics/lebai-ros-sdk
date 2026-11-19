from io import BytesIO
from unittest.mock import Mock

import pytest

from lebai_interfaces.msg import Result
from lebai_interfaces.srv import GetSignals, SetLed, SetSignals

from lebai_driver.connection import RobotConnection
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


def _register(fake_rospy, robot, gate=None):
    from lebai_driver.led_signal_services import register_led_signal_services

    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    return register_led_signal_services(RosNodeAdapter(fake_rospy), connection, sdk_gate=gate)


def _get_signals_response(fake_rospy, robot, gate=None):
    services = _register(fake_rospy, robot, gate)
    handler = next(service.handler for service in services if service.name == 'signal/get_signals')
    response = handler(GetSignals._request_class(index=5, length=2))
    assert isinstance(response, GetSignals._response_class)
    wire = BytesIO()
    response.serialize(wire)
    return GetSignals._response_class().deserialize(wire.getvalue())


def test_led_signal_services_register_sdk_category_names(fake_rospy):
    services = _register(fake_rospy, object())

    assert services == fake_rospy.services
    assert [(service.name, service.srv_type) for service in services] == [
        ('led/set_led', SetLed),
        ('signal/get_signals', GetSignals),
        ('signal/set_signals', SetSignals),
    ]


def test_set_led_passes_deserialized_color_as_a_list(fake_rospy):
    robot = Mock(spec=['set_led'])
    services = _register(fake_rospy, robot)
    handler = next(service.handler for service in services if service.name == 'led/set_led')
    wire = BytesIO()
    SetLed._request_class(mode=3, speed=2, color=[1, 8, 255]).serialize(wire)

    response = handler(SetLed._request_class().deserialize(wire.getvalue()))

    robot.set_led.assert_called_once_with(3, 2, [1, 8, 255])
    assert isinstance(response, SetLed._response_class)
    assert response.result == Result(success=True, code=0, message='')


def test_led_sdk_error_serializes_and_releases_gate(fake_rospy):
    gate = StatusServiceGate()

    def set_led(_mode, _speed, _color):
        with gate.status_access() as allowed:
            assert allowed is False
        raise RuntimeError('LED unavailable')

    robot = Mock(spec=['set_led'])
    robot.set_led.side_effect = set_led
    services = _register(fake_rospy, robot, gate)
    handler = next(service.handler for service in services if service.name == 'led/set_led')

    response = handler(SetLed._request_class(mode=3, speed=2, color=[1, 8, 255]))

    assert isinstance(response, SetLed._response_class)
    wire = BytesIO()
    response.serialize(wire)
    decoded = SetLed._response_class().deserialize(wire.getvalue())
    assert decoded.result == Result(success=False, code=1, message='LED unavailable')
    with gate.status_access() as allowed:
        assert allowed is True


def test_set_signals_passes_integer_values_as_a_list(fake_rospy):
    robot = Mock(spec=['set_signals'])
    services = _register(fake_rospy, robot)
    handler = next(service.handler for service in services if service.name == 'signal/set_signals')

    response = handler(SetSignals._request_class(index=7, values=(100, -200)))

    robot.set_signals.assert_called_once_with(7, [100, -200])
    assert isinstance(response, SetSignals._response_class)
    assert response.result == Result(success=True, code=0, message='')


def test_get_signals_converts_signed_int32_values_and_serializes(fake_rospy):
    robot = Mock(spec=['get_signals'])
    robot.get_signals.return_value = ('-2147483648', '2147483647')

    decoded = _get_signals_response(fake_rospy, robot)

    robot.get_signals.assert_called_once_with(5, 2)
    assert decoded.result == Result(success=True, code=0, message='')
    assert list(decoded.values) == [-2_147_483_648, 2_147_483_647]


@pytest.mark.parametrize('sdk_value', [-2_147_483_649, 2_147_483_648])
def test_out_of_range_signal_value_serializes_as_failed_result(fake_rospy, sdk_value):
    robot = Mock(spec=['get_signals'])
    robot.get_signals.return_value = (1, sdk_value)

    decoded = _get_signals_response(fake_rospy, robot)

    assert not decoded.values
    assert decoded.result == Result(
        success=False,
        code=1,
        message=(
            "The 'values' field must be a set or sequence and each value of type 'int' "
            "and each integer in [-2147483648, 2147483647]"
        ),
    )


def test_signal_sdk_error_serializes_and_releases_gate(fake_rospy):
    gate = StatusServiceGate()

    def get_signals(_index, _length):
        with gate.status_access() as allowed:
            assert allowed is False
        raise RuntimeError('signal bank unavailable')

    robot = Mock(spec=['get_signals'])
    robot.get_signals.side_effect = get_signals

    decoded = _get_signals_response(fake_rospy, robot, gate)

    assert not decoded.values
    assert decoded.result == Result(success=False, code=1, message='signal bank unavailable')
    with gate.status_access() as allowed:
        assert allowed is True
