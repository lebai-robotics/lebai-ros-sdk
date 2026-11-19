from io import BytesIO
from threading import Event, Thread
from unittest.mock import Mock

import pytest

from lebai_interfaces.msg import CartesianPose, MotionParams, MotionTarget, Result
from lebai_interfaces.srv import (
    Command,
    CommandRequest,
    GetMotionState,
    GetMotionStateRequest,
    GetRunningMotion,
    GetRunningMotionRequest,
    MoveCircular,
    MoveCircularRequest,
    MoveJoint,
    MoveJointRequest,
    MoveLinear,
    MoveLinearRequest,
    MovePvat,
    MovePvatRequest,
    SpeedJoint,
    SpeedJointRequest,
    SpeedLinear,
    SpeedLinearRequest,
    WaitMove,
    WaitMoveRequest,
)

from lebai_driver.connection import RobotConnection
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


MOTION_SERVICES = (
    ('movej', MoveJoint),
    ('movel', MoveLinear),
    ('movec', MoveCircular),
    ('speedj', SpeedJoint),
    ('speedl', SpeedLinear),
    ('move_pvat', MovePvat),
    ('wait_move', WaitMove),
    ('stop_move', Command),
    ('skip_move', Command),
    ('get_running_motion', GetRunningMotion),
    ('get_motion_state', GetMotionState),
)
MAX_MOTION_ID = 4_294_967_295


def _register(fake_rospy, robot, gate=None):
    from lebai_driver.motion_services import register_motion_services

    node = RosNodeAdapter(fake_rospy)
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    return register_motion_services(node, connection, sdk_gate=gate)


def _handlers(services):
    return {service.name: service.handler for service in services}


def test_motion_services_register_sdk_category_names(fake_rospy):
    services = _register(fake_rospy, object())

    assert services == fake_rospy.services
    assert [(service.name, service.srv_type) for service in services] == [
        (f'motion/{name}', srv_type) for name, srv_type in MOTION_SERVICES
    ]


@pytest.mark.parametrize('name,request_message,sdk_args,sdk_return,fields', [
    pytest.param(
        'movej',
        MoveJointRequest(
            target=MotionTarget(is_joint_pose=True, joint_positions=(1, 2, 3, 4, 5, 6)),
            params=MotionParams(acceleration=2.0, velocity=0.5, time=3.0, blend_radius=0.2),
        ),
        ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 2.0, 0.5, 3.0, 0.2),
        str(MAX_MOTION_ID), {'motion_id': MAX_MOTION_ID}, id='movej',
    ),
    pytest.param(
        'movel',
        MoveLinearRequest(
            target=MotionTarget(cartesian_pose=CartesianPose(0.11, 0.22, 0.33, 0.44, 0.55, 0.66)),
            params=MotionParams(acceleration=1.2, velocity=0.4, time=0.0, blend_radius=0.01),
        ),
        ({'x': 0.11, 'y': 0.22, 'z': 0.33, 'rx': 0.44, 'ry': 0.55, 'rz': 0.66}, 1.2, 0.4, 0.0, 0.01),
        str(MAX_MOTION_ID), {'motion_id': MAX_MOTION_ID}, id='movel',
    ),
    pytest.param(
        'movec',
        MoveCircularRequest(
            via=MotionTarget(is_joint_pose=True, joint_positions=(1, 2, 3, 4, 5, 6)),
            target=MotionTarget(cartesian_pose=CartesianPose(0.1, 0.2, 0.3, 0.4, 0.5, 0.6)),
            rad=1.57,
            params=MotionParams(acceleration=1.0, velocity=0.2, time=0.3, blend_radius=0.4),
        ),
        ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
         {'x': 0.1, 'y': 0.2, 'z': 0.3, 'rx': 0.4, 'ry': 0.5, 'rz': 0.6}, 1.57, 1.0, 0.2, 0.3, 0.4),
        str(MAX_MOTION_ID), {'motion_id': MAX_MOTION_ID}, id='movec',
    ),
    pytest.param(
        'speedj', SpeedJointRequest(acceleration=1.0, velocities=(0.1, 0.2), time=0.3),
        (1.0, [0.1, 0.2], 0.3), str(MAX_MOTION_ID), {'motion_id': MAX_MOTION_ID}, id='speedj',
    ),
    pytest.param(
        'speedl',
        SpeedLinearRequest(
            acceleration=2.0,
            velocity=CartesianPose(0.01, 0.2, 0.3, 0.4, 0.5, 0.6),
            time=0.5,
            reference=CartesianPose(0.1, 0.2, 0.25, 0.4, 0.5, 0.6),
        ),
        (2.0, {'x': 0.01, 'y': 0.2, 'z': 0.3, 'rx': 0.4, 'ry': 0.5, 'rz': 0.6},
         0.5, {'x': 0.1, 'y': 0.2, 'z': 0.25, 'rx': 0.4, 'ry': 0.5, 'rz': 0.6}),
        str(MAX_MOTION_ID), {'motion_id': MAX_MOTION_ID}, id='speedl',
    ),
    pytest.param(
        'move_pvat',
        MovePvatRequest(positions=(1, 2), velocities=(3, 4), accelerations=(5, 6), duration=0.007),
        ([1.0, 2.0], [3.0, 4.0], [5.0, 6.0], 0.007), None, {}, id='move_pvat',
    ),
    pytest.param('wait_move', WaitMoveRequest(motion_id=123), (123,), None, {}, id='wait_move'),
    pytest.param('stop_move', CommandRequest(), (), None, {}, id='stop_move'),
    pytest.param('skip_move', CommandRequest(), (), None, {}, id='skip_move'),
    pytest.param(
        'get_running_motion', GetRunningMotionRequest(), (),
        str(MAX_MOTION_ID), {'motion_id': MAX_MOTION_ID}, id='get_running_motion',
    ),
    pytest.param(
        'get_motion_state', GetMotionStateRequest(motion_id=123), (123,),
        456, {'state': '456'}, id='get_motion_state',
    ),
])
def test_motion_service_maps_sdk_arguments_and_generated_response(
    fake_rospy, name, request_message, sdk_args, sdk_return, fields,
):
    robot = Mock(spec=[name])
    getattr(robot, name).return_value = sdk_return
    handlers = _handlers(_register(fake_rospy, robot))

    response = handlers[f'motion/{name}'](request_message)

    getattr(robot, name).assert_called_once_with(*sdk_args)
    response_type = dict(MOTION_SERVICES)[name]._response_class
    assert isinstance(response, response_type)
    assert response == response_type(result=Result(success=True, code=0, message=''), **fields)
    if 'motion_id' in fields:
        assert type(response.motion_id) is int
        wire = BytesIO()
        response.serialize(wire)
        assert response_type().deserialize(wire.getvalue()).motion_id == MAX_MOTION_ID


