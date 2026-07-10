import json

from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from rclpy.action import GoalResponse
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from fakes import FakeNode, FakeRobot


def _register(robot):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.trajectory_action import register_trajectory_action

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
    def __init__(self, trajectory, cancel_requested=False):
        self.request = FakeGoalRequest(trajectory)
        self.is_cancel_requested = cancel_requested
        self.succeeded = False
        self.aborted = False
        self.cancel_complete = False

    def succeed(self):
        self.succeeded = True

    def abort(self):
        self.aborted = True

    def canceled(self):
        self.cancel_complete = True


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


class FailingLock:
    def __enter__(self):
        raise AssertionError('trajectory action should not use sdk_access')

    def __exit__(self, *_exc_info):
        return False


def test_trajectory_action_registers_follow_joint_trajectory_server():
    _server, action_type, name, callbacks = _register(FakeRobot())

    assert action_type is FollowJointTrajectory
    assert name == '/lebai_trajectory_controller'
    assert callbacks['goal_callback'] is not None
    assert callbacks['execute_callback'] is not None
    assert callbacks['cancel_callback'] is not None
    assert callbacks['callback_group'] is not None


def test_trajectory_action_accepts_valid_arm_trajectory():
    _server, _action_type, _name, callbacks = _register(FakeRobot())

    response = callbacks['goal_callback'](FakeGoalRequest(_trajectory()))

    assert response == GoalResponse.ACCEPT


def test_trajectory_action_rejects_empty_or_wrong_joint_goals():
    _server, _action_type, _name, callbacks = _register(FakeRobot())

    empty_response = callbacks['goal_callback'](FakeGoalRequest(_trajectory(points=[])))
    wrong_joint_response = callbacks['goal_callback'](
        FakeGoalRequest(_trajectory(joint_names=['joint_1', 'gripper_r_joint1']))
    )

    assert empty_response == GoalResponse.REJECT
    assert wrong_joint_response == GoalResponse.REJECT


def test_trajectory_action_runs_controller_managed_pvat_trajectory():
    robot = FakeRobot()
    robot.robot_state = 5
    robot.actual_joint_positions = [2, 3, 4, 5, 6, 7]
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = FakeGoalHandle(_trajectory())

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
    assert robot.calls[2:4] == [
        ('get_robot_state', (), {}),
        ('get_actual_joint_positions', (), {}),
    ]
    assert robot.calls[4][0] == 'call'
    assert robot.calls[4][1][0] == 'save_trajectory'
    assert json.loads(robot.calls[4][1][1]) == {
        'name': resource_name,
        'dir': '',
    }
    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert goal_handle.succeeded is True


def test_trajectory_action_does_not_start_saved_trajectory_after_cancel():
    robot = CancelOnSaveFakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = FakeGoalHandle(_trajectory())
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


def test_trajectory_action_uses_controller_playback_without_sdk_access_lock():
    robot = FakeRobot()
    robot.robot_state = 5
    robot.actual_joint_positions = [2, 3, 4, 5, 6, 7]
    _server, _action_type, _name, callbacks = _register(robot)
    bridge = callbacks['execute_callback'].__self__
    bridge.sdk_lock = FailingLock()
    goal_handle = FakeGoalHandle(_trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL


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
    goal_handle = FakeGoalHandle(_trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert goal_handle.succeeded is True
    assert [call[0] for call in robot.calls] == [
        'call',
        'move_trajectory',
        'get_robot_state',
        'get_robot_state',
        'get_robot_state',
        'get_actual_joint_positions',
        'get_actual_joint_positions',
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
    goal_handle = FakeGoalHandle(trajectory)

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls == []
    assert result.error_code == FollowJointTrajectory.Result.INVALID_GOAL
    assert goal_handle.aborted is True


def test_trajectory_action_cancel_stops_robot():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = FakeGoalHandle(_trajectory(), cancel_requested=True)

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls == [('stop_move', (), {})]
    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert goal_handle.cancel_complete is True


def test_trajectory_action_cancel_callback_stops_robot_immediately():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)

    response = callbacks['cancel_callback'](object())

    assert response.name == 'ACCEPT'
    assert robot.calls == [('stop_move', (), {})]


def test_trajectory_action_aborts_when_sdk_rejects_saved_trajectory():
    robot = FakeRobot()
    error = RuntimeError('controller rejected trajectory')
    robot.exceptions['call'] = error
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = FakeGoalHandle(_trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls[0][0] == 'call'
    assert robot.calls[0][1][0] == 'save_trajectory'
    assert result.error_code == FollowJointTrajectory.Result.INVALID_GOAL
    assert result.error_string == 'controller rejected trajectory'
    assert goal_handle.aborted is True


def test_trajectory_action_stops_and_cleans_up_when_playback_fails():
    robot = FakeRobot()
    robot.exceptions['move_trajectory'] = RuntimeError('playback failed')
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = FakeGoalHandle(_trajectory())

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
