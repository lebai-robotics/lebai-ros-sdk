import time

from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup


ACTION_NAME = '/lebai_trajectory_controller'
GOAL_TOLERANCE = 0.01
POLL_INTERVAL_SEC = 0.05
RUNNING_ROBOT_STATES = {6, 7}
TIMEOUT_MARGIN_SEC = 5.0
TIMEOUT_SCALE = 1.25

_COMPLETED = 'completed'
_CANCELED = 'canceled'
_TIMEOUT = 'timeout'


def register_trajectory_action(node, connection):
    bridge = TrajectoryActionBridge(node, connection)
    return bridge.register()


class TrajectoryActionBridge:
    def __init__(self, node, connection):
        self.node = node
        self.connection = connection
        self.joint_names = list(node.get_parameter('joint_names').value)
        self.callback_group = ReentrantCallbackGroup()
        self.sdk_lock = connection.sdk_access

    def register(self):
        if hasattr(self.node, 'create_action_server'):
            return self.node.create_action_server(
                FollowJointTrajectory,
                ACTION_NAME,
                execute_callback=self.execute_callback,
                goal_callback=self.goal_callback,
                cancel_callback=self.cancel_callback,
                callback_group=self.callback_group,
            )
        return ActionServer(
            self.node,
            FollowJointTrajectory,
            ACTION_NAME,
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.callback_group,
        )

    def goal_callback(self, goal_request):
        trajectory = goal_request.trajectory
        if not trajectory.points:
            self.node.get_logger().error('Lebai trajectory rejected empty goal')
            return GoalResponse.REJECT
        if list(trajectory.joint_names) != self.joint_names:
            self.node.get_logger().error('Lebai trajectory rejected invalid joints')
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, _goal_handle):
        self.node.get_logger().info('Lebai trajectory received cancel request')
        with self._sdk_access() as robot:
            robot.stop_move()
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        result = FollowJointTrajectory.Result()
        trajectory = goal_handle.request.trajectory

        if not self._is_valid_trajectory(trajectory):
            result.error_code = FollowJointTrajectory.Result.INVALID_GOAL
            result.error_string = 'invalid trajectory'
            goal_handle.abort()
            return result

        try:
            execution_start_time = time.monotonic()
            final_time_from_start = self._time_from_start(trajectory.points[-1])
            with self._sdk_access() as robot:
                previous_time = self._time_from_start(trajectory.points[0])
                for point in trajectory.points[1:]:
                    if goal_handle.is_cancel_requested:
                        robot.stop_move()
                        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                        goal_handle.canceled()
                        return result

                    current_time = self._time_from_start(point)
                    robot.move_pvat(
                        list(point.positions),
                        list(point.velocities),
                        list(point.accelerations),
                        current_time - previous_time,
                    )
                    previous_time = current_time

            self._wait_for_planned_duration(
                goal_handle,
                execution_start_time,
                final_time_from_start,
            )
            if goal_handle.is_cancel_requested:
                with self._sdk_access() as robot:
                    robot.stop_move()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                goal_handle.canceled()
                return result

            completion = self._wait_for_completion(
                goal_handle,
                list(trajectory.points[-1].positions),
                execution_start_time,
                final_time_from_start,
            )
            if completion == _CANCELED:
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                goal_handle.canceled()
                return result
            if completion == _TIMEOUT:
                result.error_code = FollowJointTrajectory.Result.GOAL_TOLERANCE_VIOLATED
                result.error_string = 'trajectory did not reach final joint state'
                goal_handle.abort()
                return result
        except Exception as exc:
            result.error_code = FollowJointTrajectory.Result.INVALID_GOAL
            result.error_string = str(exc)
            goal_handle.abort()
            return result

        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
        goal_handle.succeed()
        return result

    def _is_valid_trajectory(self, trajectory):
        if list(trajectory.joint_names) != self.joint_names:
            return False
        if len(trajectory.points) < 2:
            return False

        previous_time = None
        joint_count = len(self.joint_names)
        for point in trajectory.points:
            if (
                len(point.positions) != joint_count
                or len(point.velocities) != joint_count
                or len(point.accelerations) != joint_count
            ):
                return False

            current_time = self._time_from_start(point)
            if previous_time is not None and current_time <= previous_time:
                return False
            previous_time = current_time

        return True

    def _sdk_access(self):
        if hasattr(self.sdk_lock, '__enter__'):
            return self.sdk_lock
        return self.sdk_lock()

    @staticmethod
    def _time_from_start(point):
        return point.time_from_start.sec + point.time_from_start.nanosec / 1_000_000_000

    def _wait_for_planned_duration(
        self,
        goal_handle,
        execution_start_time,
        final_time_from_start,
    ):
        wakeup_time = execution_start_time + final_time_from_start
        now = time.monotonic()
        while now < wakeup_time:
            if goal_handle.is_cancel_requested:
                return
            time.sleep(wakeup_time - now)
            now = time.monotonic()

    def _wait_for_completion(
        self,
        goal_handle,
        final_positions,
        execution_start_time,
        final_time_from_start,
    ):
        deadline = execution_start_time + max(
            TIMEOUT_MARGIN_SEC,
            final_time_from_start * TIMEOUT_SCALE + TIMEOUT_MARGIN_SEC,
        )
        sdk_motion_finished = False

        while time.monotonic() <= deadline:
            if goal_handle.is_cancel_requested:
                with self._sdk_access() as robot:
                    robot.stop_move()
                return _CANCELED

            if self._final_positions_reached(final_positions):
                return _COMPLETED

            if not sdk_motion_finished:
                with self._sdk_access() as robot:
                    robot_state = int(robot.get_robot_state())
                if robot_state in RUNNING_ROBOT_STATES:
                    self._sleep_until_next_poll(deadline)
                    continue
                sdk_motion_finished = True

            self._sleep_until_next_poll(deadline)

        return _TIMEOUT

    def _final_positions_reached(self, final_positions):
        with self._sdk_access() as robot:
            actual_positions = list(robot.get_actual_joint_positions())
        if len(actual_positions) != len(final_positions):
            return False

        return all(
            abs(actual - expected) <= GOAL_TOLERANCE
            for actual, expected in zip(actual_positions, final_positions)
        )

    @staticmethod
    def _sleep_until_next_poll(deadline):
        remaining = deadline - time.monotonic()
        if remaining > 0.0:
            time.sleep(min(POLL_INTERVAL_SEC, remaining))
