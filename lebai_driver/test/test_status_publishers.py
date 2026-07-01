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
