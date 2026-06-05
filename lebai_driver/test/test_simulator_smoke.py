import os
import time

import pytest


pytestmark = pytest.mark.integration


def test_driver_talks_to_simulator_topics_and_services():
    robot_ip = os.environ.get('LEBAI_TEST_ROBOT_IP')
    if not robot_ip:
        pytest.skip('LEBAI_TEST_ROBOT_IP is not set')

    import rclpy
    from rclpy.executors import MultiThreadedExecutor

    from lebai_driver.driver_node import LebaiDriverNode
    from lebai_interfaces.msg import RobotState
    from lebai_interfaces.srv import Command, GetClaw, GetRunningMotion, SetClaw
    from sensor_msgs.msg import JointState

    args = [
        '--ros-args',
        '-r', '__ns:=/lebai',
        '-p', 'robot_ip:=%s' % robot_ip,
        '-p', 'simulator:=true',
    ]

    rclpy.init(args=args)
    executor = MultiThreadedExecutor(num_threads=2)
    driver = None
    probe = None
    try:
        driver = LebaiDriverNode()
        probe = rclpy.create_node('lebai_simulator_smoke_probe')
        executor.add_node(driver)
        executor.add_node(probe)

        assert driver.connection.robot_ip == robot_ip
        assert driver.connection.simulator is True

        joint_states = []
        robot_states = []
        probe.create_subscription(
            JointState,
            '/lebai/status/joint_states',
            joint_states.append,
            10,
        )
        probe.create_subscription(
            RobotState,
            '/lebai/status/robot',
            robot_states.append,
            10,
        )

        _spin_until(executor, lambda: joint_states and robot_states)

        running_motion = _call_service(
            executor,
            probe,
            GetRunningMotion,
            '/lebai/motion/get_running_motion',
            GetRunningMotion.Request(),
        )
        assert running_motion.result.success is True

        claw_before = _call_service(
            executor,
            probe,
            GetClaw,
            '/lebai/claw/get_claw',
            GetClaw.Request(),
        )
        assert claw_before.result.success is True
        assert claw_before.state.connected is True

        set_claw_request = SetClaw.Request()
        set_claw_request.force = 50.0
        set_claw_request.amplitude = 40.0
        set_claw_result = _call_service(
            executor,
            probe,
            SetClaw,
            '/lebai/claw/set_claw',
            set_claw_request,
        )
        assert set_claw_result.result.success is True

        claw_after = _call_service(
            executor,
            probe,
            GetClaw,
            '/lebai/claw/get_claw',
            GetClaw.Request(),
        )
        assert claw_after.result.success is True
        assert claw_after.state.force == pytest.approx(50.0)
        assert claw_after.state.amplitude == pytest.approx(40.0)

        if os.environ.get('LEBAI_TEST_START_STOP') == '1':
            start_result = _call_command(
                executor,
                probe,
                '/lebai/start_stop/start_sys',
            )
            assert start_result.result.success is True
            stop_result = _call_command(
                executor,
                probe,
                '/lebai/start_stop/stop_sys',
            )
            assert stop_result.result.success is True
    finally:
        if driver is not None:
            executor.remove_node(driver)
            driver.destroy_node()
        if probe is not None:
            executor.remove_node(probe)
            probe.destroy_node()
        rclpy.shutdown()


def _call_command(executor, node, service_name):
    from lebai_interfaces.srv import Command

    return _call_service(
        executor,
        node,
        Command,
        service_name,
        Command.Request(),
    )


def _call_service(executor, node, srv_type, service_name, request):
    client = node.create_client(srv_type, service_name)
    _spin_until(executor, client.service_is_ready)
    future = client.call_async(request)
    _spin_until(executor, future.done)
    return future.result()


def _spin_until(executor, predicate, timeout_sec=10.0):
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        executor.spin_once(timeout_sec=0.1)
        if predicate():
            return
    raise AssertionError('timed out waiting for simulator smoke condition')
