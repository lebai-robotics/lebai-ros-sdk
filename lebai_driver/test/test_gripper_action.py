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

import math

from control_msgs.action import GripperCommand
from rclpy.action import GoalResponse

from fakes import FakeClawData, FakeNode, FakeRobot


MAX_GRIPPER_POSITION = math.pi / 3.0


def _register(robot):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.gripper_action import register_gripper_action

    node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    action_server = register_gripper_action(node, connection)
    action_type, name, callbacks = node.actions[0]
    return action_server, action_type, name, callbacks


def _goal(position, max_effort=0.0):
    goal = GripperCommand.Goal()
    goal.command.position = float(position)
    goal.command.max_effort = float(max_effort)
    return goal


class FakeGoalHandle:
    def __init__(self, goal, cancel_requested=False):
        self.request = goal
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


def _accepted_goal_handle(callbacks, goal, cancel_requested=False):
    assert callbacks['goal_callback'](goal) == GoalResponse.ACCEPT
    goal_handle = FakeGoalHandle(goal, cancel_requested=cancel_requested)
    callbacks['handle_accepted_callback'](goal_handle)
    assert goal_handle.execute_requested is True
    return goal_handle


def _assert_next_gripper_goal_is_accepted(callbacks):
    response = callbacks['goal_callback'](_goal(MAX_GRIPPER_POSITION / 3.0))
    assert response == GoalResponse.ACCEPT


class MovingClawRobot(FakeRobot):
    def __init__(self, amplitudes):
        super().__init__()
        self._amplitudes = list(amplitudes)

    def get_claw(self):
        self._record('get_claw')
        if len(self._amplitudes) > 1:
            amplitude = self._amplitudes.pop(0)
        else:
            amplitude = self._amplitudes[0]
        return FakeClawData(force=self.claw.force, amplitude=amplitude)


def test_gripper_action_registers_moveit_gripper_command_server():
    _server, action_type, name, callbacks = _register(FakeRobot())

    assert action_type is GripperCommand
    assert name == 'lebai_gripper_controller/gripper_cmd'
    assert callbacks['goal_callback'] is not None
    assert callbacks['execute_callback'] is not None
    assert callbacks['cancel_callback'] is not None
    assert callbacks['handle_accepted_callback'] is not None
    assert callbacks['callback_group'] is not None


def test_gripper_action_accepts_moveit_gripper_goals():
    _server, _action_type, _name, callbacks = _register(FakeRobot())

    response = callbacks['goal_callback'](_goal(MAX_GRIPPER_POSITION / 2.0, 20.0))

    assert response == GoalResponse.ACCEPT


def test_gripper_action_rejects_second_goal_without_robot_command():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    first = _goal(MAX_GRIPPER_POSITION / 2.0, 20.0)
    second = _goal(MAX_GRIPPER_POSITION / 3.0, 10.0)

    first_response = callbacks['goal_callback'](first)
    second_response = callbacks['goal_callback'](second)

    assert first_response == GoalResponse.ACCEPT
    assert second_response == GoalResponse.REJECT
    assert robot.calls == []


def test_gripper_action_drops_goal_whose_pending_reservation_expired():
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
    expired_request = _goal(MAX_GRIPPER_POSITION / 2.0, 20.0)
    assert callbacks['goal_callback'](expired_request) == GoalResponse.ACCEPT
    clock.now = 11.0
    assert callbacks['goal_callback'](
        _goal(MAX_GRIPPER_POSITION / 3.0, 10.0)
    ) == GoalResponse.ACCEPT
    expired_handle = FakeGoalHandle(expired_request)

    callbacks['handle_accepted_callback'](expired_handle)
    result = callbacks['execute_callback'](expired_handle)

    assert expired_handle.aborted is True
    assert expired_handle.execute_requested is True
    assert result.stalled is True
    assert result.reached_goal is False
    assert robot.calls == []


def test_stale_gripper_cancel_cannot_affect_newer_goal():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    first_request = _goal(MAX_GRIPPER_POSITION / 2.0, 20.0)
    first_handle = _accepted_goal_handle(callbacks, first_request)
    callbacks['execute_callback'](first_handle)
    robot.calls.clear()

    second_request = _goal(MAX_GRIPPER_POSITION / 3.0, 10.0)
    assert callbacks['goal_callback'](second_request) == GoalResponse.ACCEPT
    response = callbacks['cancel_callback'](first_handle)

    assert response.name == 'REJECT'
    assert robot.calls == []


def test_gripper_action_maps_joint_position_and_effort_to_claw_command():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(
        callbacks,
        _goal(MAX_GRIPPER_POSITION / 2.0, 42.0),
    )

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls == [
        ('set_claw', (42.0, 50.0), {}),
        ('get_claw', (), {}),
    ]
    assert math.isclose(result.position, MAX_GRIPPER_POSITION / 2.0)
    assert result.effort == 42.0
    assert result.reached_goal is True
    assert result.stalled is False
    assert goal_handle.succeeded is True
    _assert_next_gripper_goal_is_accepted(callbacks)


def test_gripper_action_clamps_position_and_uses_default_effort_when_moveit_omits_it():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(
        callbacks,
        _goal(MAX_GRIPPER_POSITION * 2.0, 0.0),
    )

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls == [
        ('set_claw', (100.0, 100.0), {}),
        ('get_claw', (), {}),
    ]
    assert math.isclose(result.position, MAX_GRIPPER_POSITION)
    assert result.effort == 100.0
    assert result.reached_goal is True
    assert goal_handle.succeeded is True


def test_gripper_action_waits_until_claw_reaches_requested_position(monkeypatch):
    from lebai_driver import gripper_action

    monkeypatch.setattr(gripper_action.time, 'sleep', lambda _duration: None)
    robot = MovingClawRobot(amplitudes=[0.0, 25.0, 50.0])
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(
        callbacks,
        _goal(MAX_GRIPPER_POSITION / 2.0, 12.0),
    )

    result = callbacks['execute_callback'](goal_handle)

    assert [call[0] for call in robot.calls] == [
        'set_claw',
        'get_claw',
        'get_claw',
        'get_claw',
    ]
    assert result.reached_goal is True
    assert goal_handle.succeeded is True


def test_gripper_action_cancel_before_command_does_not_move_claw():
    robot = FakeRobot()
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(
        callbacks,
        _goal(MAX_GRIPPER_POSITION / 2.0, 42.0),
        cancel_requested=True,
    )

    result = callbacks['execute_callback'](goal_handle)

    assert robot.calls == []
    assert result.reached_goal is False
    assert goal_handle.cancel_complete is True
    _assert_next_gripper_goal_is_accepted(callbacks)


def test_gripper_action_cancel_callback_accepts_moveit_cancel_requests():
    _server, _action_type, _name, callbacks = _register(FakeRobot())
    goal_handle = _accepted_goal_handle(
        callbacks,
        _goal(MAX_GRIPPER_POSITION / 2.0),
    )

    response = callbacks['cancel_callback'](goal_handle)

    assert response.name == 'ACCEPT'
    assert callbacks['goal_callback'](
        _goal(MAX_GRIPPER_POSITION / 3.0)
    ) == GoalResponse.REJECT


def test_gripper_action_releases_owner_after_sdk_failure():
    robot = FakeRobot()
    robot.exceptions['set_claw'] = RuntimeError('claw unavailable')
    _server, _action_type, _name, callbacks = _register(robot)
    goal_handle = _accepted_goal_handle(
        callbacks,
        _goal(MAX_GRIPPER_POSITION / 2.0),
    )

    result = callbacks['execute_callback'](goal_handle)

    assert result.stalled is True
    assert result.reached_goal is False
    assert goal_handle.aborted is True
    _assert_next_gripper_goal_is_accepted(callbacks)
