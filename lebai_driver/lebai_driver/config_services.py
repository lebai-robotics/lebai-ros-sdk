from lebai_interfaces.srv import LoadResourceList

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok


def register_config_services(node, connection, callback_group=None):
    definitions = [
        (LoadResourceList, 'config/load_tcp_list', _load_tcp_list),
        (LoadResourceList, 'config/load_pose_list', _load_pose_list),
        (LoadResourceList, 'config/load_frame_list', _load_frame_list),
        (LoadResourceList, 'config/load_trajectory_list', _load_trajectory_list),
    ]

    services = []
    for srv_type, service_name, handler in definitions:
        services.append(
            node.create_service(
                srv_type,
                service_name,
                _make_config_callback(connection, handler),
                callback_group=callback_group,
            )
        )
    return services


def _make_config_callback(connection, handler):
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


def _load_tcp_list(robot, request, response):
    response.names = _as_names(robot.load_tcp_list(request.directory))


def _load_pose_list(robot, request, response):
    response.names = _as_names(robot.load_pose_list(request.directory))


def _load_frame_list(robot, request, response):
    response.names = _as_names(robot.load_frame_list(request.directory))


def _load_trajectory_list(robot, request, response):
    response.names = _as_names(robot.load_trajectory_list(request.directory))


def _as_names(values):
    return [str(value) for value in values]
