from fakes import FakeNode, FakeRobot


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


def test_status_publishers_can_prioritize_model_joint_state_group():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.status import register_status_publishers

    node = FakeNode()
    connection = RobotConnection(
        '127.0.0.1',
        robot_factory=lambda *_args, **_kwargs: FakeRobot(),
    )
    status_callback_group = object()
    model_state_callback_group = object()

    register_status_publishers(
        node,
        connection,
        callback_group=status_callback_group,
        model_state_callback_group=model_state_callback_group,
    )

    timer_groups_by_topic = {
        publisher.name: timer.callback_group
        for publisher, timer in zip(node.publishers, node.timers)
    }

    assert timer_groups_by_topic['status/joint_states'] is model_state_callback_group
    assert timer_groups_by_topic['model/joint_states'] is model_state_callback_group
    assert timer_groups_by_topic['status/joint_motion'] is status_callback_group
    assert timer_groups_by_topic['status/robot'] is status_callback_group
