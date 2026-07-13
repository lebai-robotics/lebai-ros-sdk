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

import threading

import pytest

from fakes import FakeRobotFactory


_TEST_ROBOT_IP = '192.0.2.1'  # TEST-NET-1; injected factories perform no I/O.


def test_robot_connection_uses_injected_factory():
    from lebai_driver.connection import RobotConnection

    factory = FakeRobotFactory()

    connection = RobotConnection(
        robot_ip=_TEST_ROBOT_IP,
        simulator=True,
        robot_factory=factory,
    )

    assert factory.calls == []
    robot = connection.robot
    assert factory.calls == [(_TEST_ROBOT_IP, True)]
    assert robot.robot_ip == _TEST_ROBOT_IP
    assert robot.simulator is True
    assert connection.robot is robot


def test_robot_connection_initializes_once_for_concurrent_first_access():
    from lebai_driver.connection import RobotConnection

    start = threading.Barrier(2)
    calls = []
    calls_lock = threading.Lock()
    second_factory_call = threading.Event()
    results = []
    errors = []

    def factory(robot_ip, simulator=False):
        with calls_lock:
            calls.append((robot_ip, simulator))
            call_number = len(calls)
        if call_number == 1:
            second_factory_call.wait(timeout=0.2)
        else:
            second_factory_call.set()
        return object()

    connection = RobotConnection(_TEST_ROBOT_IP, robot_factory=factory)

    def worker():
        try:
            start.wait(timeout=1.0)
            results.append(connection.robot)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _index in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=1.0)

    assert not errors
    assert all(not thread.is_alive() for thread in threads)
    assert calls == [(_TEST_ROBOT_IP, False)]
    assert len(results) == 2
    assert results[0] is results[1]


def test_robot_connection_retries_after_factory_failure():
    from lebai_driver.connection import RobotConnection

    robot = object()
    attempts = []

    def factory(robot_ip, simulator=False):
        attempts.append((robot_ip, simulator))
        if len(attempts) == 1:
            raise RuntimeError('initialization failed')
        return robot

    connection = RobotConnection(_TEST_ROBOT_IP, robot_factory=factory)

    with pytest.raises(RuntimeError, match='initialization failed'):
        connection.robot

    assert connection.robot is robot
    assert connection.robot is robot
    assert attempts == [
        (_TEST_ROBOT_IP, False),
        (_TEST_ROBOT_IP, False),
    ]


def test_robot_connection_does_not_expose_sdk_access_lock():
    from lebai_driver.connection import RobotConnection

    factory = FakeRobotFactory()
    connection = RobotConnection(
        robot_ip=_TEST_ROBOT_IP,
        simulator=True,
        robot_factory=factory,
    )

    assert not hasattr(connection, 'sdk_access')


def test_robot_connection_requires_robot_ip():
    from lebai_driver.connection import RobotConnection

    with pytest.raises(ValueError, match='robot_ip'):
        RobotConnection(robot_ip='')
