import os
import time

import pytest


pytestmark = pytest.mark.integration

_SERVICE_TIMEOUT_SEC = 10.0
_MOTION_TIMEOUT_SEC = 20.0


def test_driver_talks_to_simulator_topics_and_core_services():
    robot_ip = os.environ.get('LEBAI_TEST_ROBOT_IP')
    if not robot_ip:
        pytest.skip('LEBAI_TEST_ROBOT_IP is not set')

    import rclpy
    from rclpy.executors import MultiThreadedExecutor

    from lebai_driver.driver_node import LebaiDriverNode
    from lebai_interfaces.msg import (
        IOState,
        JointMotion,
        MotionParams,
        MotionTarget,
        RobotState,
    )
    import lebai_interfaces.srv as srv
    from sensor_msgs.msg import JointState

    args = [
        '--ros-args',
        '-r', '__ns:=/lebai',
        '-p', 'robot_ip:=%s' % robot_ip,
        '-p', 'simulator:=true',
        '-p', 'joint_state_publish_rate:=2.0',
        '-p', 'robot_state_publish_rate:=2.0',
        '-p', 'joint_motion_publish_rate:=2.0',
        '-p', 'io_state_publish_rate:=2.0',
        '-p', 'gripper_state_publish_rate:=2.0',
    ]

    rclpy.init(args=args)
    executor = MultiThreadedExecutor(num_threads=8)
    driver = None
    probe = None
    started = False
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
        assert robot_states[-1].connected is True
        assert list(joint_states[-1].position)
        assert len(joint_states[-1].position) >= 6

        joint_motions = []
        io_states = []
        probe.create_subscription(
            JointMotion,
            '/lebai/status/joint_motion',
            joint_motions.append,
            10,
        )
        probe.create_subscription(
            IOState,
            '/lebai/io/state',
            io_states.append,
            10,
        )
        _spin_until(executor, lambda: joint_motions and io_states)
        assert joint_motions[-1].connected is True
        assert list(joint_motions[-1].actual_joint_positions)
        assert io_states[-1].connected is True

        clients = [
            probe.create_client(srv_type, service_name)
            for srv_type, service_name in _driver_service_specs(srv)
        ]
        _spin_until(executor, lambda: all(client.service_is_ready() for client in clients))

        running = _call_service(
            executor,
            probe,
            srv.GetRunningMotion,
            '/lebai/motion/get_running_motion',
            srv.GetRunningMotion.Request(),
        )
        assert running.result.success is True

        for srv_type, service_name, request in _read_only_io_requests(srv):
            response = _call_service(executor, probe, srv_type, service_name, request)
            assert response.result.success is True

        start_result = _call_command(
            executor,
            probe,
            '/lebai/start_stop/start_sys',
        )
        assert start_result.result.success is True
        started = True

        movej = _call_service(
            executor,
            probe,
            srv.MoveJoint,
            '/lebai/motion/movej',
            srv.MoveJoint.Request(
                target=MotionTarget(
                    is_joint_pose=True,
                    joint_positions=list(joint_states[-1].position[:6]),
                ),
                params=MotionParams(
                    acceleration=0.2,
                    velocity=0.2,
                    time=0.0,
                    blend_radius=0.0,
                ),
            ),
            timeout_sec=_MOTION_TIMEOUT_SEC,
        )
        assert movej.result.success is True

        motion_state = _call_service(
            executor,
            probe,
            srv.GetMotionState,
            '/lebai/motion/get_motion_state',
            srv.GetMotionState.Request(motion_id=movej.motion_id),
        )
        assert motion_state.result.success is True

        wait = _call_service(
            executor,
            probe,
            srv.WaitMove,
            '/lebai/motion/wait_move',
            srv.WaitMove.Request(motion_id=movej.motion_id),
            timeout_sec=_MOTION_TIMEOUT_SEC,
        )
        assert wait.result.success is True

        if os.environ.get('LEBAI_TEST_START_STOP') == '1':
            stop_result = _call_command(
                executor,
                probe,
                '/lebai/start_stop/stop_sys',
            )
            assert stop_result.result.success is True
            started = False
    finally:
        if started and probe is not None:
            try:
                _call_command(executor, probe, '/lebai/start_stop/stop_sys')
            except Exception:
                pass
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