@pytest.mark.parametrize('motion_id', [-1, MAX_MOTION_ID + 1])
def test_invalid_motion_id_serializes_as_failed_result(fake_rospy, motion_id):
    robot = Mock(spec=['movej'])
    robot.movej.return_value = motion_id
    handlers = _handlers(_register(fake_rospy, robot))

    response = handlers['motion/movej'](MoveJointRequest())
    wire = BytesIO()
    response.serialize(wire)
    decoded = MoveJoint._response_class().deserialize(wire.getvalue())

    assert decoded.motion_id == 0
    assert decoded.result == Result(
        success=False,
        code=1,
        message="The 'motion_id' field must be an unsigned integer in [0, 4294967295]",
    )


@pytest.mark.parametrize('name,srv_type', MOTION_SERVICES, ids=[name for name, _ in MOTION_SERVICES])
def test_motion_service_returns_generated_response_on_sdk_exception(fake_rospy, name, srv_type):
    robot = Mock(spec=[name])
    getattr(robot, name).side_effect = RuntimeError('motion rejected')
    handlers = _handlers(_register(fake_rospy, robot))

    response = handlers[f'motion/{name}'](srv_type._request_class())

    assert isinstance(response, srv_type._response_class)
    assert response == srv_type._response_class(
        result=Result(success=False, code=1, message='motion rejected'),
    )


@pytest.mark.parametrize('name,srv_type', MOTION_SERVICES, ids=[name for name, _ in MOTION_SERVICES])
def test_motion_service_reports_unsupported_sdk_method(fake_rospy, name, srv_type):
    handlers = _handlers(_register(fake_rospy, object()))

    response = handlers[f'motion/{name}'](srv_type._request_class())

    assert isinstance(response, srv_type._response_class)
    assert response == srv_type._response_class(
        result=Result(success=False, code=2, message='unsupported by installed pylebai'),
    )


def test_get_running_motion_returns_zero_when_sdk_has_no_motion(fake_rospy):
    robot = Mock(spec=['get_running_motion'])
    robot.get_running_motion.return_value = None
    handlers = _handlers(_register(fake_rospy, robot))

    response = handlers['motion/get_running_motion'](GetRunningMotionRequest())

    assert response.result.success is True
    assert response.motion_id == 0


def test_wait_move_holds_exclusive_gate_until_sdk_returns(fake_rospy):
    gate = StatusServiceGate()
    wait_entered = Event()
    release_wait = Event()
    stop_started = Event()
    stop_entered = Event()
    responses = {}

    def wait_move(_motion_id):
        wait_entered.set()
        assert release_wait.wait(timeout=5)

    def stop_move():
        stop_entered.set()

    robot = Mock(spec=['wait_move', 'stop_move'])
    robot.wait_move.side_effect = wait_move
    robot.stop_move.side_effect = stop_move
    handlers = _handlers(_register(fake_rospy, robot, gate))

    def call_wait():
        responses['wait'] = handlers['motion/wait_move'](WaitMoveRequest(motion_id=123))

    def call_stop():
        stop_started.set()
        responses['stop'] = handlers['motion/stop_move'](CommandRequest())

    wait_thread = Thread(target=call_wait, daemon=True)
    stop_thread = Thread(target=call_stop, daemon=True)
    wait_thread.start()
    try:
        assert wait_entered.wait(timeout=2)
        with gate.status_access() as allowed:
            assert allowed is False

        stop_thread.start()
        assert stop_started.wait(timeout=2)
        assert not stop_entered.wait(timeout=0.1)
    finally:
        release_wait.set()
        wait_thread.join(timeout=2)
        if stop_thread.ident is not None:
            stop_thread.join(timeout=2)

    assert not wait_thread.is_alive()
    assert not stop_thread.is_alive()
    assert stop_entered.is_set()
    assert responses['wait'].result.success is True
    assert responses['stop'].result.success is True
    with gate.status_access() as allowed:
        assert allowed is True


def test_wait_move_releases_exclusive_gate_after_sdk_exception(fake_rospy):
    gate = StatusServiceGate()
    robot = Mock(spec=['wait_move', 'stop_move'])
    robot.wait_move.side_effect = RuntimeError('wait interrupted')
    handlers = _handlers(_register(fake_rospy, robot, gate))

    response = handlers['motion/wait_move'](WaitMoveRequest(motion_id=123))

    assert response.result == Result(success=False, code=1, message='wait interrupted')
    with gate.status_access() as allowed:
        assert allowed is True
    assert handlers['motion/stop_move'](CommandRequest()).result.success is True
