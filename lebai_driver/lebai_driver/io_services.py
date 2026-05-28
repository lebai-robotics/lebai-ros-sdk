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

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok


def register_io_services(node, connection):
    definitions = [
        (SetDigitalOutput, 'io/set_do', _set_do),
        (GetDigitalInput, 'io/get_di', _get_di),
        (GetDigitalOutput, 'io/get_do', _get_do),
        (SetAnalogOutput, 'io/set_ao', _set_ao),
        (GetAnalogInput, 'io/get_ai', _get_ai),
        (GetAnalogOutput, 'io/get_ao', _get_ao),
        (SetDioMode, 'io/set_dio_mode', _set_dio_mode),
        (GetDioMode, 'io/get_dio_mode', _get_dio_mode),
    ]

    services = []
    for srv_type, service_name, handler in definitions:
        services.append(
            node.create_service(
                srv_type,
                service_name,
                _make_io_callback(connection, handler),
            )
        )
    return services


def _make_io_callback(connection, handler):
    def callback(request, response):
        try:
            handler(connection.robot, request, response)
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _set_do(robot, request, response):
    del response
    robot.set_do(request.device, request.pin, request.value)


def _get_di(robot, request, response):
    response.value = bool(robot.get_di(request.device, request.pin))


def _get_do(robot, request, response):
    response.value = bool(robot.get_do(request.device, request.pin))


def _set_ao(robot, request, response):
    del response
    robot.set_ao(request.device, request.pin, request.value)


def _get_ai(robot, request, response):
    response.value = float(robot.get_ai(request.device, request.pin))


def _get_ao(robot, request, response):
    response.value = float(robot.get_ao(request.device, request.pin))


def _set_dio_mode(robot, request, response):
    del response
    robot.set_dio_mode(request.device, request.pin, request.is_output)


def _get_dio_mode(robot, request, response):
    response.is_output = bool(robot.get_dio_mode(request.device, request.pin))
