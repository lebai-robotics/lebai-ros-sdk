from contextlib import contextmanager
import math

from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import lebai_interfaces.msg as interface_messages
from lebai_interfaces.msg import JointMotion, MotionParams, MotionTarget
import pytest
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


def _pose(
    x=0.1,
    y=0.2,
    z=0.3,
    qx=0.0,
    qy=0.0,
    qz=0.0,
    qw=1.0,
):
    return Pose(
        position=Point(x=x, y=y, z=z),
        orientation=Quaternion(x=qx, y=qy, z=qz, w=qw),
    )


def _cartesian_target(**kwargs):
    return MotionTarget(is_joint_pose=False, cartesian_pose=_pose(**kwargs))


def test_motion_interfaces_use_standard_geometry_messages_only():
    target = MotionTarget()
    motion = JointMotion()
    speed_request = SpeedLinear.Request()

    assert isinstance(target.cartesian_pose, Pose)
    assert isinstance(motion.actual_tcp_pose, Pose)
    assert isinstance(motion.target_tcp_pose, Pose)
    assert isinstance(motion.actual_flange_pose, Pose)
    assert isinstance(speed_request.velocity, Twist)
    assert isinstance(speed_request.reference, Pose)
    assert not hasattr(interface_messages, 'CartesianPose')


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


def test_motion_service_wraps_sdk_call_with_exclusive_gate():
    from lebai_driver.motion_services import register_motion_services

    class RecordingGate:
        def __init__(self):
            self.events = []

        @contextmanager
        def exclusive_access(self):
            self.events.append('enter')
            yield
            self.events.append('exit')

    class GuardedRobot(FakeRobot):
        def __init__(self, gate):
            super().__init__()
            self._gate = gate

        def movej(self, target, acceleration, velocity, time, blend_radius):
            assert self._gate.events == ['enter']
            return super().movej(target, acceleration, velocity, time, blend_radius)

    node = FakeNode()
    gate = RecordingGate()
    robot = GuardedRobot(gate)
    connection = type('Connection', (), {'robot': robot})()
    register_motion_services(node, connection, sdk_gate=gate)
    callback = dict((name, callback) for _srv_type, name, callback in node.services)[
        'motion/movej'
    ]

    response = callback(
        MoveJoint.Request(target=_joint_target(1, 2, 3, 4, 5, 6), params=_params()),
        MoveJoint.Response(),
    )

    assert gate.events == ['enter', 'exit']
    assert robot.calls[0][0] == 'movej'
    assert response.result.success is True


def test_movel_maps_cartesian_target_to_sdk_pose_dict():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = MoveLinear.Request(
        target=_cartesian_target(
            x=0.11,
            y=0.22,
            z=0.33,
            qx=math.sqrt(0.5),
            qw=math.sqrt(0.5),
        ),
        params=_params(),
    )

    response = callbacks['motion/movel'](request, MoveLinear.Response())

    assert robot.calls == [
        (
            'movel',
            (
                {
                    'x': 0.11,
                    'y': 0.22,
                    'z': 0.33,
                    'rx': math.pi / 2.0,
                    'ry': 0.0,
                    'rz': 0.0,
                },
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
            (
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                [6.0, 5.0, 4.0, 3.0, 2.0, 1.0],
                1.57,
                1.0,
                0.2,
                0.3,
                0.4,
            ),
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
            velocity=Twist(
                linear=Vector3(x=0.01, y=0.02, z=0.03),
                angular=Vector3(x=0.04, y=0.05, z=0.06),
            ),
            time=0.5,
            reference=_pose(
                x=0.1,
                y=0.2,
                z=0.2,
                qz=math.sqrt(0.5),
                qw=math.sqrt(0.5),
            ),
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
                {'x': 0.01, 'y': 0.02, 'z': 0.03, 'rx': 0.04, 'ry': 0.05, 'rz': 0.06},
                0.5,
                {
                    'x': 0.1,
                    'y': 0.2,
                    'z': 0.2,
                    'rx': 0.0,
                    'ry': 0.0,
                    'rz': math.pi / 2.0,
                },
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


@pytest.mark.parametrize(
    ('target_kwargs', 'error_text'),
    [
        ({'qx': 0.0, 'qy': 0.0, 'qz': 0.0, 'qw': 0.0}, 'quaternion'),
        ({'x': float('nan')}, 'finite'),
    ],
)
def test_cartesian_motion_rejects_invalid_pose_without_sdk_call(
    target_kwargs,
    error_text,
):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    target = _cartesian_target(**target_kwargs)

    response = callbacks['motion/movel'](
        MoveLinear.Request(target=target, params=_params()),
        MoveLinear.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert error_text in response.result.message
    assert robot.calls == []


def test_speed_linear_rejects_nonfinite_twist_without_sdk_call():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/speedl'](
        SpeedLinear.Request(
            acceleration=1.0,
            velocity=Twist(angular=Vector3(z=float('inf'))),
            reference=_pose(),
        ),
        SpeedLinear.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert 'finite' in response.result.message
    assert robot.calls == []


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
