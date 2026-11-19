from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from threading import Barrier
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest
from control_msgs.msg import (
    FollowJointTrajectoryAction, FollowJointTrajectoryGoal, FollowJointTrajectoryResult,
)
from genpy import Duration, Time
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from fakes import ActionHarness
from lebai_driver.connection import RobotConnection


def goal(times=(0.25, 0.75, 1.5), joints=('axis',)):
    points = [
        JointTrajectoryPoint(positions=[float(i)], velocities=[2.0], accelerations=[3.0],
                             time_from_start=Duration.from_sec(t))
        for i, t in enumerate(times)
    ]
    return FollowJointTrajectoryGoal(trajectory=JointTrajectory(joint_names=list(joints),
                                                               points=points))


def setup_bridge(**kwargs):
    from lebai_driver.trajectory_action import register_trajectory_action

    server = ActionHarness()
    robot = Mock(spec=['move_pvat', 'stop_move', 'get_robot_state', 'get_actual_joint_positions'])
    robot.get_robot_state.return_value = 5
    robot.get_actual_joint_positions.return_value = [2.0]
    connection = RobotConnection('test', robot_factory=lambda *a, **kw: robot)
    bridge = register_trajectory_action(connection, ['axis'], server_factory=server.server_factory,
                                        worker_factory=server.worker_factory, **kwargs)
    return server, robot, bridge


@pytest.mark.parametrize('override,expected', [
    ({}, '/lebai_trajectory_controller'), ({'action_name': '/robot_a/arm'}, '/robot_a/arm'),
])
def test_registration(override, expected):
    server, _, _ = setup_bridge(**override)
    assert (server.name, server.action_type, server.start_count) == (
        expected, FollowJointTrajectoryAction, 1)


@pytest.mark.parametrize('request_goal', [goal(times=()), goal(joints=['different'])])
def test_rejects_empty_or_wrong_joints_before_starting_worker(request_goal):
    server, robot, _ = setup_bridge()
    handle = server.submit(request_goal)
    handle.set_rejected.assert_called_once()
    assert server.jobs == []
    assert robot.mock_calls == []


@pytest.mark.parametrize('times,short_field', [
    ((0,), None), ((0, 0), None), ((1, 0), None),
    ((0, 1), 'positions'), ((0, 1), 'velocities'), ((0, 1), 'accelerations'),
])
def test_aborts_malformed_accepted_trajectory_without_sending_a_segment(times, short_field):
    server, robot, _ = setup_bridge()
    request = goal(times)
    if short_field:
        setattr(request.trajectory.points[-1], short_field, [])
    handle = server.submit(request)
    handle.set_accepted.assert_called_once()
    server.jobs[0]()
    result = handle.set_aborted.call_args[0][0]
    assert (result.error_code, result.error_string) == (FollowJointTrajectoryResult.INVALID_GOAL,
                                                       'invalid trajectory')
    assert robot.mock_calls == []


def test_pvat_deltas_running_states_and_final_position_tolerance(monkeypatch):
    from lebai_driver import trajectory_action
    sleep = Mock()
    monkeypatch.setattr(trajectory_action, 'time', SimpleNamespace(monotonic=lambda: 0, sleep=sleep))
    server, robot, _ = setup_bridge()
    robot.get_robot_state.side_effect = [6, 7, 5]
    robot.get_actual_joint_positions.side_effect = [[], [2.011], [1.991]]
    handle = server.submit(goal())
    server.jobs[0]()
    assert robot.mock_calls == [
        call.move_pvat([1.0], [2.0], [3.0], 0.5),
        call.move_pvat([2.0], [2.0], [3.0], 0.75),
        call.get_robot_state(), call.get_robot_state(), call.get_robot_state(),
        call.get_actual_joint_positions(), call.get_actual_joint_positions(),
        call.get_actual_joint_positions(),
    ]
    assert sleep.call_args_list == [call(0.05)] * 4
    assert handle.set_succeeded.call_args[0][0].error_code == FollowJointTrajectoryResult.SUCCESSFUL


def test_wire_goal_with_uint32_header_and_duration_crossing_zero():
    server, robot, _ = setup_bridge()
    request = goal(times=(0, 1))
    request.trajectory.points[0].time_from_start = Duration(-1, 999999999)
    request.trajectory.points[1].time_from_start = Duration(0, 1)
    request.trajectory.header.seq = 4294967295
    request.trajectory.header.stamp = Time(4294967295, 999999999)
    wire = BytesIO()
    request.serialize(wire)
    robot.get_actual_joint_positions.return_value = [1.0]
    handle = server.submit(FollowJointTrajectoryGoal().deserialize(wire.getvalue()))
    server.jobs[0]()
    assert robot.move_pvat.call_args[0][-1] == pytest.approx(2e-9, abs=1e-15)
    handle.set_succeeded.assert_called_once()


