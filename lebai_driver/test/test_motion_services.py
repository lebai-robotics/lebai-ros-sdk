# Copyright 2022-2026 Shanghai Lebai Robotics Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


class _SequencedMotionRobot(FakeRobot):
    def __init__(self, states):
        super().__init__()
        self._states = list(states)

    def get_motion_state(self, motion_id):
        self._record('get_motion_state', motion_id)
        if len(self._states) > 1:
            return self._states.pop(0)
        return self._states[0]


class _AdvancingClock:
    def __init__(self):
        self.now = 10.0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, duration):
        self.sleeps.append(duration)
        self.now += duration


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


def _pvat_request(
    positions=None,
    velocities=None,
    accelerations=None,
    duration=0.01,
):
    return MovePvat.Request(
        positions=list(positions if positions is not None else [0.0] * 6),
        velocities=list(velocities if velocities is not None else [0.0] * 6),
        accelerations=list(
            accelerations if accelerations is not None else [0.0] * 6
        ),
        duration=duration,
    )


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


def test_wait_move_interface_supports_optional_timeout():
    request = WaitMove.Request()

    assert hasattr(request, 'timeout_sec')
    assert request.timeout_sec == 0.0


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


def test_wait_move_service_uses_dedicated_callback_group():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.motion_services import register_motion_services

    node = FakeNode()
    regular_group = object()
    wait_group = object()
    robot = FakeRobot()
    connection = RobotConnection(
        '127.0.0.1',
        robot_factory=lambda *_args, **_kwargs: robot,
    )

    register_motion_services(
        node,
        connection,
        callback_group=regular_group,
        wait_callback_group=wait_group,
    )

    assert node.service_callback_groups['motion/wait_move'] is wait_group
    assert {
        group
        for name, group in node.service_callback_groups.items()
        if name != 'motion/wait_move'
    } == {regular_group}


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
        _pvat_request(
            positions=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            velocities=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            accelerations=[1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
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
        (
            'move_pvat',
            (
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                [1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
                0.007,
            ),
            {},
        ),
    ]
    assert speedj_response.result.success is True
    assert speedj_response.motion_id == 100
    assert speedl_response.result.success is True
    assert speedl_response.motion_id == 101
    assert pvat_response.result.success is True


@pytest.mark.parametrize(
    ('field_name', 'values'),
    [
        ('positions', [0.0] * 5),
        ('positions', [0.0] * 7),
        ('velocities', [0.0] * 5),
        ('velocities', [0.0] * 7),
        ('accelerations', [0.0] * 5),
        ('accelerations', [0.0] * 7),
    ],
)
def test_move_pvat_rejects_non_six_element_arrays_without_sdk_call(
    field_name,
    values,
):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = _pvat_request()
    setattr(request, field_name, values)

    response = callbacks['motion/move_pvat'](request, MovePvat.Response())

    assert response.result.success is False
    assert response.result.code == 1
    assert field_name in response.result.message
    assert '6' in response.result.message
    assert robot.calls == []


@pytest.mark.parametrize(
    ('field_name', 'value'),
    [
        ('positions', float('nan')),
        ('positions', float('inf')),
        ('positions', float('-inf')),
        ('velocities', float('nan')),
        ('velocities', float('inf')),
        ('velocities', float('-inf')),
        ('accelerations', float('nan')),
        ('accelerations', float('inf')),
        ('accelerations', float('-inf')),
    ],
)
def test_move_pvat_rejects_nonfinite_array_values_without_sdk_call(
    field_name,
    value,
):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = _pvat_request()
    values = list(getattr(request, field_name))
    values[2] = value
    setattr(request, field_name, values)

    response = callbacks['motion/move_pvat'](request, MovePvat.Response())

    assert response.result.success is False
    assert response.result.code == 1
    assert field_name in response.result.message
    assert 'finite' in response.result.message
    assert robot.calls == []


@pytest.mark.parametrize(
    'duration',
    [0.0, -0.01, float('nan'), float('inf'), float('-inf')],
)
def test_move_pvat_rejects_nonpositive_or_nonfinite_duration_without_sdk_call(
    duration,
):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/move_pvat'](
        _pvat_request(duration=duration),
        MovePvat.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert 'duration' in response.result.message
    assert robot.calls == []


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


def test_wait_move_polls_until_finished_without_calling_blocking_sdk_wait(monkeypatch):
    from lebai_driver import motion_services

    clock = _AdvancingClock()
    monkeypatch.setattr(motion_services, 'monotonic', clock.monotonic, raising=False)
    monkeypatch.setattr(motion_services, 'sleep', clock.sleep, raising=False)
    robot = _SequencedMotionRobot(['WAIT', 'RUNNING', 'FINISHED'])
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/wait_move'](
        WaitMove.Request(motion_id=123, timeout_sec=0.0),
        WaitMove.Response(),
    )

    assert response.result.success is True
    assert robot.calls == [
        ('get_motion_state', (123,), {}),
        ('get_motion_state', (123,), {}),
        ('get_motion_state', (123,), {}),
    ]
    assert clock.sleeps == pytest.approx([0.05, 0.05])


def test_wait_move_times_out_using_monotonic_deadline(monkeypatch):
    from lebai_driver import motion_services

    clock = _AdvancingClock()
    monkeypatch.setattr(motion_services, 'monotonic', clock.monotonic, raising=False)
    monkeypatch.setattr(motion_services, 'sleep', clock.sleep, raising=False)
    robot = _SequencedMotionRobot(['RUNNING'])
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/wait_move'](
        WaitMove.Request(motion_id=123, timeout_sec=0.1),
        WaitMove.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert 'timed out' in response.result.message
    assert clock.now == pytest.approx(10.1)
    assert clock.sleeps == pytest.approx([0.05, 0.05])
    assert robot.calls
    assert {name for name, _args, _kwargs in robot.calls} == {'get_motion_state'}


def test_wait_move_rejects_finished_state_observed_after_deadline(monkeypatch):
    from lebai_driver import motion_services

    clock = _AdvancingClock()

    class SlowFinishedRobot(_SequencedMotionRobot):
        def get_motion_state(self, motion_id):
            clock.now += 0.2
            return super().get_motion_state(motion_id)

    monkeypatch.setattr(motion_services, 'monotonic', clock.monotonic)
    monkeypatch.setattr(motion_services, 'sleep', clock.sleep)
    robot = SlowFinishedRobot(['FINISHED'])
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/wait_move'](
        WaitMove.Request(motion_id=123, timeout_sec=0.1),
        WaitMove.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert 'timed out' in response.result.message
    assert robot.calls == [('get_motion_state', (123,), {})]


@pytest.mark.parametrize(
    'timeout_sec',
    [-0.1, float('nan'), float('inf'), float('-inf')],
)
def test_wait_move_rejects_invalid_timeout_without_sdk_call(timeout_sec):
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/wait_move'](
        WaitMove.Request(motion_id=123, timeout_sec=timeout_sec),
        WaitMove.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert 'timeout_sec' in response.result.message
    assert robot.calls == []


def test_wait_move_rejects_zero_motion_id_without_sdk_call():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/wait_move'](
        WaitMove.Request(motion_id=0, timeout_sec=0.0),
        WaitMove.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert 'motion_id' in response.result.message
    assert robot.calls == []


def test_wait_move_maps_backend_error_to_failure():
    robot = FakeRobot()
    robot.exceptions['get_motion_state'] = RuntimeError('state unavailable')
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/wait_move'](
        WaitMove.Request(motion_id=123, timeout_sec=1.0),
        WaitMove.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'state unavailable'
    assert robot.calls == [('get_motion_state', (123,), {})]


def test_wait_move_rejects_unknown_backend_state():
    robot = _SequencedMotionRobot(['PAUSED'])
    _node, _services, callbacks = _register(robot)

    response = callbacks['motion/wait_move'](
        WaitMove.Request(motion_id=123, timeout_sec=1.0),
        WaitMove.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'unknown motion state: PAUSED'
    assert robot.calls == [('get_motion_state', (123,), {})]


def test_wait_move_releases_sdk_access_between_state_polls(monkeypatch):
    from lebai_driver import motion_services
    from lebai_driver.motion_services import register_motion_services

    class RecordingConnection:
        def __init__(self, robot):
            self.robot = robot
            self.active = False
            self.events = []

        @contextmanager
        def sdk_access(self):
            assert self.active is False
            self.active = True
            self.events.append('enter')
            try:
                yield self.robot
            finally:
                self.events.append('exit')
                self.active = False

    class GuardedRobot(_SequencedMotionRobot):
        def get_motion_state(self, motion_id):
            assert connection.active is True
            return super().get_motion_state(motion_id)

    clock = _AdvancingClock()
    robot = GuardedRobot(['WAIT', 'RUNNING', 'FINISHED'])
    connection = RecordingConnection(robot)

    def sleep_outside_sdk_access(duration):
        assert connection.active is False
        clock.sleep(duration)

    monkeypatch.setattr(motion_services, 'monotonic', clock.monotonic, raising=False)
    monkeypatch.setattr(
        motion_services,
        'sleep',
        sleep_outside_sdk_access,
        raising=False,
    )
    node = FakeNode()
    register_motion_services(node, connection)
    callback = dict((name, callback) for _srv_type, name, callback in node.services)[
        'motion/wait_move'
    ]

    response = callback(
        WaitMove.Request(motion_id=123, timeout_sec=0.0),
        WaitMove.Response(),
    )

    assert response.result.success is True
    assert connection.events == ['enter', 'exit'] * 3
    assert clock.sleeps == pytest.approx([0.05, 0.05])


def test_stop_skip_and_motion_queries_map_to_sdk():
    robot = FakeRobot()
    robot.running_motion_id = 123
    robot.motion_states[123] = 'FINISHED'
    _node, _services, callbacks = _register(robot)

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
        ('stop_move', (), {}),
        ('skip_move', (), {}),
        ('get_running_motion', (), {}),
        ('get_motion_state', (123,), {}),
    ]
    assert stop_response.result.success is True
    assert skip_response.result.success is True
    assert running_response.result.success is True
    assert running_response.motion_id == 123
    assert state_response.result.success is True
    assert state_response.state == 'FINISHED'


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
