from lebai_interfaces.srv import GetSignals, SetLed, SetSignals
import pytest

from fakes import FakeNode, FakeRobot


def _register(robot):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.led_signal_services import register_led_signal_services

    node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    services = register_led_signal_services(node, connection)
    callbacks = {
        name: callback
        for _srv_type, name, callback in node.services
    }
    return node, services, callbacks


def test_led_signal_services_register_sdk_category_names():
    robot = FakeRobot()

    node, services, _callbacks = _register(robot)

    assert [(srv_type, name) for srv_type, name, _callback in node.services] == [
        (SetLed, 'led/set_led'),
        (GetSignals, 'signal/get_signals'),
        (SetSignals, 'signal/set_signals'),
    ]
    assert len(services) == 3


def test_set_led_maps_request_to_sdk_call():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = SetLed.Request(mode=3, speed=2, color=[1, 2, 3, 4])

    response = callbacks['led/set_led'](request, SetLed.Response())

    assert robot.calls == [('set_led', (3, 2, [1, 2, 3, 4]), {})]
    assert response.result.success is True


def test_set_led_interface_defines_controller_mode_and_speed_constants():
    assert SetLed.Request.MODE_UNCHANGED == 0
    assert SetLed.Request.MODE_OFF == 1
    assert SetLed.Request.MODE_STEADY == 2
    assert SetLed.Request.MODE_BREATH == 3
    assert SetLed.Request.MODE_ROTATE_SEGMENTED == 4
    assert SetLed.Request.MODE_ROTATE_SOLID == 5
    assert SetLed.Request.MODE_FLASH == 6
    assert SetLed.Request.SPEED_UNSPECIFIED == 0
    assert SetLed.Request.SPEED_FAST == 1
    assert SetLed.Request.SPEED_NORMAL == 2
    assert SetLed.Request.SPEED_SLOW == 3


@pytest.mark.parametrize('mode', range(7))
def test_set_led_accepts_every_mode_boundary(mode):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['led/set_led'](
        SetLed.Request(mode=mode, speed=0, color=[]),
        SetLed.Response(),
    )

    assert response.result.success is True
    assert robot.calls == [('set_led', (mode, 0, []), {})]


@pytest.mark.parametrize('speed', range(4))
def test_set_led_accepts_every_speed_boundary(speed):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['led/set_led'](
        SetLed.Request(mode=0, speed=speed, color=[]),
        SetLed.Response(),
    )

    assert response.result.success is True
    assert robot.calls == [('set_led', (0, speed, []), {})]


@pytest.mark.parametrize('color', [[], [0], [15], [0, 15, 0, 15]])
def test_set_led_accepts_color_count_and_value_boundaries(color):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['led/set_led'](
        SetLed.Request(mode=0, speed=0, color=color),
        SetLed.Response(),
    )

    assert response.result.success is True
    assert robot.calls == [('set_led', (0, 0, color), {})]


@pytest.mark.parametrize(
    ('led_request', 'field_name'),
    [
        (SetLed.Request(mode=7, speed=0, color=[]), 'mode'),
        (SetLed.Request(mode=2**32 - 1, speed=0, color=[]), 'mode'),
        (SetLed.Request(mode=0, speed=4, color=[]), 'speed'),
        (SetLed.Request(mode=0, speed=2**32 - 1, color=[]), 'speed'),
        (SetLed.Request(mode=0, speed=0, color=[0] * 5), 'color'),
        (SetLed.Request(mode=0, speed=0, color=[16]), 'color'),
        (SetLed.Request(mode=0, speed=0, color=[255]), 'color'),
    ],
)
def test_set_led_rejects_invalid_request_without_sdk_call(
    led_request,
    field_name,
):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['led/set_led'](led_request, SetLed.Response())

    assert response.result.success is False
    assert response.result.code == 1
    assert field_name in response.result.message
    assert robot.calls == []


def test_get_signals_returns_int_values():
    robot = FakeRobot()
    robot.signals[5] = -10
    robot.signals[6] = 20
    _node, _services, callbacks = _register(robot)
    request = GetSignals.Request(index=5, length=2)

    response = callbacks['signal/get_signals'](request, GetSignals.Response())

    assert robot.calls == [('get_signals', (5, 2), {})]
    assert response.result.success is True
    assert list(response.values) == [-10, 20]


def test_set_signals_maps_request_to_sdk_call():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = SetSignals.Request(index=7, values=[100, -200])

    response = callbacks['signal/set_signals'](request, SetSignals.Response())

    assert robot.calls == [('set_signals', (7, [100, -200]), {})]
    assert response.result.success is True
    assert robot.signals[7] == 100
    assert robot.signals[8] == -200


def test_led_signal_service_maps_sdk_exception_to_result():
    robot = FakeRobot()
    robot.exceptions['set_signals'] = RuntimeError('signal bank unavailable')
    _node, _services, callbacks = _register(robot)
    request = SetSignals.Request(index=7, values=[100, -200])

    response = callbacks['signal/set_signals'](request, SetSignals.Response())

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'signal bank unavailable'
