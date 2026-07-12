#!/usr/bin/env python3

import argparse

import rclpy
from control_msgs.action import GripperCommand
from rclpy.action import ActionClient
from rclpy.node import Node

from lebai_tutorials_common import amplitude_to_gripper_joint


class MoveItGripperAmplitudeExample(Node):
    def __init__(self, action_name, namespace):
        super().__init__("moveit_gripper_amplitude_example", namespace=namespace)
        self._client = ActionClient(self, GripperCommand, action_name)

    def send_amplitude(self, amplitude, max_effort, timeout_sec):
        target_joint = amplitude_to_gripper_joint(amplitude)
        self.get_logger().info(
            "Sending gripper amplitude %.1f%% as active joint %.6f rad"
            % (amplitude, target_joint)
        )
        if not self._client.wait_for_server(timeout_sec=timeout_sec):
            self.get_logger().error("gripper action server is not available")
            return False

        goal = GripperCommand.Goal()
        goal.command.position = target_joint
        goal.command.max_effort = max_effort

        send_future = self._client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_future, timeout_sec=timeout_sec)
        goal_handle = send_future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error("gripper goal was rejected")
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future, timeout_sec=timeout_sec)
        result = result_future.result()
        if result is None:
            self.get_logger().error("timed out waiting for gripper result")
            return False

        reached_goal = result.result.reached_goal
        self.get_logger().info(
            "Gripper result: position=%.6f effort=%.6f reached_goal=%s stalled=%s"
            % (
                result.result.position,
                result.result.effort,
                reached_goal,
                result.result.stalled,
            )
        )
        return reached_goal


def parse_args():
    parser = argparse.ArgumentParser(
        description="Set the MoveIt gripper group using a claw amplitude percentage."
    )
    parser.add_argument("--amplitude", type=float, default=50.0, help="claw amplitude, 0..100")
    parser.add_argument("--max-effort", type=float, default=50.0)
    parser.add_argument("--namespace", default="lebai")
    parser.add_argument(
        "--action-name",
        default="lebai_gripper_controller/gripper_cmd",
        help="control_msgs/action/GripperCommand action name",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def main():
    args = parse_args()
    rclpy.init()
    node = MoveItGripperAmplitudeExample(args.action_name, args.namespace)
    try:
        ok = node.send_amplitude(args.amplitude, args.max_effort, args.timeout)
    finally:
        node.destroy_node()
        rclpy.shutdown()
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
