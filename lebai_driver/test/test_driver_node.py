from concurrent.futures import ThreadPoolExecutor
from threading import Event, Lock
from unittest.mock import Mock

import pytest
import rospy
from control_msgs.msg import GripperCommandGoal
from lebai_interfaces.srv import CommandRequest

from fakes import ActionHarness
from test_trajectory_action import goal

from lebai_driver.connection import RobotConnection
from lebai_driver.parameters import DEFAULT_PARAMETERS
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


@pytest.mark.parametrize('overrides', [{}, {
    '~robot_ip': 'sim.example', '~simulator': True,
    '~trajectory_action_name': 'arm/follow', '~gripper_action_name': '/other/claw',
    '~joint_names': list('abcdef'),
}])
def test_driver_composes_one_connection_and_one_status_service_gate(fake_rospy, monkeypatch, overrides):
    from lebai_driver import driver_node

    defaults = {
        'robot_ip': '127.0.0.1', 'simulator': False, 'namespace': '',
        'joint_names': ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6'],
        'joint_state_publish_rate': 20.0, 'robot_state_publish_rate': 10.0,
        'joint_motion_publish_rate': 20.0, 'io_state_publish_rate': 10.0,
        'gripper_state_publish_rate': 10.0, 'gripper_joint_name': 'gripper_r_joint1',
        'io_state_device': 'robot', 'io_state_digital_input_count': 0,
        'io_state_digital_output_count': 0, 'io_state_analog_input_count': 0,
        'io_state_analog_output_count': 0, 'io_state_dio_count': 0,
        'trajectory_action_name': '/lebai_trajectory_controller',
        'gripper_action_name': '/lebai_gripper_controller/gripper_cmd',
    }
    assert DEFAULT_PARAMETERS == defaults
    adapter = RosNodeAdapter(fake_rospy)
    fake_rospy.parameters.update(overrides)
    grouped = []
    for name in ('status_publishers', 'start_stop_services', 'motion_services',
                 'io_services', 'led_signal_services', 'resource_services', 'claw_services'):
        registrar = 'register_' + name
        spy = Mock(wraps=getattr(driver_node, registrar))
        monkeypatch.setattr(driver_node, registrar, spy)
        grouped.append(spy)

    arm, gripper = Mock(), Mock()
    monkeypatch.setattr(driver_node, 'register_trajectory_action', arm)
    monkeypatch.setattr(driver_node, 'register_gripper_action', gripper)
    robot_factory = Mock()
    driver = driver_node.LebaiDriverNode(adapter, robot_factory=robot_factory)
    assert dict(fake_rospy.parameter_calls) == {'~' + k: v for k, v in defaults.items()}
    robot_factory.assert_not_called()
    connection = driver.connection
    assert isinstance(connection, RobotConnection)
    assert connection.robot_ip == overrides.get('~robot_ip', '127.0.0.1')
    assert connection.simulator == overrides.get('~simulator', False)
    gate = grouped[0].call_args.kwargs['sdk_gate']
    assert isinstance(gate, StatusServiceGate)
    assert gate.admission is adapter.admission
    for registrar in grouped:
        registrar.assert_called_once_with(adapter, connection, sdk_gate=gate)
    arm.assert_called_once_with(connection, overrides.get('~joint_names', defaults['joint_names']),
                                action_name=overrides.get('~trajectory_action_name', defaults['trajectory_action_name']),
                                admission=adapter.admission)
    gripper.assert_called_once_with(connection,
                                    action_name=overrides.get('~gripper_action_name', defaults['gripper_action_name']),
                                    admission=adapter.admission)
    assert driver.trajectory_action is arm.return_value
    assert driver.gripper_action is gripper.return_value
    shutdown, = fake_rospy.shutdown_callbacks
    shutdown()
    assert adapter.admission.is_closed()