def _call_service(
    executor,
    node,
    srv_type,
    service_name,
    request,
    timeout_sec=_SERVICE_TIMEOUT_SEC,
):
    client = node.create_client(srv_type, service_name)
    _spin_until(executor, client.service_is_ready, timeout_sec=timeout_sec)
    future = client.call_async(request)
    _spin_until(executor, future.done, timeout_sec=timeout_sec)
    return future.result()


def _driver_service_specs(srv):
    return [
        (srv.MoveJoint, '/lebai/motion/movej'),
        (srv.MoveLinear, '/lebai/motion/movel'),
        (srv.MoveCircular, '/lebai/motion/movec'),
        (srv.SpeedJoint, '/lebai/motion/speedj'),
        (srv.SpeedLinear, '/lebai/motion/speedl'),
        (srv.MovePvat, '/lebai/motion/move_pvat'),
        (srv.WaitMove, '/lebai/motion/wait_move'),
        (srv.Command, '/lebai/motion/stop_move'),
        (srv.Command, '/lebai/motion/skip_move'),
        (srv.GetRunningMotion, '/lebai/motion/get_running_motion'),
        (srv.GetMotionState, '/lebai/motion/get_motion_state'),
        (srv.Command, '/lebai/start_stop/start_sys'),
        (srv.Command, '/lebai/start_stop/stop_sys'),
        (srv.Command, '/lebai/start_stop/powerdown'),
        (srv.Command, '/lebai/start_stop/stop'),
        (srv.Command, '/lebai/start_stop/estop'),
        (srv.Command, '/lebai/start_stop/start_teach_mode'),
        (srv.Command, '/lebai/start_stop/end_teach_mode'),
        (srv.Command, '/lebai/start_stop/pause_move'),
        (srv.Command, '/lebai/start_stop/resume_move'),
        (srv.Command, '/lebai/start_stop/reboot'),
        (srv.SetDigitalOutput, '/lebai/io/set_do'),
        (srv.GetDigitalInput, '/lebai/io/get_di'),
        (srv.GetDigitalOutput, '/lebai/io/get_do'),
        (srv.SetDigitalOutputs, '/lebai/io/set_dos'),
        (srv.GetDigitalInputs, '/lebai/io/get_dis'),
        (srv.GetDigitalOutputs, '/lebai/io/get_dos'),
        (srv.SetAnalogOutput, '/lebai/io/set_ao'),
        (srv.GetAnalogInput, '/lebai/io/get_ai'),
        (srv.GetAnalogOutput, '/lebai/io/get_ao'),
        (srv.SetAnalogOutputs, '/lebai/io/set_aos'),
        (srv.GetAnalogInputs, '/lebai/io/get_ais'),
        (srv.GetAnalogOutputs, '/lebai/io/get_aos'),
        (srv.SetDioMode, '/lebai/io/set_dio_mode'),
        (srv.GetDioMode, '/lebai/io/get_dio_mode'),
        (srv.Command, '/lebai/claw/init_claw'),
        (srv.SetClaw, '/lebai/claw/set_claw'),
        (srv.GetClaw, '/lebai/claw/get_claw'),
    ]


def _read_only_io_requests(srv):
    return [
        (
            srv.GetDigitalInput,
            '/lebai/io/get_di',
            srv.GetDigitalInput.Request(device='robot', pin=0),
        ),
        (
            srv.GetDigitalOutput,
            '/lebai/io/get_do',
            srv.GetDigitalOutput.Request(device='robot', pin=0),
        ),
        (
            srv.GetAnalogInput,
            '/lebai/io/get_ai',
            srv.GetAnalogInput.Request(device='robot', pin=0),
        ),
        (
            srv.GetAnalogOutput,
            '/lebai/io/get_ao',
            srv.GetAnalogOutput.Request(device='robot', pin=0),
        ),
        (
            srv.GetDioMode,
            '/lebai/io/get_dio_mode',
            srv.GetDioMode.Request(device='robot', pin=0),
        ),
    ]


def _spin_until(executor, predicate, timeout_sec=10.0):
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        executor.spin_once(timeout_sec=0.1)
        if predicate():
            return
    raise AssertionError('timed out waiting for simulator smoke condition')
