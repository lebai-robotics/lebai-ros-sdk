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

import json

from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from rclpy.action import GoalResponse
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from fakes import FakeNode, FakeRobot


def _register(robot, node=None):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.trajectory_action import register_trajectory_action

    if node is None:
        node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    action_server = register_trajectory_action(node, connection)
    action_type, name, callbacks = node.actions[0]
    return action_server, action_type, name, callbacks


def _trajectory(joint_names=None, points=None):
    trajectory = JointTrajectory()
    trajectory.joint_names = joint_names or [
        'joint_1',
        'joint_2',
        'joint_3',
        'joint_4',
        'joint_5',
        'joint_6',
    ]
    if points is None:
        points = [
            _point(0.0, [0, 0, 0, 0, 0, 0]),
            _point(0.5, [1, 2, 3, 4, 5, 6]),
            _point(1.25, [2, 3, 4, 5, 6, 7]),
        ]
    trajectory.points = points
    return trajectory


def _point(seconds, positions, velocities=None, accelerations=None):
    point = JointTrajectoryPoint()
    point.positions = [float(value) for value in positions]
    point.velocities = velocities or [0.1] * len(point.positions)
    point.accelerations = accelerations or [0.2] * len(point.positions)
    whole_seconds = int(seconds)
    point.time_from_start = Duration(
        sec=whole_seconds,
        nanosec=int(round((seconds - whole_seconds) * 1_000_000_000)),
    )
    return point


class FakeGoalRequest:
    def __init__(self, trajectory):
        self.trajectory = trajectory


class FakeGoalHandle:
    def __init__(self, trajectory, cancel_requested=False, request=None):
        self.request = request if request is not None else FakeGoalRequest(trajectory)
        self.is_cancel_requested = cancel_requested
        self.succeeded = False
        self.aborted = False
        self.cancel_complete = False
        self.execute_requested = False

    def succeed(self):
        self.succeeded = True

    def abort(self):
        self.aborted = True

    def canceled(self):
        self.cancel_complete = True

    def execute(self):
        self.execute_requested = True


def _accepted_goal_handle(callbacks, trajectory, cancel_requested=False):
    request = FakeGoalRequest(trajectory)
    assert callbacks['goal_callback'](request) == GoalResponse.ACCEPT
    goal_handle = FakeGoalHandle(
        trajectory,
        cancel_requested=cancel_requested,
        request=request,
    )
    callbacks['handle_accepted_callback'](goal_handle)
    assert goal_handle.execute_requested is True
    return goal_handle


def _assert_next_trajectory_goal_is_accepted(callbacks):
    response = callbacks['goal_callback'](FakeGoalRequest(_trajectory()))
    assert response == GoalResponse.ACCEPT


class MovingFakeRobot(FakeRobot):
    def __init__(self, states, positions):
        super().__init__()
        self._states = list(states)
        self._positions = [list(position) for position in positions]

    def get_robot_state(self):
        self._record('get_robot_state')
        if len(self._states) > 1:
            return self._states.pop(0)
        return self._states[0]

    def get_actual_joint_positions(self):
        self._record('get_actual_joint_positions')
        if len(self._positions) > 1:
            return self._positions.pop(0)
        return self._positions[0]


class CancelOnSaveFakeRobot(FakeRobot):
    def __init__(self):
        super().__init__()
        self.goal_handle = None

    def call(self, method, params):
        result = super().call(method, params)
        if 'data' in json.loads(params):
            self.goal_handle.is_cancel_requested = True
        return result


class RecordingLock:
    def __init__(self, robot):
        self.robot = robot
        self.events = []

    def __enter__(self):
        self.events.append(('enter', len(self.robot.calls)))
        return self.robot

    def __exit__(self, *_exc_info):
        self.events.append(('exit', len(self.robot.calls)))
        return False


def test_trajectory_action_registers_follow_joint_trajectory_server():
    _server, action_type, name, callbacks = _register(FakeRobot())

    assert action_type is FollowJointTrajectory
    assert name == 'lebai_trajectory_controller/follow_joint_trajectory'
    assert callbacks['goal_callback'] is not None
    assert callbacks['execute_callback'] is not None
    assert callbacks['cancel_callback'] is not None
    assert callbacks['handle_accepted_callback'] is not None
    assert callbacks['callback_group'] is not None


def test_trajectory_action_accepts_valid_arm_trajectory():
    _server, _action_type, _name, callbacks = _register(FakeRobot())

    response = callbacks['goal_callback'](FakeGoalRequest(_trajectory()))

    assert response == GoalResponse.ACCEPT


def test_trajectory_action_rejects_second_goal_without_robot_command():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    first = FakeGoalRequest(_trajectory())
    second = FakeGoalRequest(_trajectory())

    first_response = callbacks['goal_callback'](first)
    second_response = callbacks['goal_callback'](second)

    assert first_response == GoalResponse.ACCEPT
    assert second_response == GoalResponse.REJECT
    assert robot.calls == []


