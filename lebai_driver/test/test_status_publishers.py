from contextlib import contextmanager

from fakes import FakeClawData, FakeJointMotionData, FakeNode, FakeRobot


def test_status_publishers_use_provided_callback_group():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.status import register_status_publishers

    node = FakeNode()
    robot = FakeRobot()
    callback_group = object()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)

    register_status_publishers(node, connection, callback_group=callback_group)

    assert node.timers
    assert {timer.callback_group for timer in node.timers} == {callback_group}


def test_status_publishers_skip_sdk_poll_when_gate_denies_access():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.status import register_status_publishers

    class DenyStatusGate:
        @contextmanager
        def status_access(self):
            yield False

    node = FakeNode()
    robot = FakeRobot()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)

    register_status_publishers(node, connection, sdk_gate=DenyStatusGate())

    node.timers[0].callback()

    assert robot.calls == []
    assert node.publishers[0].messages == []


def test_matching_kinematics_rates_share_timer_snapshot_and_timestamp():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.status import register_status_publishers

    node = FakeNode()
    robot = FakeRobot()
    robot.kin_data = FakeJointMotionData(
        actual_joint_pose=[1.0, 2.0],
        actual_joint_speed=[3.0, 4.0],
        actual_joint_torque=[5.0, 6.0],
        target_joint_pose=[7.0, 8.0],
        target_joint_speed=[9.0, 10.0],
        target_joint_torque=[11.0, 12.0],
    )
    robot.claw = FakeClawData(amplitude=50.0)
    connection = RobotConnection(
        '127.0.0.1',
        robot_factory=lambda *_args, **_kwargs: robot,
    )

    handles = register_status_publishers(node, connection)
    by_topic = {
        publisher.name: (publisher, timer)
        for publisher, timer in handles
    }
    joint_publisher, joint_timer = by_topic['status/joint_states']
    model_publisher, model_timer = by_topic['model/joint_states']
    motion_publisher, motion_timer = by_topic['status/joint_motion']

    assert joint_timer is model_timer
    assert joint_timer is motion_timer
    assert joint_timer.period == 0.05
    assert len(node.timers) == 5

    joint_timer.callback()

    assert robot.calls == [
        ('get_kin_data', (), {}),
        ('get_claw', (), {}),
    ]
    assert node.clock_now_calls == 1
    assert list(joint_publisher.messages[-1].position) == [1.0, 2.0]
    assert list(model_publisher.messages[-1].position) == [
        1.0,
        2.0,
        0.5235987755982988,
    ]
    assert list(motion_publisher.messages[-1].target_joint_positions) == [7.0, 8.0]
    stamps = [
        publisher.messages[-1].header.stamp
        for publisher in (joint_publisher, model_publisher, motion_publisher)
    ]
    assert [(stamp.sec, stamp.nanosec) for stamp in stamps] == [(12, 34)] * 3


def test_unequal_kinematics_rates_keep_independent_configured_timers():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.status import register_status_publishers

    node = FakeNode({
        'joint_state_publish_rate': 10.0,
        'joint_motion_publish_rate': 5.0,
    })
    robot = FakeRobot()
    connection = RobotConnection(
        '127.0.0.1',
        robot_factory=lambda *_args, **_kwargs: robot,
    )

    handles = register_status_publishers(node, connection)
    timers = {publisher.name: timer for publisher, timer in handles}
    joint_timer = timers['status/joint_states']
    model_timer = timers['model/joint_states']
    motion_timer = timers['status/joint_motion']

    assert len({id(joint_timer), id(model_timer), id(motion_timer)}) == 3
    assert joint_timer.period == 0.1
    assert model_timer.period == 0.1
    assert motion_timer.period == 0.2

    for timer in (joint_timer, model_timer, motion_timer):
        robot.calls.clear()
        timer.callback()
        assert [call[0] for call in robot.calls].count('get_kin_data') == 1
