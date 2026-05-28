from lebai_interfaces.msg import ClawState
from lebai_interfaces.srv import Command, GetClaw, SetClaw

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok


def register_claw_services(node, connection):
    definitions = [
        (Command, 'claw/init_claw', _init_claw),
        (SetClaw, 'claw/set_claw', _set_claw),
        (GetClaw, 'claw/get_claw', _get_claw),
    ]

    services = []
    for srv_type, service_name, handler in definitions:
        services.append(
            node.create_service(
                srv_type,
                service_name,
                _make_claw_callback(connection, handler),
            )
        )
    return services


def _make_claw_callback(connection, handler):
    def callback(request, response):
        try:
            handler(connection.robot, request, response)
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _init_claw(robot, request, response):
    del request, response
    robot.init_claw(False)


def _set_claw(robot, request, response):
    del response
    robot.set_claw(request.force, request.amplitude)


def _get_claw(robot, request, response):
    del request
    response.state = _claw_state_from_sdk(robot.get_claw())


def _claw_state_from_sdk(data):
    state = ClawState()
    state.connected = True
    state.force = float(_get_value(data, 0, 'force', 0.0))
    state.amplitude = float(_get_value(data, 1, 'amplitude', 0.0))
    state.hold_on = bool(_get_value(data, 2, 'hold_on', False))
    return state


def _get_value(data, index, name, default):
    if hasattr(data, name):
        return getattr(data, name)
    try:
        return data[index]
    except (IndexError, KeyError, TypeError):
        return default
