import time

from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryResult

from lebai_driver._action_server import ActionBridge


ACTION_NAME = '/lebai_trajectory_controller'
GOAL_TOLERANCE = 0.01
POLL_INTERVAL_SEC = 0.05
RUNNING_ROBOT_STATES = {6, 7}
TIMEOUT_MARGIN_SEC = 5.0
TIMEOUT_SCALE = 1.25


def register_trajectory_action(connection, joint_names, action_name=ACTION_NAME,
                               server_factory=None, worker_factory=None):
    return TrajectoryActionBridge(connection, joint_names, action_name, server_factory, worker_factory)


class TrajectoryActionBridge(ActionBridge):
    action_type = FollowJointTrajectoryAction
    result_type = FollowJointTrajectoryResult

    def __init__(self, connection, joint_names, action_name, server_factory, worker_factory):
        self.joint_names = list(joint_names)
        super().__init__(connection, action_name, server_factory, worker_factory)

    def _rejection(self, goal):
        if not goal.trajectory.points:
            return self.result_type(error_code=self.result_type.INVALID_GOAL,
                                    error_string='empty trajectory')
        if list(goal.trajectory.joint_names) != self.joint_names:
            return self.result_type(error_code=self.result_type.INVALID_JOINTS,
                                    error_string='invalid joints')
        return None

    def _on_cancel(self):
        if self._shutdown.is_set():
            return
        robot = self.connection.robot
        if not self._shutdown.is_set():
            robot.stop_move()

    def _error_result(self, exc):
        return self.result_type(error_code=self.result_type.INVALID_GOAL, error_string=str(exc))

    def _valid_points(self, points):
        if len(points) < 2:
            return False
        previous_time = None
        for point in points:
            if any(len(values) != len(self.joint_names)
                   for values in (point.positions, point.velocities, point.accelerations)):
                return False
            current_time = point.time_from_start.to_sec()
            if previous_time is not None and current_time <= previous_time:
                return False
            previous_time = current_time
        return True

    def _execute(self, goal, result, check_active):
        points = goal.trajectory.points
        if not self._valid_points(points):
            result.error_code = result.INVALID_GOAL
            result.error_string = 'invalid trajectory'
            return False

        check_active()
        robot = self.connection.robot
        start = time.monotonic()
        previous_time = points[0].time_from_start.to_sec()
        for point in points[1:]:
            current_time = point.time_from_start.to_sec()
            check_active()
            robot.move_pvat(list(point.positions), list(point.velocities),
                            list(point.accelerations), current_time - previous_time)
            previous_time = current_time

        deadline = start + max(TIMEOUT_MARGIN_SEC, previous_time * TIMEOUT_SCALE + TIMEOUT_MARGIN_SEC)
        target = points[-1].positions
        motion_finished = False
        while time.monotonic() <= deadline:
            check_active()
            if not motion_finished:
                motion_finished = int(robot.get_robot_state()) not in RUNNING_ROBOT_STATES
            if motion_finished:
                check_active()
                actual = list(robot.get_actual_joint_positions())
                if len(actual) == len(target) and all(
                        abs(a - b) <= GOAL_TOLERANCE for a, b in zip(actual, target)):
                    result.error_code = result.SUCCESSFUL
                    return True
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(POLL_INTERVAL_SEC, remaining))

        result.error_code = result.GOAL_TOLERANCE_VIOLATED
        result.error_string = 'trajectory did not reach final joint state'
        return False