def test_trajectory_action_drops_goal_whose_pending_reservation_expired():
    from lebai_driver.action_goal_owner import ActionGoalOwner

    class Clock:
        now = 10.0

        def monotonic(self):
            return self.now

    clock = Clock()
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    bridge = callbacks['execute_callback'].__self__
    bridge.goal_owner = ActionGoalOwner(
        pending_timeout_sec=1.0,
        monotonic=clock.monotonic,
    )
    expired_request = FakeGoalRequest(_trajectory())
    assert callbacks['goal_callback'](expired_request) == GoalResponse.ACCEPT
    clock.now = 11.0
    assert callbacks['goal_callback'](
        FakeGoalRequest(_trajectory())
    ) == GoalResponse.ACCEPT
    expired_handle = FakeGoalHandle(_trajectory(), request=expired_request)

    callbacks['handle_accepted_callback'](expired_handle)
    result = callbacks['execute_callback'](expired_handle)

    assert expired_handle.aborted is True
    assert expired_handle.execute_requested is True
    assert result.error_code == FollowJointTrajectory.Result.INVALID_GOAL
    assert robot.calls == []


def test_stale_trajectory_cancel_cannot_stop_newer_goal():
    robot = FakeRobot()
    robot.robot_state = 5
    robot.actual_joint_positions = [2, 3, 4, 5, 6, 7]
    _server, _action_type, _name, callbacks = _register(robot)
    first_handle = _accepted_goal_handle(callbacks, _trajectory())
    callbacks['execute_callback'](first_handle)
    robot.calls.clear()

    second_request = FakeGoalRequest(_trajectory())
    assert callbacks['goal_callback'](second_request) == GoalResponse.ACCEPT
    response = callbacks['cancel_callback'](first_handle)

    assert response.name == 'REJECT'
    assert robot.calls == []


def test_trajectory_action_rejects_empty_or_wrong_joint_goals():
    _server, _action_type, _name, callbacks = _register(FakeRobot())

    empty_response = callbacks['goal_callback'](FakeGoalRequest(_trajectory(points=[])))
    wrong_joint_response = callbacks['goal_callback'](
        FakeGoalRequest(_trajectory(joint_names=['joint_1', 'gripper_r_joint1']))
    )

    assert empty_response == GoalResponse.REJECT
    assert wrong_joint_response == GoalResponse.REJECT


def test_trajectory_action_rejects_parameter_advertised_prefixed_joint_names():
    advertised_joint_names = [f'robot1_joint_{index}' for index in range(1, 7)]
    node = FakeNode({'joint_names': advertised_joint_names})
    _server, _action_type, _name, callbacks = _register(FakeRobot(), node=node)

    response = callbacks['goal_callback'](
        FakeGoalRequest(_trajectory(joint_names=advertised_joint_names))
    )

    assert response == GoalResponse.REJECT
    assert 'joint_names' not in node.parameter_requests


