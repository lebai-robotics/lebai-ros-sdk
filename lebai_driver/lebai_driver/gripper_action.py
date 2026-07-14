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

import math
import time

from control_msgs.action import GripperCommand
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup

from lebai_driver.action_goal_owner import ActionGoalOwner


ACTION_NAME = 'lebai_gripper_controller/gripper_cmd'
DEFAULT_FORCE = 100.0
GOAL_TOLERANCE = 0.01
MAX_AMPLITUDE = 100.0
MAX_GRIPPER_POSITION = math.pi / 3.0
POLL_INTERVAL_SEC = 0.05
TIMEOUT_SEC = 5.0


def register_gripper_action(node, connection):
    bridge = GripperActionBridge(node, connection)
    return bridge.register()


class GripperActionBridge:
    def __init__(self, node, connection):
        self.node = node
        self.connection = connection
        self.callback_group = ReentrantCallbackGroup()
        self.goal_owner = ActionGoalOwner()

    def register(self):
        if hasattr(self.node, 'create_action_server'):
            return self.node.create_action_server(
                GripperCommand,
                ACTION_NAME,
                execute_callback=self.execute_callback,
                goal_callback=self.goal_callback,
                cancel_callback=self.cancel_callback,
                handle_accepted_callback=self.handle_accepted_callback,
                callback_group=self.callback_group,
            )
        return ActionServer(
            self.node,
            GripperCommand,
            ACTION_NAME,
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            handle_accepted_callback=self.handle_accepted_callback,
            callback_group=self.callback_group,
        )

    def goal_callback(self, goal_request):
        if not self.goal_owner.try_reserve(id(goal_request)):
            self.node.get_logger().error('Lebai gripper rejected concurrent goal')
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        if not self.goal_owner.is_owner(id(goal_handle.request)):
            self.node.get_logger().error('Lebai gripper rejected stale cancel')
            return CancelResponse.REJECT
        self.node.get_logger().info('Lebai gripper received cancel request')
        return CancelResponse.ACCEPT

    def handle_accepted_callback(self, goal_handle):
        goal_id = id(goal_handle.request)
        owns_goal = self.goal_owner.activate(goal_id)
        if not owns_goal:
            self.node.get_logger().error(
                'Lebai gripper dropping expired accepted goal'
            )
        try:
            # Scheduling the callback is required so rclpy can publish a final result.
            goal_handle.execute()
        except Exception:
            if owns_goal:
                self.goal_owner.release(goal_id)
            raise

    def execute_callback(self, goal_handle):
        goal_id = id(goal_handle.request)
        if not self.goal_owner.activate(goal_id):
            result = GripperCommand.Result()
            result.stalled = True
            result.reached_goal = False
            goal_handle.abort()
            return result
        try:
            return self._execute_owned_goal(goal_handle)
        finally:
            self.goal_owner.release(goal_id)

    def _execute_owned_goal(self, goal_handle):
        result = GripperCommand.Result()
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            return result

        target_position = _clamp_position(goal_handle.request.command.position)
        force = _command_force(goal_handle.request.command.max_effort)
        target_amplitude = _position_to_amplitude(target_position)

        try:
            robot = self.connection.robot
            robot.set_claw(force, target_amplitude)
            result = self._wait_for_completion(robot, goal_handle, target_position)
        except Exception:
            result.stalled = True
            result.reached_goal = False
            goal_handle.abort()
            return result

        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            return result
        if not result.reached_goal:
            result.stalled = True
            goal_handle.abort()
            return result

        goal_handle.succeed()
        return result

    def _wait_for_completion(self, robot, goal_handle, target_position):
        deadline = time.monotonic() + TIMEOUT_SEC
        result = GripperCommand.Result()

        while time.monotonic() <= deadline:
            if goal_handle.is_cancel_requested:
                return result

            result = _result_from_claw(robot.get_claw(), target_position)
            if result.reached_goal:
                return result

            _sleep_until_next_poll(deadline)

        return result


def _result_from_claw(data, target_position):
    position = _amplitude_to_position(_value(data, 1, 'amplitude', 0.0))
    result = GripperCommand.Result()
    result.position = position
    result.effort = float(_value(data, 0, 'force', 0.0))
    result.stalled = False
    result.reached_goal = abs(position - target_position) <= GOAL_TOLERANCE
    return result


def _command_force(max_effort):
    max_effort = float(max_effort)
    if max_effort <= 0.0:
        return DEFAULT_FORCE
    return max(0.0, min(MAX_AMPLITUDE, max_effort))


def _position_to_amplitude(position):
    return _clamp_position(position) * MAX_AMPLITUDE / MAX_GRIPPER_POSITION


def _amplitude_to_position(amplitude):
    amplitude = max(0.0, min(MAX_AMPLITUDE, float(amplitude)))
    return MAX_GRIPPER_POSITION * amplitude / MAX_AMPLITUDE


def _clamp_position(position):
    return max(0.0, min(MAX_GRIPPER_POSITION, float(position)))


def _sleep_until_next_poll(deadline):
    remaining = deadline - time.monotonic()
    if remaining > 0.0:
        time.sleep(min(POLL_INTERVAL_SEC, remaining))


def _value(data, index, name, default):
    if data is None:
        return default
    if isinstance(data, dict):
        return data.get(name, default)
    if hasattr(data, name):
        return getattr(data, name)
    try:
        return data[index]
    except (IndexError, KeyError, TypeError):
        return default