def test_signal_shutdown_closes_actions_timers_and_services_before_drain(fake_rospy, monkeypatch):
    from lebai_driver import _action_server, driver_node
    from lebai_driver.serial_gripper_node import LebaiSerialGripperNode

    # Isolate the real Noetic shutdown sequence from the rest of this pytest process.
    for field in ('_client_shutdown_hooks', '_preshutdown_hooks', '_shutdown_hooks', '_shutdown_threads'):
        monkeypatch.setattr(rospy.core, field, [])
    for field in ('_in_shutdown', '_shutdown_flag'):
        monkeypatch.setattr(rospy.core, field, False)
    fake_rospy.on_shutdown = rospy.on_shutdown
    fake_rospy.is_shutdown = rospy.is_shutdown
    fake_rospy.is_shutdown_requested = rospy.is_shutdown_requested
    adapter = RosNodeAdapter(fake_rospy)
    servers = {}

    def server_factory(name, *args, **kwargs):
        servers[name] = ActionHarness()
        return servers[name].server_factory(name, *args, **kwargs)

    monkeypatch.setattr(_action_server, 'ActionServer', server_factory)
    robot = Mock()
    active, release = Event(), Event()
    robot.move_pvat.side_effect = lambda *_: (active.set(), release.wait(5))
    robot.get_claw.return_value = (0, 0, False)
    driver = driver_node.LebaiDriverNode(adapter, robot_factory=lambda *a, **kw: robot)
    serial = LebaiSerialGripperNode(RosNodeAdapter(fake_rospy), gripper_factory=Mock())
    for publisher in fake_rospy.publishers:
        publisher.publish = Mock()
    plain_tick = Mock()
    timer = adapter.create_timer(1, plain_tick)
    arm, claw = servers.values()
    arm.submit(goal(joints=DEFAULT_PARAMETERS['joint_names']))
    assert active.wait(3)
    # Both serial callbacks have entered the ROS handler and are queued on the port.
    port = Lock()
    waiting_timer, waiting_service = Event(), Event()

    class QueuedPort:
        def __enter__(self):
            (waiting_service if waiting_timer.is_set() else waiting_timer).set()
            port.acquire()

        def __exit__(self, *_):
            port.release()

    serial._lock = QueuedPort()
    port.acquire()
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending_tick = pool.submit(serial.timer.callback, None)
        assert waiting_timer.wait(3)
        command = serial.services[3]
        pending_service = pool.submit(command.handler, CommandRequest())
        assert waiting_service.wait(3)
        closing = pool.submit(rospy.signal_shutdown, 'test')
        try:
            assert adapter.admission.closed.wait(3)
            assert not rospy.is_shutdown()
            assert not closing.done()
            handle = claw.submit(GripperCommandGoal())
            handle.set_rejected.assert_called_once()
            timer.callback(None)
            driver.status_publishers[0][1].callback(None)
            plain_tick.assert_not_called()
            robot.get_actual_joint_positions.assert_not_called()
            robot.set_claw.assert_not_called()
            stop = next(service for service in driver.services if service.name == 'start_stop/stop')
            assert not stop.handler(CommandRequest()).result.success
            robot.stop.assert_not_called()
        finally:
            port.release()
            release.set()
        pending_tick.result(3)
        assert not pending_service.result(3).result.success
        closing.result(3)
    serial._factory.assert_not_called()


def test_service_opening_connection_at_shutdown_does_not_send_command(fake_rospy, monkeypatch):
    from lebai_driver import driver_node

    monkeypatch.setattr(driver_node, 'register_gripper_action', Mock())
    monkeypatch.setattr(driver_node, 'register_trajectory_action', Mock())
    active, release = Event(), Event()
    robot = Mock()

    def open_robot(*args, **kwargs):
        active.set()
        assert release.wait(3)
        return robot

    adapter = RosNodeAdapter(fake_rospy)
    driver = driver_node.LebaiDriverNode(adapter, robot_factory=open_robot)
    start = next(s for s in driver.services if s.name == 'start_stop/start_sys')
    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = pool.submit(start.handler, CommandRequest())
        assert active.wait(3)
        closing = pool.submit(driver.shutdown)
        try:
            assert adapter.admission.closed.wait(3)
            assert not closing.done()
        finally:
            release.set()
        response = pending.result(3)
        closing.result(3)
    assert not response.result.success
    robot.start_sys.assert_not_called()
