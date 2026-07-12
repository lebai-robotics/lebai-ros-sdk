import json
import time
import uuid

from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup

from lebai_driver.action_goal_owner import ActionGoalOwner
from lebai_driver.parameters import DEFAULT_JOINT_NAMES


ACTION_NAME = 'lebai_trajectory_controller/follow_joint_trajectory'
GOAL_TOLERANCE = 0.01
POLL_INTERVAL_SEC = 0.05
RUNNING_ROBOT_STATES = {6, 7}
TIMEOUT_MARGIN_SEC = 5.0
TIMEOUT_SCALE = 1.25
TRAJECTORY_RESOURCE_DIR = ''
TRAJECTORY_RESOURCE_PREFIX = 'ros2_pvat_'

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
        self.joint_names = list(DEFAULT_JOINT_NAMES)
        self.callback_group = ReentrantCallbackGroup()
        self.sdk_lock = connection.sdk_access
        self.goal_owner = ActionGoalOwner()

    def register(self):
        if hasattr(self.node, 'create_action_server'):
            return self.node.create_action_server(
                FollowJointTrajectory,
                ACTION_NAME,
                execute_callback=self.execute_callback,
                goal_callback=self.goal_callback,
                cancel_callback=self.cancel_callback,
                handle_accepted_callback=self.handle_accepted_callback,
                callback_group=self.callback_group,
            )
        return ActionServer(
            self.node,
            FollowJointTrajectory,
            ACTION_NAME,
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            handle_accepted_callback=self.handle_accepted_callback,
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
        if not self.goal_owner.try_reserve(id(goal_request)):
            self.node.get_logger().error('Lebai trajectory rejected concurrent goal')
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        if not self.goal_owner.is_owner(id(goal_handle.request)):
            self.node.get_logger().error('Lebai trajectory rejected stale cancel')
            return CancelResponse.REJECT
        self.node.get_logger().info('Lebai trajectory received cancel request')
        return CancelResponse.ACCEPT

    def handle_accepted_callback(self, goal_handle):
        goal_id = id(goal_handle.request)
        owns_goal = self.goal_owner.activate(goal_id)
        if not owns_goal:
            self.node.get_logger().error(
                'Lebai trajectory dropping expired accepted goal'
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
            result = FollowJointTrajectory.Result()
            result.error_code = FollowJointTrajectory.Result.INVALID_GOAL
            result.error_string = 'goal does not own trajectory action'
            goal_handle.abort()
            return result
        try:
            return self._execute_owned_goal(goal_handle)
        finally:
            self.goal_owner.release(goal_id)

    def _execute_owned_goal(self, goal_handle):
        result = FollowJointTrajectory.Result()
        trajectory = goal_handle.request.trajectory

        if not self._is_valid_trajectory(trajectory):
            result.error_code = FollowJointTrajectory.Result.INVALID_GOAL
            result.error_string = 'invalid trajectory'
            goal_handle.abort()
            return result

        resource_name = None
        trajectory_saved = False
        motion_started = False
        try:
            final_time_from_start = self._time_from_start(trajectory.points[-1])
            if goal_handle.is_cancel_requested:
                with self._sdk_access() as robot:
                    robot.stop_move()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                goal_handle.canceled()
                return result

            resource_name = self._new_trajectory_resource_name()
            # Controller-side playback owns PVAT queue backpressure and lookahead.
            with self._sdk_access() as robot:
                self._save_controller_trajectory(robot, trajectory, resource_name)
            trajectory_saved = True

            if goal_handle.is_cancel_requested:
                with self._sdk_access() as robot:
                    robot.stop_move()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                goal_handle.canceled()
                return result

            with self._sdk_access() as robot:
                execution_start_time = time.monotonic()
                motion_started = True
                robot.move_trajectory(
                    resource_name,
                    TRAJECTORY_RESOURCE_DIR,
                )

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
                with self._sdk_access() as robot:
                    robot.stop_move()
                result.error_code = FollowJointTrajectory.Result.GOAL_TOLERANCE_VIOLATED
                result.error_string = 'trajectory did not reach final joint state'
                goal_handle.abort()
                return result
        except Exception as exc:
            if motion_started:
                try:
                    with self._sdk_access() as robot:
                        robot.stop_move()
                except Exception as stop_exc:
                    self.node.get_logger().error(
                        'Lebai trajectory stop failed: %s' % stop_exc
                    )
            result.error_code = FollowJointTrajectory.Result.INVALID_GOAL
            result.error_string = str(exc)
            goal_handle.abort()
            return result
        finally:
            if trajectory_saved:
                try:
                    with self._sdk_access() as robot:
                        self._delete_controller_trajectory(robot, resource_name)
                except Exception as exc:
                    self.node.get_logger().error(
                        'Lebai temporary trajectory cleanup failed: %s' % exc
                    )

        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
        goal_handle.succeed()
        return result

    def _save_controller_trajectory(self, robot, trajectory, resource_name):
        previous_time = self._time_from_start(trajectory.points[0])
        segments = []
        for point in trajectory.points[1:]:
            current_time = self._time_from_start(point)
            segments.append({
                'duration': current_time - previous_time,
                'joints': [
                    {
                        'pose': float(position),
                        'velocity': float(velocity),
                        'acc': float(acceleration),
                    }
                    for position, velocity, acceleration in zip(
                        point.positions,
                        point.velocities,
                        point.accelerations,
                    )
                ],
            })
            previous_time = current_time

        request = {
            'name': resource_name,
            'data': {
                'kind': 'PVAT',
                'data': segments,
            },
            'dir': TRAJECTORY_RESOURCE_DIR,
        }
        error_code, error_message = robot.call(
            'save_trajectory',
            json.dumps(request, separators=(',', ':'), allow_nan=False),
        )
        if error_code != 0:
            raise RuntimeError(error_message)

    def _delete_controller_trajectory(self, robot, resource_name):
        request = {
            'name': resource_name,
            'dir': TRAJECTORY_RESOURCE_DIR,
        }
        try:
            error_code, error_message = robot.call(
                'save_trajectory',
                json.dumps(request, separators=(',', ':')),
            )
            if error_code != 0:
                raise RuntimeError(error_message)
        except Exception as exc:
            self.node.get_logger().error(
                'Lebai temporary trajectory cleanup failed: %s' % exc
            )

    @staticmethod
    def _new_trajectory_resource_name():
        return TRAJECTORY_RESOURCE_PREFIX + uuid.uuid4().hex[:16]

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
