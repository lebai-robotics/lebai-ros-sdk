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

from contextlib import suppress
import os
import time


_ACTION_SERVICE_SUFFIXES = {
    "/_action/cancel_goal",
    "/_action/get_result",
    "/_action/send_goal",
}


class _NoIoConnection:
    @property
    def robot(self):
        raise AssertionError("action registration must not access a controller")

    def sdk_access(self):
        raise AssertionError("action registration must not access a controller")


def _action_service_graph(node):
    graph = {}
    for service_name, service_types in node.get_service_names_and_types():
        for suffix in _ACTION_SERVICE_SUFFIXES:
            if service_name.endswith(suffix):
                action_name = service_name[:-len(suffix)]
                graph.setdefault(action_name, {})[suffix] = tuple(service_types)
                break
    return graph


def _spin_until(executor, predicate, timeout_sec=5.0):
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        executor.spin_once(timeout_sec=0.05)
        if predicate():
            return
    raise AssertionError("timed out waiting for the action service graph")


def test_driver_action_service_graphs_follow_their_node_namespaces(monkeypatch):
    monkeypatch.setenv("ROS_DOMAIN_ID", str(150 + os.getpid() % 50))

    import rclpy
    from rclpy.executors import SingleThreadedExecutor

    from lebai_driver.gripper_action import register_gripper_action
    from lebai_driver.trajectory_action import register_trajectory_action

    expected_actions = {
        "/robot_1/lebai_trajectory_controller/follow_joint_trajectory",
        "/robot_1/lebai_gripper_controller/gripper_cmd",
        "/robot_2/lebai_trajectory_controller/follow_joint_trajectory",
        "/robot_2/lebai_gripper_controller/gripper_cmd",
    }
    forbidden_actions = {
        "/lebai_trajectory_controller",
        "/lebai_trajectory_controller/follow_joint_trajectory",
        "/lebai_gripper_controller/gripper_cmd",
    }

    rclpy.init()
    executor = SingleThreadedExecutor()
    nodes = []
    servers = []
    try:
        for namespace in ("robot_1", "robot_2"):
            node = rclpy.create_node("lebai_action_namespace_probe", namespace=namespace)
            nodes.append(node)
            executor.add_node(node)
            servers.append(register_trajectory_action(node, _NoIoConnection()))
            servers.append(register_gripper_action(node, _NoIoConnection()))

        _spin_until(
            executor,
            lambda: expected_actions.issubset(_action_service_graph(nodes[0])),
        )
        graph = _action_service_graph(nodes[0])

        assert expected_actions.issubset(graph)
        assert forbidden_actions.isdisjoint(graph)
        for action_name in expected_actions:
            assert set(graph[action_name]) == _ACTION_SERVICE_SUFFIXES

        robot_1_services = {
            action_name + suffix
            for action_name in expected_actions
            if action_name.startswith("/robot_1/")
            for suffix in graph[action_name]
        }
        robot_2_services = {
            action_name + suffix
            for action_name in expected_actions
            if action_name.startswith("/robot_2/")
            for suffix in graph[action_name]
        }
        assert robot_1_services.isdisjoint(robot_2_services)
    finally:
        for server in reversed(servers):
            with suppress(Exception):
                server.destroy()
        for node in reversed(nodes):
            with suppress(Exception):
                executor.remove_node(node)
            with suppress(Exception):
                node.destroy_node()
        with suppress(Exception):
            executor.shutdown()
        if rclpy.ok():
            with suppress(Exception):
                rclpy.shutdown()
