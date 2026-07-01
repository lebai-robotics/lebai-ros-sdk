from lebai_interfaces.srv import GetSignals, SetLed, SetSignals

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok


def register_led_signal_services(node, connection, callback_group=None):
    definitions = [
        (SetLed, 'led/set_led', _set_led),
        (GetSignals, 'signal/get_signals', _get_signals),
        (SetSignals, 'signal/set_signals', _set_signals),
    ]

    services = []
    for srv_type, service_name, handler in definitions:
        services.append(
            node.create_service(
                srv_type,
                service_name,
                _make_led_signal_callback(connection, handler),
                callback_group=callback_group,
            )
        )
    return services


def _make_led_signal_callback(connection, handler):
    def callback(request, response):
        try:
            with connection.sdk_access() as robot:
                handler(robot, request, response)
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _set_led(robot, request, response):
    del response
    robot.set_led(request.mode, request.speed, list(request.color))


def _get_signals(robot, request, response):
    response.values = [int(value) for value in robot.get_signals(request.index, request.length)]


def _set_signals(robot, request, response):
    del response
    robot.set_signals(request.index, list(request.values))
