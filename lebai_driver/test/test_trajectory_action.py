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


def test_trajectory_action_streams_segments_to_move_pvat():
    robot = FakeRobot()
    robot.robot_state = 5
    robot.actual_joint_positions = [2, 3, 4, 5, 6, 7]
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = FakeGoalHandle(_trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls[:2] == [
        ('move_pvat', ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [0.1] * 6, [0.2] * 6, 0.5), {}),
        ('move_pvat', ([2.0, 3.0, 4.0, 5.0, 6.0, 7.0], [0.1] * 6, [0.2] * 6, 0.75), {}),
    ]
    assert robot.calls[2:] == [
        ('get_robot_state', (), {}),
        ('get_actual_joint_positions', (), {}),
    ]
    assert result.error_code == FollowJointTrajectory.Result.SUCCESSFUL
    assert goal_handle.succeeded is True


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
        'move_pvat',
        'move_pvat',
        'get_robot_state',
        'get_robot_state',
        'get_robot_state',
        'get_actual_joint_positions',
        'get_actual_joint_positions',
        'get_actual_joint_positions',
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


def test_trajectory_action_aborts_when_sdk_rejects_pvat():
    robot = FakeRobot()
    robot.exceptions['move_pvat'] = RuntimeError('controller rejected trajectory')
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = FakeGoalHandle(_trajectory())

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls == [
        ('move_pvat', ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [0.1] * 6, [0.2] * 6, 0.5), {})
    ]
    assert result.error_code == FollowJointTrajectory.Result.INVALID_GOAL
    assert result.error_string == 'controller rejected trajectory'
    assert goal_handle.aborted is True
