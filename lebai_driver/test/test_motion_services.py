from lebai_interfaces.msg import CartesianPose, MotionParams, MotionTarget
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

from fakes import FakeNode, FakeRobot


def _register(robot):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.motion_services import register_motion_services

    node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    services = register_motion_services(node, connection)
    callbacks = {
        name: callback
        for _srv_type, name, callback in node.services
    }
    return node, services, callbacks


def _params(acceleration=1.2, velocity=0.4, time=0.0, blend_radius=0.01):
    return MotionParams(
        acceleration=acceleration,
        velocity=velocity,
        time=time,
        blend_radius=blend_radius,
    )


def _joint_target(*positions):
    return MotionTarget(is_joint_pose=True, joint_positions=list(positions))


def _cartesian_pose(x=0.1, y=0.2, z=0.3, rx=0.4, ry=0.5, rz=0.6):
    return CartesianPose(x=x, y=y, z=z, rx=rx, ry=ry, rz=rz)


def _cartesian_target(**kwargs):
    return MotionTarget(is_joint_pose=False, cartesian_pose=_cartesian_pose(**kwargs))


def test_motion_services_register_sdk_category_names():
    node, services, _callbacks = _register(FakeRobot())

    assert [(srv_type, name) for srv_type, name, _callback in node.services] == [
        (MoveJoint, 'motion/movej'),
        (MoveLinear, 'motion/movel'),
        (MoveCircular, 'motion/movec'),
        (SpeedJoint, 'motion/speedj'),
        (SpeedLinear, 'motion/speedl'),
        (MovePvat, 'motion/move_pvat'),
        (WaitMove, 'motion/wait_move'),
        (Command, 'motion/stop_move'),
        (Command, 'motion/skip_move'),
        (GetRunningMotion, 'motion/get_running_motion'),
        (GetMotionState, 'motion/get_motion_state'),
    ]
    assert len(services) == 11


def test_movej_maps_joint_target_to_sdk_call_and_motion_id():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = MoveJoint.Request(
        target=_joint_target(1, 2, 3, 4, 5, 6),
        params=_params(acceleration=2.0, velocity=0.5, time=3.0, blend_radius=0.2),
    )

    response = callbacks['motion/movej'](request, MoveJoint.Response())

    assert robot.calls == [('movej', ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 2.0, 0.5, 3.0, 0.2), {})]
    assert response.result.success is True
    assert response.motion_id == 100


def test_movel_maps_cartesian_target_to_sdk_pose_dict():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = MoveLinear.Request(
        target=_cartesian_target(x=0.11, y=0.22, z=0.33, rx=0.44, ry=0.55, rz=0.66),
        params=_params(),
    )

    response = callbacks['motion/movel'](request, MoveLinear.Response())

    assert robot.calls == [
        (
            'movel',
            (
                {'x': 0.11, 'y': 0.22, 'z': 0.33, 'rx': 0.44, 'ry': 0.55, 'rz': 0.66},
                1.2,
                0.4,
                0.0,
                0.01,
            ),
            {},
        )
    ]
    assert response.result.success is True
    assert response.motion_id == 100


def test_movec_maps_via_and_target_with_radius():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = MoveCircular.Request(
        via=_joint_target(1, 2, 3, 4, 5, 6),
        target=_joint_target(6, 5, 4, 3, 2, 1),
        rad=1.57,
        params=_params(acceleration=1.0, velocity=0.2, time=0.3, blend_radius=0.4),
    )

    response = callbacks['motion/movec'](request, MoveCircular.Response())

    assert robot.calls == [
        (
            'movec',
            ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [6.0, 5.0, 4.0, 3.0, 2.0, 1.0], 1.57, 1.0, 0.2, 0.3, 0.4),
            {},
        )
    ]
    assert response.result.success is True
    assert response.motion_id == 100


def test_speed_and_pvat_services_map_request_fields():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    speedj_response = callbacks['motion/speedj'](
        SpeedJoint.Request(acceleration=1.0, velocities=[0.1, 0.2], time=0.3),
        SpeedJoint.Response(),
    )
    speedl_response = callbacks['motion/speedl'](
        SpeedLinear.Request(
            acceleration=2.0,
            velocity=_cartesian_pose(x=0.01),
            time=0.5,
            reference=_cartesian_pose(z=0.2),
        ),
        SpeedLinear.Response(),
    )
    pvat_response = callbacks['motion/move_pvat'](
        MovePvat.Request(
            positions=[1.0, 2.0],
            velocities=[3.0, 4.0],
            accelerations=[5.0, 6.0],
            duration=0.007,
        ),
        MovePvat.Response(),
    )

    assert robot.calls == [
        ('speedj', (1.0, [0.1, 0.2], 0.3), {}),
        (
            'speedl',
            (
                2.0,
                {'x': 0.01, 'y': 0.2, 'z': 0.3, 'rx': 0.4, 'ry': 0.5, 'rz': 0.6},
                0.5,
                {'x': 0.1, 'y': 0.2, 'z': 0.2, 'rx': 0.4, 'ry': 0.5, 'rz': 0.6},
            ),
            {},
        ),
        ('move_pvat', ([1.0, 2.0], [3.0, 4.0], [5.0, 6.0], 0.007), {}),
    ]
    assert speedj_response.result.success is True
    assert speedj_response.motion_id == 100
    assert speedl_response.result.success is True
    assert speedl_response.motion_id == 101
    assert pvat_response.result.success is True


def test_wait_stop_skip_and_motion_queries_map_to_sdk():
    robot = FakeRobot()
    robot.running_motion_id = 123
    robot.motion_states[123] = 'finished'
    _node, _services, callbacks = _register(robot)

    wait_response = callbacks['motion/wait_move'](
        WaitMove.Request(motion_id=123),
        WaitMove.Response(),
    )
    stop_response = callbacks['motion/stop_move'](Command.Request(), Command.Response())
    skip_response = callbacks['motion/skip_move'](Command.Request(), Command.Response())
    running_response = callbacks['motion/get_running_motion'](
        GetRunningMotion.Request(),
        GetRunningMotion.Response(),
    )
    state_response = callbacks['motion/get_motion_state'](
        GetMotionState.Request(motion_id=123),
        GetMotionState.Response(),
    )

    assert robot.calls == [
        ('wait_move', (123,), {}),
        ('stop_move', (), {}),
        ('skip_move', (), {}),
        ('get_running_motion', (), {}),
        ('get_motion_state', (123,), {}),
    ]
    assert wait_response.result.success is True
    assert stop_response.result.success is True
    assert skip_response.result.success is True
    assert running_response.result.success is True
    assert running_response.motion_id == 123
    assert state_response.result.success is True
    assert state_response.state == 'finished'


def test_motion_service_maps_sdk_exception_to_result():
    robot = FakeRobot()
    robot.exceptions['movej'] = RuntimeError('motion rejected')
    _node, _services, callbacks = _register(robot)
    request = MoveJoint.Request(target=_joint_target(1, 2), params=_params())

    response = callbacks['motion/movej'](request, MoveJoint.Response())

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'motion rejected'


def test_motion_service_reports_unsupported_sdk_method():
    robot = object()
    _node, _services, callbacks = _register(robot)
    request = MoveJoint.Request(target=_joint_target(1, 2), params=_params())

    response = callbacks['motion/movej'](request, MoveJoint.Response())

    assert response.result.success is False
    assert response.result.code == 2
    assert response.result.message == 'unsupported by installed pylebai'
