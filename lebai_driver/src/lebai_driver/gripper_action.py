import math
import time

from control_msgs.msg import GripperCommandAction, GripperCommandResult

from lebai_driver._action_server import ActionBridge
from lebai_driver.conversions import _amplitude_to_gripper_angle, _value


ACTION_NAME = '/lebai_gripper_controller/gripper_cmd'
DEFAULT_FORCE = 100.0
MAX_AMPLITUDE = 100.0
MAX_GRIPPER_POSITION = math.pi / 3.0
GOAL_TOLERANCE = 0.01
POLL_INTERVAL_SEC = 0.05
TIMEOUT_SEC = 5.0


def register_gripper_action(connection, action_name=ACTION_NAME, server_factory=None,
                            worker_factory=None):
    return GripperActionBridge(connection, action_name, server_factory, worker_factory)


class GripperActionBridge(ActionBridge):
    action_type = GripperCommandAction
    result_type = GripperCommandResult

    def _error_result(self, exc):
        return self.result_type(stalled=True)

    def _execute(self, goal, result, canceled):
        command = goal.command
        position = max(0.0, min(MAX_GRIPPER_POSITION, float(command.position)))
        amplitude = position * MAX_AMPLITUDE / MAX_GRIPPER_POSITION
        effort = float(command.max_effort)
        force = DEFAULT_FORCE if effort <= 0 else max(0.0, min(MAX_AMPLITUDE, effort))

        with self._admit_call(canceled):
            robot = self.connection.robot
        with self._admit_call(canceled):
            robot.set_claw(force, amplitude)
        deadline = time.monotonic() + TIMEOUT_SEC
        while time.monotonic() <= deadline:
            with self._admit_call(canceled):
                data = robot.get_claw()
            result.position = _amplitude_to_gripper_angle(_value(data, 1, 'amplitude', 0.0))
            result.effort = float(_value(data, 0, 'force', 0.0))
            result.reached_goal = abs(result.position - position) <= GOAL_TOLERANCE
            if result.reached_goal:
                return True
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(POLL_INTERVAL_SEC, remaining))
        result.stalled = True
        return False
