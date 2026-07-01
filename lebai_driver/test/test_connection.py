import pytest
import threading

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


def test_robot_connection_sdk_access_returns_cached_robot():
    from lebai_driver.connection import RobotConnection

    factory = FakeRobotFactory()
    connection = RobotConnection(
        robot_ip='192.168.1.100',
        simulator=True,
        robot_factory=factory,
    )

    with connection.sdk_access() as robot:
        assert robot.robot_ip == '192.168.1.100'

    assert factory.calls == [('192.168.1.100', True)]
    assert connection.robot is robot


def test_robot_connection_sdk_access_serializes_threads():
    from lebai_driver.connection import RobotConnection

    factory = FakeRobotFactory()
    connection = RobotConnection(
        robot_ip='192.168.1.100',
        simulator=True,
        robot_factory=factory,
    )
    entered = threading.Event()
    release = threading.Event()
    worker_entered = threading.Event()

    def worker():
        entered.set()
        with connection.sdk_access():
            worker_entered.set()

    with connection.sdk_access():
        thread = threading.Thread(target=worker)
        thread.start()
        assert entered.wait(timeout=1.0)
        assert not worker_entered.wait(timeout=0.05)
        release.set()

    thread.join(timeout=1.0)

    assert release.is_set()
    assert worker_entered.is_set()


def test_robot_connection_requires_robot_ip():
    from lebai_driver.connection import RobotConnection

    with pytest.raises(ValueError, match='robot_ip'):
        RobotConnection(robot_ip='')
