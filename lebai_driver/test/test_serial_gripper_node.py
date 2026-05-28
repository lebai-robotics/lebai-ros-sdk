from lebai_interfaces.msg import GripperState
from lebai_interfaces.srv import (
    Command,
    SetGripperForce,
    SetGripperPosition,
    SetGripperVelocity,
)

from fakes import FakeNode, FakeStandaloneGripper


def _register(gripper):
    from lebai_driver.serial_gripper_node import register_gripper_interfaces

    node = FakeNode()
    handles = register_gripper_interfaces(node, lambda: gripper)
    callbacks = {
        name: callback
        for _srv_type, name, callback in node.services
    }
    return node, handles, callbacks


def test_gripper_interfaces_register_sdk_category_names():
    node, handles, _callbacks = _register(FakeStandaloneGripper())

    assert [(srv_type, name) for srv_type, name, _callback in node.services] == [
        (SetGripperPosition, 'gripper/set_position'),
        (SetGripperForce, 'gripper/set_force'),
        (SetGripperVelocity, 'gripper/set_velocity'),
        (Command, 'gripper/do_calibration'),
        (Command, 'gripper/turn_on_auto_calibration'),
        (Command, 'gripper/turn_off_auto_calibration'),
    ]
    assert [(publisher.msg_type, publisher.name, publisher.depth) for publisher in node.publishers] == [
        (GripperState, 'gripper/state', 10),
    ]
    assert [timer.period for timer in node.timers] == [0.1]
    assert len(handles) == 7


def test_gripper_set_services_map_requests_to_pylebai_gripper():
    gripper = FakeStandaloneGripper()
    _node, _handles, callbacks = _register(gripper)

    position_response = callbacks['gripper/set_position'](
        SetGripperPosition.Request(position=42),
        SetGripperPosition.Response(),
    )
    force_response = callbacks['gripper/set_force'](
        SetGripperForce.Request(force=73),
        SetGripperForce.Response(),
    )
    velocity_response = callbacks['gripper/set_velocity'](
        SetGripperVelocity.Request(velocity=91, persistent=True),
        SetGripperVelocity.Response(),
    )

    assert gripper.calls == [
        ('set_position', (42,), {}),
        ('set_force', (73,), {}),
        ('set_velocity', (91, True), {}),
    ]
    assert position_response.result.success is True
    assert force_response.result.success is True
    assert velocity_response.result.success is True


def test_gripper_command_services_map_to_pylebai_gripper():
    gripper = FakeStandaloneGripper()
    _node, _handles, callbacks = _register(gripper)

    calibration_response = callbacks['gripper/do_calibration'](
        Command.Request(),
        Command.Response(),
    )
    on_response = callbacks['gripper/turn_on_auto_calibration'](
        Command.Request(),
        Command.Response(),
    )
    off_response = callbacks['gripper/turn_off_auto_calibration'](
        Command.Request(),
        Command.Response(),
    )

    assert gripper.calls == [
        ('do_calibration', (), {}),
        ('turn_on_auto_calibration', (), {}),
        ('turn_off_auto_calibration', (), {}),
    ]
    assert calibration_response.result.success is True
    assert on_response.result.success is True
    assert off_response.result.success is True


def test_gripper_state_publisher_maps_pylebai_getters():
    gripper = FakeStandaloneGripper()
    gripper.position = 12
    gripper.force = 34
    gripper.velocity = 56
    gripper.calibrated = True
    node, _handles, _callbacks = _register(gripper)

    node.timers[0].callback()

    assert gripper.calls == [
        ('get_current_position', (), {}),
        ('get_current_force', (), {}),
        ('get_current_velocity', (False,), {}),
        ('is_calibrated', (), {}),
    ]
    message = node.publishers[0].messages[-1]
    assert message.header.stamp.sec == 12
    assert message.connected is True
    assert message.position == 12.0
    assert message.force == 34.0
    assert message.velocity == 56.0
    assert message.calibrated is True


def test_gripper_service_and_state_map_exceptions():
    gripper = FakeStandaloneGripper()
    gripper.exceptions['set_position'] = RuntimeError('position rejected')
    _node, _handles, callbacks = _register(gripper)

    response = callbacks['gripper/set_position'](
        SetGripperPosition.Request(position=42),
        SetGripperPosition.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'position rejected'

    gripper.exceptions.clear()
    gripper.exceptions['get_current_position'] = RuntimeError('gripper offline')
    node, _handles, _callbacks = _register(gripper)
    node.timers[0].callback()

    message = node.publishers[0].messages[-1]
    assert message.connected is False
    assert message.message == 'gripper offline'


def test_gripper_node_uses_injected_factory_without_importing_pylebai():
    import rclpy

    from lebai_driver.serial_gripper_node import LebaiSerialGripperNode

    rclpy.init()
    node = None

    try:
        node = LebaiSerialGripperNode(
            gripper_factory=lambda port_name: FakeStandaloneGripper(port_name),
        )

        assert node.get_name() == 'lebai_serial_gripper'
        assert node.has_parameter('port_name')
        assert len(node.gripper_handles) == 7
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()
