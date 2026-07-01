from lebai_interfaces.srv import Command

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok


_COMMANDS = [
    ('start_stop/start_sys', 'start_sys'),
    ('start_stop/stop_sys', 'stop_sys'),
    ('start_stop/powerdown', 'powerdown'),
    ('start_stop/stop', 'stop'),
    ('start_stop/estop', 'estop'),
    ('start_stop/start_teach_mode', 'start_teach_mode'),
    ('start_stop/end_teach_mode', 'end_teach_mode'),
    ('start_stop/pause_move', 'pause_move'),
    ('start_stop/resume_move', 'resume_move'),
    ('start_stop/reboot', 'reboot'),
]


def register_start_stop_services(node, connection, callback_group=None):
    services = []
    for service_name, method_name in _COMMANDS:
        services.append(
            node.create_service(
                Command,
                service_name,
                _make_command_callback(connection, method_name),
                callback_group=callback_group,
            )
        )
    return services


def _make_command_callback(connection, method_name):
    def callback(request, response):
        del request
        try:
            with connection.sdk_access() as robot:
                getattr(robot, method_name)()
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback
