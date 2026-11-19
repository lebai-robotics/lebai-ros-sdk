import math
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest
from control_msgs.msg import GripperCommand, GripperCommandAction, GripperCommandGoal

from fakes import ActionHarness, assert_shutdown_drains_command
from lebai_driver.connection import RobotConnection


def goal(position=math.pi / 6, effort=42.0):
    return GripperCommandGoal(command=GripperCommand(position=position, max_effort=effort))


def setup_bridge(**kwargs):
    from lebai_driver.gripper_action import register_gripper_action

    server = ActionHarness()
    robot = Mock(spec=['set_claw', 'get_claw'])
    connection = RobotConnection('test', robot_factory=lambda *a, **kw: robot)
    bridge = register_gripper_action(connection, server_factory=server.server_factory,
                                     worker_factory=server.worker_factory, **kwargs)
    return server, robot, bridge


@pytest.mark.parametrize('override,expected', [
    ({}, '/lebai_gripper_controller/gripper_cmd'), ({'action_name': '/robot_a/gripper'}, '/robot_a/gripper'),
])
def test_registration(override, expected):
    server, _, _ = setup_bridge(**override)
    assert (server.name, server.action_type, server.start_count) == (expected, GripperCommandAction, 1)


@pytest.mark.parametrize('position,effort,command,reading,angle', [
    (math.pi / 6, 42, (42, 50), {'amplitude': 50, 'force': 12}, math.pi / 6),
    (4, 0, (100, 100), SimpleNamespace(amplitude=112, force=12), math.pi / 3),
    (-1, -2, (100, 0), (12, -3), 0.0),
    (0, 255, (100, 0), (12, 0), 0.0),
])
def test_command_and_measured_result(position, effort, command, reading, angle):
    server, robot, _ = setup_bridge()
    robot.get_claw.return_value = reading
    handle = server.submit(goal(position, effort))
    handle.set_accepted.assert_called_once()
    server.jobs[0]()
    assert robot.mock_calls == [call.set_claw(*command), call.get_claw()]
    result = handle.set_succeeded.call_args[0][0]
    assert (result.position, result.effort) == (pytest.approx(angle), 12)
    assert result.reached_goal and not result.stalled


def test_polling_uses_angle_tolerance(monkeypatch):
    from lebai_driver import gripper_action
    sleep = Mock()
    monkeypatch.setattr(gripper_action, 'time', SimpleNamespace(monotonic=lambda: 10, sleep=sleep))
    server, robot, _ = setup_bridge()
    robot.get_claw.side_effect = [(30, 48.9), (31, 49.1)]
    handle = server.submit(goal())
    server.jobs[0]()
    sleep.assert_called_once_with(0.05)
    assert robot.get_claw.call_count == 2
    assert handle.set_succeeded.call_args[0][0].effort == 31


def test_timeout_aborts_with_last_reading(monkeypatch):
    from lebai_driver import gripper_action
    clock = Mock(side_effect=[20.0, 25.0, 25.0, 25.000001])
    monkeypatch.setattr(gripper_action, 'time', SimpleNamespace(monotonic=clock, sleep=Mock()))
    server, robot, _ = setup_bridge()
    robot.get_claw.return_value = (42, 25)
    handle = server.submit(goal())
    server.jobs[0]()
    result = handle.set_aborted.call_args[0][0]
    assert result.stalled and not result.reached_goal
    assert result.position == pytest.approx(math.pi / 12)
    assert result.effort == 42
    robot.get_claw.assert_called_once()


@pytest.mark.parametrize('failed_method', ['set_claw', 'get_claw'])
def test_sdk_exception_aborts_with_stalled_result(failed_method):
    server, robot, _ = setup_bridge()
    getattr(robot, failed_method).side_effect = RuntimeError('claw failed')
    handle = server.submit(goal())
    server.jobs[0]()
    result = handle.set_aborted.call_args[0][0]
    assert result.stalled and not result.reached_goal


def test_shutdown_drains_already_admitted_claw_command():
    server, robot, bridge = setup_bridge()
    assert_shutdown_drains_command(server, robot, bridge, goal(), 'set_claw')


@pytest.mark.parametrize('phase', ['queued', 'between_polls'])
@pytest.mark.parametrize('shutdown', [False, True])
def test_cancel_and_shutdown_stop_future_claw_calls(monkeypatch, phase, shutdown):
    from lebai_driver import gripper_action
    server, robot, bridge = setup_bridge()
    handle = server.submit(goal())
    robot.get_claw.return_value = (37, 15)
    cancel_handle = server.handle(handle.get_goal(), 'g1')
    cancel = bridge.shutdown if shutdown else lambda: server.cancel_cb(cancel_handle)
    if phase == 'queued':
        cancel()
        expected_calls = []
    else:
        expected_calls = [call.set_claw(42, 50), call.get_claw()]
        monkeypatch.setattr(gripper_action, 'time', SimpleNamespace(monotonic=lambda: 0,
                                                                   sleep=lambda _: cancel()))
    server.jobs[0]()
    result = handle.set_canceled.call_args[0][0]
    assert not result.reached_goal
    assert result.effort == (37 if phase == 'between_polls' else 0)
    assert robot.mock_calls == expected_calls
    if shutdown:
        server.submit(goal(), 'later').set_rejected.assert_called_once()
        assert len(server.jobs) == 1
