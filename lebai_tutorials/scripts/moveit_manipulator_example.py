#!/usr/bin/env python3
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


import argparse

import rclpy
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, JointConstraint, MoveItErrorCodes
from rclpy.action import ActionClient
from rclpy.node import Node

from lebai_tutorials_common import MANIPULATOR_JOINT_NAMES, parse_joint_positions


DEFAULT_TARGET = [-0.35, -1.0, 1.2, -1.1, -0.6, 0.0]


def make_joint_goal(joint_positions, plan_only):
    goal = MoveGroup.Goal()
    goal.request.group_name = "manipulator"
    goal.request.num_planning_attempts = 10
    goal.request.allowed_planning_time = 5.0
    goal.request.max_velocity_scaling_factor = 0.2
    goal.request.max_acceleration_scaling_factor = 0.2

    constraints = Constraints()
    constraints.name = "joint_space_goal"
    for joint_name, position in zip(MANIPULATOR_JOINT_NAMES, joint_positions):
        joint_constraint = JointConstraint()
        joint_constraint.joint_name = joint_name
        joint_constraint.position = float(position)
        joint_constraint.tolerance_above = 0.01
        joint_constraint.tolerance_below = 0.01
        joint_constraint.weight = 1.0
        constraints.joint_constraints.append(joint_constraint)
    goal.request.goal_constraints.append(constraints)

    goal.planning_options.plan_only = plan_only
    goal.planning_options.planning_scene_diff.is_diff = True
    goal.planning_options.planning_scene_diff.robot_state.is_diff = True
    goal.planning_options.replan = False
    return goal


class MoveItManipulatorExample(Node):
    def __init__(self, action_name, namespace):
        super().__init__("moveit_manipulator_example", namespace=namespace)
        self._client = ActionClient(self, MoveGroup, action_name)

    def move_to_joint_positions(self, joint_positions, plan_only, timeout_sec):
        self.get_logger().info("Sending manipulator target: %s" % joint_positions)
        if not self._client.wait_for_server(timeout_sec=timeout_sec):
            self.get_logger().error("MoveGroup action server is not available")
            return False

        goal = make_joint_goal(joint_positions, plan_only)
        send_future = self._client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_future, timeout_sec=timeout_sec)
        goal_handle = send_future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error("MoveGroup goal was rejected")
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future, timeout_sec=timeout_sec)
        result = result_future.result()
        if result is None:
            self.get_logger().error("timed out waiting for MoveGroup result")
            return False

        error_code = result.result.error_code.val
        if error_code != MoveItErrorCodes.SUCCESS:
            self.get_logger().error("MoveGroup failed with error code %d" % error_code)
            return False

        if plan_only:
            self.get_logger().info("Manipulator plan was computed successfully.")
        else:
            self.get_logger().info("Manipulator trajectory was executed successfully.")
        return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plan and optionally execute a MoveIt manipulator joint-space goal."
    )
    parser.add_argument(
        "--joints",
        default=",".join(str(value) for value in DEFAULT_TARGET),
        help="six comma-separated joint target positions in radians",
    )
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--namespace", default="lebai")
    parser.add_argument(
        "--action-name",
        default="move_action",
        help="moveit_msgs/action/MoveGroup action name",
    )
    parser.add_argument("--timeout", type=float, default=60.0)
    return parser.parse_args()


def main():
    args = parse_args()
    joint_positions = parse_joint_positions(args.joints)
    rclpy.init()
    node = MoveItManipulatorExample(args.action_name, args.namespace)
    try:
        ok = node.move_to_joint_positions(joint_positions, args.plan_only, args.timeout)
    finally:
        node.destroy_node()
        rclpy.shutdown()
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
