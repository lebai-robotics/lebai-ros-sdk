from lebai_interfaces.srv import (
    GetAnalogInput,
    GetAnalogOutput,
    GetDigitalInput,
    GetDigitalOutput,
    GetDioMode,
    SetAnalogOutput,
    SetDigitalOutput,
    SetDioMode,
)

from fakes import FakeNode, FakeRobot


def _register(robot):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.io_services import register_io_services

    node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    services = register_io_services(node, connection)
    callbacks = {
        name: callback
        for _srv_type, name, callback in node.services
    }
    return node, services, callbacks


def test_io_services_register_sdk_category_names():
    robot = FakeRobot()

    node, services, _callbacks = _register(robot)

    assert [(srv_type, name) for srv_type, name, _callback in node.services] == [
        (SetDigitalOutput, 'io/set_do'),
        (GetDigitalInput, 'io/get_di'),
        (GetDigitalOutput, 'io/get_do'),
        (SetAnalogOutput, 'io/set_ao'),
        (GetAnalogInput, 'io/get_ai'),
        (GetAnalogOutput, 'io/get_ao'),
        (SetDioMode, 'io/set_dio_mode'),
        (GetDioMode, 'io/get_dio_mode'),
    ]
    assert len(services) == 8


def test_set_do_maps_request_to_sdk_call():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = SetDigitalOutput.Request(device='flange', pin=2, value=True)

    response = callbacks['io/set_do'](request, SetDigitalOutput.Response())

    assert robot.calls == [('set_do', ('flange', 2, True), {})]
    assert response.result.success is True


def test_get_di_returns_bool_value():
    robot = FakeRobot()
    robot.digital_inputs[('base', 1)] = True
    _node, _services, callbacks = _register(robot)
    request = GetDigitalInput.Request(device='base', pin=1)

    response = callbacks['io/get_di'](request, GetDigitalInput.Response())

    assert robot.calls == [('get_di', ('base', 1), {})]
    assert response.result.success is True
    assert response.value is True


def test_analog_and_dio_queries_return_values():
    robot = FakeRobot()
    robot.analog_inputs[('base', 0)] = 1.25
    robot.analog_outputs[('base', 1)] = 2.5
    robot.dio_modes[('base', 3)] = True
    _node, _services, callbacks = _register(robot)

    ai_response = callbacks['io/get_ai'](
        GetAnalogInput.Request(device='base', pin=0),
        GetAnalogInput.Response(),
    )
    ao_response = callbacks['io/get_ao'](
        GetAnalogOutput.Request(device='base', pin=1),
        GetAnalogOutput.Response(),
    )
    dio_response = callbacks['io/get_dio_mode'](
        GetDioMode.Request(device='base', pin=3),
        GetDioMode.Response(),
    )

    assert ai_response.result.success is True
    assert ai_response.value == 1.25
    assert ao_response.result.success is True
    assert ao_response.value == 2.5
    assert dio_response.result.success is True
    assert dio_response.is_output is True


def test_io_service_maps_sdk_exception_to_result():
    robot = FakeRobot()
    robot.exceptions['set_ao'] = RuntimeError('analog output unavailable')
    _node, _services, callbacks = _register(robot)
    request = SetAnalogOutput.Request(device='base', pin=1, value=2.5)

    response = callbacks['io/set_ao'](request, SetAnalogOutput.Response())

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'analog output unavailable'