def test_trajectory_action_runs_controller_managed_pvat_trajectory():
    robot = FakeRobot()
    robot.robot_state = 5
    robot.actual_joint_positions = [2, 3, 4, 5, 6, 7]
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(callbacks, _trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls[0][0] == 'call'
    assert robot.calls[0][1][0] == 'save_trajectory'
    save_request = json.loads(robot.calls[0][1][1])
    resource_name = save_request['name']
    assert resource_name.startswith('ros2_pvat_')
    assert save_request == {
        'name': resource_name,
        'data': {
            'kind': 'PVAT',
            'data': [
                {
                    'duration': 0.5,
                    'joints': [
                        {'pose': float(index), 'velocity': 0.1, 'acc': 0.2}
                        for index in range(1, 7)
                    ],
                },
                {
                    'duration': 0.75,
                    'joints': [
                        {'pose': float(index), 'velocity': 0.1, 'acc': 0.2}
                        for index in range(2, 8)
                    ],
                },
            ],
        },
        'dir': '',
    }
    assert robot.calls[1] == (
        'move_trajectory',
        (resource_name, ''),
        {},
    )
    assert robot.calls[2:3] == [
        ('get_actual_joint_positions', (), {}),
    ]
    assert robot.calls[3][0] == 'call'
    assert robot.calls[3][1][0] == 'save_trajectory'
    assert json.loads(robot.calls[3][1][1]) == {
        'name': resource_name,
        'dir': '',
    }
    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert goal_handle.succeeded is True


def test_trajectory_action_does_not_start_saved_trajectory_after_cancel():
    robot = CancelOnSaveFakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(callbacks, _trajectory())
    robot.goal_handle = goal_handle

    result = callbacks['execute_callback'](goal_handle)

    assert [call[0] for call in robot.calls] == ['call', 'stop_move', 'call']
    save_request = json.loads(robot.calls[0][1][1])
    assert json.loads(robot.calls[2][1][1]) == {
        'name': save_request['name'],
        'dir': '',
    }
    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert goal_handle.cancel_complete is True
    _assert_next_trajectory_goal_is_accepted(callbacks)


def test_trajectory_action_locks_each_controller_playback_call():
    robot = FakeRobot()
    robot.robot_state = 5
    robot.actual_joint_positions = [2, 3, 4, 5, 6, 7]
    _server, _action_type, _name, callbacks = _register(robot)
    bridge = callbacks['execute_callback'].__self__
    bridge.sdk_lock = RecordingLock(robot)
    goal_handle = _accepted_goal_handle(callbacks, _trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert bridge.sdk_lock.events == [
        ('enter', 0),
        ('exit', 1),
        ('enter', 1),
        ('exit', 2),
        ('enter', 2),
        ('exit', 3),
        ('enter', 3),
        ('exit', 4),
    ]


def test_trajectory_action_waits_planned_duration_before_polling_completion(monkeypatch):
    from lebai_driver import trajectory_action

    sleeps = []
    times = iter([10.0, 10.0, 11.25, 11.25, 11.25])
    monkeypatch.setattr(
        trajectory_action.time,
        'monotonic',
        lambda: next(times),
    )
    monkeypatch.setattr(
        trajectory_action.time,
        'sleep',
        lambda duration: sleeps.append(duration),
    )
    robot = FakeRobot()
    robot.robot_state = 5
    robot.actual_joint_positions = [2, 3, 4, 5, 6, 7]
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(callbacks, _trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert sleeps == [1.25]
    assert [call[0] for call in robot.calls] == [
        'call',
        'move_trajectory',
        'get_actual_joint_positions',
        'call',
    ]


def test_trajectory_action_waits_for_sdk_motion_state_and_final_positions(monkeypatch):
    from lebai_driver import trajectory_action

    monkeypatch.setattr(trajectory_action.time, 'sleep', lambda _duration: None)
    robot = MovingFakeRobot(
        states=[7, 7, 5],
        positions=[
            [0, 0, 0, 0, 0, 0],
            [1, 2, 3, 4, 5, 6],
            [2, 3, 4, 5, 6, 7],
        ],
    )
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(callbacks, _trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert goal_handle.succeeded is True
    assert [call[0] for call in robot.calls] == [
        'call',
        'move_trajectory',
        'get_actual_joint_positions',
        'get_robot_state',
        'get_actual_joint_positions',
        'get_robot_state',
        'get_actual_joint_positions',
        'call',
    ]


def test_trajectory_action_rejects_invalid_point_shapes_during_execution():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    trajectory = _trajectory(points=[
        _point(0.0, [0, 0, 0, 0, 0, 0]),
        _point(0.5, [1, 2, 3], velocities=[0.1, 0.1, 0.1], accelerations=[0.2, 0.2, 0.2]),
    ])
    goal_handle = _accepted_goal_handle(callbacks, trajectory)

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls == []
    assert result.error_code == FollowJointTrajectory.Result.INVALID_GOAL
    assert goal_handle.aborted is True
    _assert_next_trajectory_goal_is_accepted(callbacks)


def test_trajectory_action_cancel_stops_robot():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(
        callbacks,
        _trajectory(),
        cancel_requested=True,
    )

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls == [('stop_move', (), {})]
    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert goal_handle.cancel_complete is True
    _assert_next_trajectory_goal_is_accepted(callbacks)


def test_trajectory_action_cancel_callback_defers_stop_to_active_execute():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(callbacks, _trajectory())

    response = callbacks['cancel_callback'](goal_handle)

    assert response.name == 'ACCEPT'
    assert robot.calls == []
    assert callbacks['goal_callback'](
        FakeGoalRequest(_trajectory())
    ) == GoalResponse.REJECT


def test_trajectory_action_aborts_when_sdk_rejects_saved_trajectory():
    robot = FakeRobot()
    error = RuntimeError('controller rejected trajectory')
    robot.exceptions['call'] = error
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(callbacks, _trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls[0][0] == 'call'
    assert robot.calls[0][1][0] == 'save_trajectory'
    assert result.error_code == FollowJointTrajectory.Result.INVALID_GOAL
    assert result.error_string == 'controller rejected trajectory'
    assert goal_handle.aborted is True
    _assert_next_trajectory_goal_is_accepted(callbacks)


def test_trajectory_action_stops_and_cleans_up_when_playback_fails():
    robot = FakeRobot()
    robot.exceptions['move_trajectory'] = RuntimeError('playback failed')
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(callbacks, _trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert [call[0] for call in robot.calls] == [
        'call',
        'move_trajectory',
        'stop_move',
        'call',
    ]
    save_request = json.loads(robot.calls[0][1][1])
    assert json.loads(robot.calls[-1][1][1]) == {
        'name': save_request['name'],
        'dir': '',
    }
    assert result.error_code == FollowJointTrajectory.Result.INVALID_GOAL
    assert result.error_string == 'playback failed'
    assert goal_handle.aborted is True
    _assert_next_trajectory_goal_is_accepted(callbacks)