def test_scaled_deadline_is_measured_from_before_pvat(monkeypatch):
    from lebai_driver import trajectory_action
    # Final time 4.0 gives 10.0 seconds including margin. Allow one last poll at the deadline.
    clock = Mock(side_effect=[20.0, 30.0, 30.0, 30.000001])
    monkeypatch.setattr(trajectory_action, 'time', SimpleNamespace(monotonic=clock, sleep=Mock()))
    server, robot, _ = setup_bridge()
    robot.get_actual_joint_positions.return_value = [0.0]
    handle = server.submit(goal(times=(0, 4)))
    server.jobs[0]()
    robot.get_actual_joint_positions.assert_called_once()
    result = handle.set_aborted.call_args[0][0]
    assert result.error_code == FollowJointTrajectoryResult.GOAL_TOLERANCE_VIOLATED
    assert result.error_string == 'trajectory did not reach final joint state'


def test_sdk_error_aborts_with_invalid_goal():
    server, robot, _ = setup_bridge()
    robot.move_pvat.side_effect = RuntimeError('controller rejected segment')
    handle = server.submit(goal())
    server.jobs[0]()
    result = handle.set_aborted.call_args[0][0]
    assert (result.error_code, result.error_string) == (FollowJointTrajectoryResult.INVALID_GOAL,
                                                       'controller rejected segment')
    assert robot.mock_calls == [call.move_pvat([1.0], [2.0], [3.0], 0.5)]


def test_overlap_workers_enter_sdk_together():
    server, robot, _ = setup_bridge()
    both_in_sdk = Barrier(2, timeout=3)
    robot.move_pvat.side_effect = lambda *args: both_in_sdk.wait()
    first = server.submit(goal(), 'first')
    second = server.submit(goal(), 'second')
    assert len(server.jobs) == 2
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(job) for job in server.jobs]
        for future in futures:
            future.result(timeout=5)
    assert robot.move_pvat.call_count == 4
    first.set_succeeded.assert_called_once()
    second.set_succeeded.assert_called_once()


def test_cancel_stops_immediately_and_only_cancels_matching_goal_id():
    server, robot, _ = setup_bridge()
    first = server.submit(goal(), 'first')
    second = server.submit(goal(), 'second')
    cancel_handle = server.handle(first.get_goal(), 'first')
    server.cancel_cb(cancel_handle)
    assert robot.mock_calls == [call.stop_move()]
    server.jobs[0]()
    assert first.set_canceled.call_args[0][0].error_code == FollowJointTrajectoryResult.SUCCESSFUL
    assert robot.mock_calls == [call.stop_move(), call.stop_move()]
    server.jobs[1]()
    second.set_succeeded.assert_called_once()
    server.cancel_cb(cancel_handle)
    assert robot.stop_move.call_count == 2


@pytest.mark.parametrize('phase', ['queued', 'after_state_read', 'between_polls'])
def test_shutdown_cancels_workers_and_rejects_new_goals(monkeypatch, phase):
    from lebai_driver import trajectory_action
    server, robot, bridge = setup_bridge()
    handle = server.submit(goal())
    if phase == 'queued':
        bridge.shutdown()
        expected = []
    else:
        expected = [call.move_pvat([1.0], [2.0], [3.0], 0.5),
                    call.move_pvat([2.0], [2.0], [3.0], 0.75), call.get_robot_state()]
        if phase == 'after_state_read':
            def shutdown_while_reading():
                bridge.shutdown()
                return 5
            robot.get_robot_state.side_effect = shutdown_while_reading
        else:
            robot.get_robot_state.return_value = 6
            monkeypatch.setattr(trajectory_action, 'time',
                                SimpleNamespace(monotonic=lambda: 0, sleep=lambda _: bridge.shutdown()))
    server.jobs[0]()
    handle.set_canceled.assert_called_once()
    server.cancel_cb(server.handle(handle.get_goal(), 'g1'))
    server.submit(goal(), 'later').set_rejected.assert_called_once()
    assert len(server.jobs) == 1
    assert robot.mock_calls == expected
