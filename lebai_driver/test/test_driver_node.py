from unittest.mock import Mock

import pytest

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
    for registrar in grouped:
        registrar.assert_called_once_with(adapter, connection, sdk_gate=gate)
    arm.assert_called_once_with(connection, overrides.get('~joint_names', defaults['joint_names']),
                                action_name=overrides.get('~trajectory_action_name', defaults['trajectory_action_name']))
    gripper.assert_called_once_with(connection,
                                    action_name=overrides.get('~gripper_action_name', defaults['gripper_action_name']))
    assert driver.trajectory_action is arm.return_value
    assert driver.gripper_action is gripper.return_value
    shutdown, = fake_rospy.shutdown_callbacks
    shutdown()
    arm.return_value.shutdown.assert_called_once_with()
    gripper.return_value.shutdown.assert_called_once_with()
