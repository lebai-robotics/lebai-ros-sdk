import pytest

from fakes import FakeRobotFactory


def test_robot_connection_uses_injected_factory():
    from lebai_driver.connection import RobotConnection

    factory = FakeRobotFactory()

    connection = RobotConnection(
        robot_ip='192.168.1.100',
        simulator=True,
        robot_factory=factory,
    )

    assert factory.calls == []
    robot = connection.robot
    assert factory.calls == [('192.168.1.100', True)]
    assert robot.robot_ip == '192.168.1.100'
    assert robot.simulator is True
    assert connection.robot is robot


def test_robot_connection_requires_robot_ip():
    from lebai_driver.connection import RobotConnection

    with pytest.raises(ValueError, match='robot_ip'):
        RobotConnection(robot_ip='')
