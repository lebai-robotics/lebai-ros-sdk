from lebai_interfaces.srv import (
    Command,
    GetMotionState,
    GetRunningMotion,
    MoveCircular,
    MoveJoint,
    MoveLinear,
    MovePvat,
    SpeedJoint,
    SpeedLinear,
    WaitMove,
)

from lebai_driver.errors import UNSUPPORTED, exception_message
from lebai_driver.result import fail, ok


_UNSUPPORTED_MESSAGE = 'unsupported by installed pylebai'


def register_motion_services(node, connection, callback_group=None):
    definitions = [
        (MoveJoint, 'motion/movej', _movej),
        (MoveLinear, 'motion/movel', _movel),
        (MoveCircular, 'motion/movec', _movec),
        (SpeedJoint, 'motion/speedj', _speedj),
        (SpeedLinear, 'motion/speedl', _speedl),
        (MovePvat, 'motion/move_pvat', _move_pvat),
        (WaitMove, 'motion/wait_move', _wait_move),
        (Command, 'motion/stop_move', _stop_move),
        (Command, 'motion/skip_move', _skip_move),
        (GetRunningMotion, 'motion/get_running_motion', _get_running_motion),
        (GetMotionState, 'motion/get_motion_state', _get_motion_state),
    ]

    services = []
    for srv_type, service_name, handler in definitions:
        services.append(
            node.create_service(
                srv_type,
                service_name,
                _make_motion_callback(connection, handler),
                callback_group=callback_group,
            )
        )
    return services


def _make_motion_callback(connection, handler):
    def callback(request, response):
        try:
            with connection.sdk_access() as robot:
                handler(robot, request, response)
        except _UnsupportedMethod:
            response.result = fail(_UNSUPPORTED_MESSAGE, code=UNSUPPORTED)
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _movej(robot, request, response):
    response.motion_id = _motion_id(
        _sdk_method(robot, 'movej')(
            _motion_target(request.target),
            request.params.acceleration,
            request.params.velocity,
            request.params.time,
            request.params.blend_radius,
        )
    )


def _movel(robot, request, response):
    response.motion_id = _motion_id(
        _sdk_method(robot, 'movel')(
            _motion_target(request.target),
            request.params.acceleration,
            request.params.velocity,
            request.params.time,
            request.params.blend_radius,
        )
    )


def _movec(robot, request, response):
    response.motion_id = _motion_id(
        _sdk_method(robot, 'movec')(
            _motion_target(request.via),
            _motion_target(request.target),
            request.rad,
            request.params.acceleration,
            request.params.velocity,
            request.params.time,
            request.params.blend_radius,
        )
    )


def _speedj(robot, request, response):
    response.motion_id = _motion_id(
        _sdk_method(robot, 'speedj')(
            request.acceleration,
            _float_list(request.velocities),
            request.time,
        )
    )


def _speedl(robot, request, response):
    response.motion_id = _motion_id(
        _sdk_method(robot, 'speedl')(
            request.acceleration,
            _cartesian_pose(request.velocity),
            request.time,
            _cartesian_pose(request.reference),
        )
    )


def _move_pvat(robot, request, response):
    del response
    _sdk_method(robot, 'move_pvat')(
        _float_list(request.positions),
        _float_list(request.velocities),
        _float_list(request.accelerations),
        request.duration,
    )


def _wait_move(robot, request, response):
    del response
    _sdk_method(robot, 'wait_move')(request.motion_id)


def _stop_move(robot, request, response):
    del request, response
    _sdk_method(robot, 'stop_move')()


def _skip_move(robot, request, response):
    del request, response
    _sdk_method(robot, 'skip_move')()


def _get_running_motion(robot, request, response):
    del request
    response.motion_id = _motion_id(_sdk_method(robot, 'get_running_motion')())


def _get_motion_state(robot, request, response):
    response.state = str(_sdk_method(robot, 'get_motion_state')(request.motion_id))


def _sdk_method(robot, name):
    try:
        return getattr(robot, name)
    except AttributeError as exc:
        raise _UnsupportedMethod from exc


def _motion_target(target):
    if target.is_joint_pose:
        return _float_list(target.joint_positions)
    return _cartesian_pose(target.cartesian_pose)


def _cartesian_pose(pose):
    return {
        'x': float(pose.x),
        'y': float(pose.y),
        'z': float(pose.z),
        'rx': float(pose.rx),
        'ry': float(pose.ry),
        'rz': float(pose.rz),
    }


def _float_list(values):
    return [float(value) for value in values]


def _motion_id(value):
    return int(value or 0)


class _UnsupportedMethod(Exception):
    pass
