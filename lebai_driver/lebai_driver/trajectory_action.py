from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup


ACTION_NAME = '/lebai_trajectory_controller'


def register_trajectory_action(node, connection):
    bridge = TrajectoryActionBridge(node, connection)
    return bridge.register()


class TrajectoryActionBridge:
    def __init__(self, node, connection):
        self.node = node
        self.connection = connection
        self.joint_names = list(node.get_parameter('joint_names').value)
        self.callback_group = ReentrantCallbackGroup()

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
        self.connection.robot.stop_move()
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
            robot = self.connection.robot
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

    @staticmethod
    def _time_from_start(point):
        return point.time_from_start.sec + point.time_from_start.nanosec / 1_000_000_000
