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

from threading import Event, Lock, Thread
import time

from lebai_interfaces.srv import Command, WaitMove
import pytest
import rclpy
from rclpy.node import Node

from fakes import FakeRobot, FakeRobotFactory


class _PendingWaitRobot(FakeRobot):
    def __init__(self):
        super().__init__()
        self.wait_started = Event()
        self.release_wait = Event()
        self.stop_move_called = Event()
        self.estop_called = Event()
        self._poll_lock = Lock()
        self._polled_motion_ids = set()

    def wait_move(self, motion_id=0):
        self._record('wait_move', motion_id)
        self.wait_started.set()
        self.release_wait.wait(timeout=2.0)

    def get_motion_state(self, motion_id):
        self._record('get_motion_state', motion_id)
        with self._poll_lock:
            self._polled_motion_ids.add(motion_id)
        self.wait_started.set()
        if self.release_wait.is_set():
            return 'FINISHED'
        return 'RUNNING'

    def polled_motion_count(self):
        with self._poll_lock:
            return len(self._polled_motion_ids)

    def stop_move(self):
        super().stop_move()
        self.stop_move_called.set()

    def estop(self):
        super().estop()
        self.estop_called.set()


def test_driver_node_declares_runtime_parameters():
    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    try:
        node = LebaiDriverNode(robot_factory=FakeRobotFactory())

        expected_names = {
            'robot_ip',
            'simulator',
            'namespace',
            'joint_state_publish_rate',
            'robot_state_publish_rate',
            'joint_motion_publish_rate',
            'io_state_publish_rate',
            'gripper_state_publish_rate',
            'gripper_joint_name',
            'io_state_device',
            'io_state_digital_input_count',
            'io_state_digital_output_count',
            'io_state_analog_input_count',
            'io_state_analog_output_count',
            'io_state_dio_count',
        }

        for name in expected_names:
            assert node.has_parameter(name)
        assert not node.has_parameter('joint_names')
        assert node.get_parameter('gripper_joint_name').value == 'gripper_r_joint1'
        assert node.get_name() == 'lebai_driver'
        assert node.trajectory_action is not None
        assert node.gripper_action is not None
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_node_separates_status_and_service_callback_groups():
    from rclpy.callback_groups import (
        MutuallyExclusiveCallbackGroup,
        ReentrantCallbackGroup,
    )

    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    try:
        node = LebaiDriverNode(robot_factory=FakeRobotFactory())

        assert isinstance(node.status_callback_group, MutuallyExclusiveCallbackGroup)
        assert isinstance(node.service_callback_group, MutuallyExclusiveCallbackGroup)
        assert node.status_callback_group is not node.service_callback_group
        assert isinstance(node.wait_move_callback_group, ReentrantCallbackGroup)
        assert node.wait_move_callback_group is not node.service_callback_group
        assert node.wait_move_callback_group is not node.status_callback_group
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_node_prioritizes_model_joint_state_callback_group():
    from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    try:
        node = LebaiDriverNode(robot_factory=FakeRobotFactory())

        assert isinstance(
            node.model_state_callback_group,
            MutuallyExclusiveCallbackGroup,
        )
        assert node.model_state_callback_group is not node.status_callback_group
        assert node.model_state_callback_group is not node.service_callback_group
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_node_uses_separate_status_connection():
    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    robot_factory = FakeRobotFactory()
    try:
        node = LebaiDriverNode(robot_factory=robot_factory)

        assert node.status_connection is not node.connection
        assert node.status_connection.robot_ip == node.connection.robot_ip
        assert node.status_connection.simulator == node.connection.simulator

        _status_robot = node.status_connection.robot
        _command_robot = node.connection.robot

        assert _status_robot is not _command_robot
        assert robot_factory.calls == [
            ('127.0.0.1', False),
            ('127.0.0.1', False),
        ]
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_main_uses_multithreaded_executor_for_actions():
    from rclpy.executors import MultiThreadedExecutor

    from lebai_driver.driver_node import create_executor

    rclpy.init()
    executor = None
    try:
        executor = create_executor()
        assert isinstance(executor, MultiThreadedExecutor)
    finally:
        if executor is not None:
            executor.shutdown()
        rclpy.shutdown()


@pytest.mark.parametrize(
    ('service_name', 'event_name'),
    [
        ('/motion/stop_move', 'stop_move_called'),
        ('/start_stop/estop', 'estop_called'),
    ],
)
def test_pending_wait_does_not_block_safety_commands(service_name, event_name):
    from rclpy.executors import MultiThreadedExecutor

    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    robot = _PendingWaitRobot()
    driver = None
    probe = None
    executor = None
    spin_thread = None
    try:
        driver = LebaiDriverNode(
            robot_factory=lambda *_args, **_kwargs: robot,
        )
        probe = Node('wait_move_interrupt_probe')
        executor = MultiThreadedExecutor(num_threads=4)
        executor.add_node(driver)
        executor.add_node(probe)
        spin_thread = Thread(target=executor.spin, daemon=True)
        spin_thread.start()

        wait_client = probe.create_client(WaitMove, '/motion/wait_move')
        command_client = probe.create_client(Command, service_name)
        assert wait_client.wait_for_service(timeout_sec=1.0)
        assert command_client.wait_for_service(timeout_sec=1.0)

        wait_futures = [
            wait_client.call_async(
                WaitMove.Request(motion_id=motion_id, timeout_sec=2.0)
            )
            for motion_id in range(123, 127)
        ]
        assert robot.wait_started.wait(timeout=0.25)
        assert _wait_until(
            lambda: robot.polled_motion_count() == len(wait_futures)
            or sum(future.done() for future in wait_futures) >= 3,
            timeout_sec=1.0,
        )

        command_future = command_client.call_async(Command.Request())
        command_called = getattr(robot, event_name)
        assert command_called.wait(timeout=0.25)
        assert sum(future.done() for future in wait_futures) == 3

        robot.release_wait.set()
        assert _wait_until(
            lambda: all(future.done() for future in wait_futures),
            timeout_sec=1.0,
        )
        assert _wait_until(command_future.done, timeout_sec=1.0)
        wait_results = [future.result().result for future in wait_futures]
        assert sum(result.success for result in wait_results) == 1
        assert {
            result.message
            for result in wait_results
            if not result.success
        } == {'another wait_move request is active'}
        assert command_future.result().result.success is True
    finally:
        robot.release_wait.set()
        if executor is not None:
            executor.shutdown(timeout_sec=1.0)
        if spin_thread is not None:
            spin_thread.join(timeout=1.0)
        if probe is not None:
            probe.destroy_node()
        if driver is not None:
            driver.destroy_node()
        rclpy.shutdown()


def _wait_until(predicate, timeout_sec):
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return predicate()
