import rclpy
from rclpy.node import Node

from lebai_interfaces.msg import GripperState
from lebai_interfaces.srv import (
    Command,
    SetGripperForce,
    SetGripperPosition,
    SetGripperVelocity,
)

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok


_DEPTH = 10


class LebaiSerialGripperNode(Node):
    def __init__(self, gripper_factory=None):
        super().__init__('lebai_serial_gripper')
        self.declare_parameter('port_name', '/dev/ttyUSB0')
        self.declare_parameter('gripper_state_publish_rate', 10.0)

        port_name = self.get_parameter('port_name').value
        self.gripper_handles = register_gripper_interfaces(
            self,
            _lazy_gripper_factory(
                port_name,
                gripper_factory or _default_gripper_factory,
            ),
        )


def register_gripper_interfaces(node, gripper_factory):
    definitions = [
        (SetGripperPosition, 'gripper/set_position', _set_position),
        (SetGripperForce, 'gripper/set_force', _set_force),
        (SetGripperVelocity, 'gripper/set_velocity', _set_velocity),
        (Command, 'gripper/do_calibration', _do_calibration),
        (Command, 'gripper/turn_on_auto_calibration', _turn_on_auto_calibration),
        (Command, 'gripper/turn_off_auto_calibration', _turn_off_auto_calibration),
    ]

    handles = []
    for srv_type, service_name, handler in definitions:
        handles.append(
            node.create_service(
                srv_type,
                service_name,
                _make_gripper_callback(gripper_factory, handler),
            )
        )

    publisher = node.create_publisher(GripperState, 'gripper/state', _DEPTH)
    timer = node.create_timer(
        _period(_parameter_value(node, 'gripper_state_publish_rate', 10.0)),
        _make_state_callback(node, gripper_factory, publisher),
    )
    handles.append((publisher, timer))
    return handles


def _make_gripper_callback(gripper_factory, handler):
    def callback(request, response):
        try:
            handler(gripper_factory(), request, response)
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _make_state_callback(node, gripper_factory, publisher):
    def callback():
        try:
            message = _state_from_gripper(gripper_factory())
        except Exception as exc:
            message = GripperState(
                connected=False,
                message=exception_message(exc),
            )
        message.header.stamp = node.get_clock().now().to_msg()
        publisher.publish(message)

    return callback


def _set_position(gripper, request, response):
    del response
    gripper.set_position(request.position)


def _set_force(gripper, request, response):
    del response
    gripper.set_force(request.force)


def _set_velocity(gripper, request, response):
    del response
    gripper.set_velocity(request.velocity, request.persistent)


def _do_calibration(gripper, request, response):
    del request, response
    gripper.do_calibration()


def _turn_on_auto_calibration(gripper, request, response):
    del request, response
    gripper.turn_on_auto_calibration()


def _turn_off_auto_calibration(gripper, request, response):
    del request, response
    gripper.turn_off_auto_calibration()


def _state_from_gripper(gripper):
    return GripperState(
        connected=True,
        position=float(gripper.get_current_position()),
        force=float(gripper.get_current_force()),
        velocity=float(gripper.get_current_velocity(False)),
        calibrated=bool(gripper.is_calibrated()),
    )


def _lazy_gripper_factory(port_name, factory):
    gripper = None

    def get_gripper():
        nonlocal gripper
        if gripper is None:
            gripper = factory(port_name)
        return gripper

    return get_gripper


def _default_gripper_factory(port_name):
    from pylebai.gripper import Gripper

    return Gripper(port_name)


def _parameter_value(node, name, default):
    try:
        return node.get_parameter(name).value
    except Exception:
        return default


def _period(rate):
    rate = float(rate)
    if rate <= 0.0:
        raise ValueError('publish rate must be positive')
    return 1.0 / rate


def main(args=None):
    rclpy.init(args=args)
    node = LebaiSerialGripperNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
