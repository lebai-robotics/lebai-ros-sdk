from concurrent.futures import ThreadPoolExecutor
import sys
from threading import Event, Lock
from types import SimpleNamespace

import pytest

from fakes import FakeRobotFactory


def test_robot_connection_uses_injected_factory_once_on_first_access():
    from lebai_driver.connection import RobotConnection

    factory = FakeRobotFactory()
    connection = RobotConnection('192.168.1.100', simulator=True, robot_factory=factory)

    assert factory.calls == []
    robot = connection.robot
    assert robot.robot_ip == '192.168.1.100'
    assert robot.simulator is True
    assert connection.robot is robot
    assert factory.calls == [('192.168.1.100', True)]


def test_robot_connection_lazily_uses_pylebai_robot(monkeypatch):
    monkeypatch.setitem(sys.modules, 'pylebai', None)
    from lebai_driver.connection import RobotConnection

    connection = RobotConnection('127.0.0.1')
    factory = FakeRobotFactory()
    monkeypatch.setitem(sys.modules, 'pylebai', SimpleNamespace(Robot=factory))

    connection.robot
    assert factory.calls == [('127.0.0.1', False)]


def test_concurrent_first_access_constructs_one_robot(monkeypatch):
    from lebai_driver.connection import RobotConnection

    factory = FakeRobotFactory()
    factory_entered = Event()
    allow_factory_return = Event()
    concurrent_access = Event()
    initialization_lock = Lock()

    class ObservedLock:
        def __enter__(self):
            if initialization_lock.locked():
                concurrent_access.set()
            assert initialization_lock.acquire(timeout=5)

        def __exit__(self, *exc_info):
            initialization_lock.release()

    def blocking_factory(robot_ip, simulator=False):
        robot = factory(robot_ip, simulator=simulator)
        if len(factory.calls) == 1:
            factory_entered.set()
            assert allow_factory_return.wait(timeout=5)
        else:
            concurrent_access.set()
        return robot

    connection = RobotConnection('127.0.0.1', robot_factory=blocking_factory)
    monkeypatch.setattr(connection, '_initialization_lock', ObservedLock(), raising=False)

    with ThreadPoolExecutor(max_workers=2) as executor:
        first_access = executor.submit(lambda: connection.robot)
        try:
            assert factory_entered.wait(timeout=5)
            second_access = executor.submit(lambda: connection.robot)
            assert concurrent_access.wait(timeout=5)
        finally:
            allow_factory_return.set()
        assert first_access.result(timeout=5) is second_access.result(timeout=5)

    assert factory.calls == [('127.0.0.1', False)]


def test_robot_connection_does_not_expose_sdk_access_lock():
    from lebai_driver.connection import RobotConnection

    connection = RobotConnection('127.0.0.1', robot_factory=FakeRobotFactory())

    assert not hasattr(connection, 'sdk_access')
    assert not hasattr(connection, 'sdk_lock')


def test_robot_connection_requires_robot_ip():
    from lebai_driver.connection import RobotConnection

    with pytest.raises(ValueError, match='robot_ip is required'):
        RobotConnection('')
