import math
from threading import Lock
from time import monotonic, sleep

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

from lebai_driver.conversions import pose_to_sdk, twist_to_sdk
from lebai_driver.errors import UNSUPPORTED, exception_message
from lebai_driver.parameters import DEFAULT_JOINT_NAMES
from lebai_driver.result import fail, ok
from lebai_driver.sdk_gate import exclusive_access


_UNSUPPORTED_MESSAGE = 'unsupported by installed pylebai'
_WAIT_POLL_INTERVAL_SEC = 0.05
_WAIT_PENDING_STATES = {'WAIT', 'RUNNING'}


def register_motion_services(
    node,
    connection,
    callback_group=None,
    wait_callback_group=None,
    sdk_gate=None,
):
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
        if handler is _wait_move:
            callback = _make_wait_move_callback(connection, sdk_gate)
            service_callback_group = (
                wait_callback_group
                if wait_callback_group is not None
                else callback_group
            )
        else:
            callback = _make_motion_callback(connection, handler, sdk_gate)
            service_callback_group = callback_group
        services.append(
            node.create_service(
                srv_type,
                service_name,
                callback,
                callback_group=service_callback_group,
            )
        )
    return services


def _make_motion_callback(connection, handler, sdk_gate=None):
    def callback(request, response):
        try:
            with exclusive_access(sdk_gate):
                handler(connection.robot, request, response)
        except _UnsupportedMethod:
            response.result = fail(_UNSUPPORTED_MESSAGE, code=UNSUPPORTED)
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _make_wait_move_callback(connection, sdk_gate=None):
    active_wait = Lock()

    def callback(request, response):
        if not active_wait.acquire(blocking=False):
            response.result = fail('another wait_move request is active')
            return response
        try:
            try:
                _wait_move(
                    lambda motion_id: _poll_motion_state(
                        connection,
                        sdk_gate,
                        motion_id,
                    ),
                    request,
                    response,
                )
            except _UnsupportedMethod:
                response.result = fail(_UNSUPPORTED_MESSAGE, code=UNSUPPORTED)
            except Exception as exc:
                response.result = fail(exception_message(exc))
            else:
                response.result = ok()
        finally:
            active_wait.release()
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
            twist_to_sdk(request.velocity),
            request.time,
            pose_to_sdk(request.reference),
        )
    )


def _move_pvat(robot, request, response):
    del response
    positions = _validated_pvat_array(request.positions, 'positions')
    velocities = _validated_pvat_array(request.velocities, 'velocities')
    accelerations = _validated_pvat_array(
        request.accelerations,
        'accelerations',
    )
    duration = float(request.duration)
    if not math.isfinite(duration) or duration <= 0.0:
        raise ValueError('duration must be finite and greater than zero')
    _sdk_method(robot, 'move_pvat')(
        positions,
        velocities,
        accelerations,
        duration,
    )


def _wait_move(poll_motion_state, request, response):
    del response
    motion_id = int(request.motion_id)
    timeout_sec = float(request.timeout_sec)
    if motion_id == 0:
        raise ValueError('motion_id must be greater than zero')
    if not math.isfinite(timeout_sec) or timeout_sec < 0.0:
        raise ValueError('timeout_sec must be finite and non-negative')

    deadline = None if timeout_sec == 0.0 else monotonic() + timeout_sec
    while True:
        if deadline is not None and monotonic() >= deadline:
            raise TimeoutError('wait_move timed out')

        state = poll_motion_state(motion_id)
        if deadline is not None and monotonic() >= deadline:
            raise TimeoutError('wait_move timed out')
        if state == 'FINISHED':
            return
        if state not in _WAIT_PENDING_STATES:
            raise RuntimeError('unknown motion state: %s' % state)

        sleep_sec = _WAIT_POLL_INTERVAL_SEC
        if deadline is not None:
            remaining_sec = deadline - monotonic()
            if remaining_sec <= 0.0:
                raise TimeoutError('wait_move timed out')
            sleep_sec = min(sleep_sec, remaining_sec)
        sleep(sleep_sec)


def _poll_motion_state(connection, sdk_gate, motion_id):
    with exclusive_access(sdk_gate):
        return str(
            _sdk_method(connection.robot, 'get_motion_state')(motion_id)
        )


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
    return pose_to_sdk(target.cartesian_pose)


def _float_list(values):
    return [float(value) for value in values]


def _validated_pvat_array(values, field_name):
    converted = _float_list(values)
    joint_count = len(DEFAULT_JOINT_NAMES)
    if len(converted) != joint_count:
        raise ValueError(
            '%s must contain exactly %d values' % (field_name, joint_count)
        )
    if any(not math.isfinite(value) for value in converted):
        raise ValueError('%s values must be finite' % field_name)
    return converted


def _motion_id(value):
    return int(value or 0)


class _UnsupportedMethod(Exception):
    pass
