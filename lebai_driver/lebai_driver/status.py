from lebai_interfaces.msg import ClawState, IOState, JointMotion, RobotState
from sensor_msgs.msg import JointState

from lebai_driver.conversions import (
    claw_state_error,
    claw_state_from_sdk,
    gripper_joint_state_error,
    gripper_joint_state_from_claw,
    io_state_error,
    io_state_from_sdk,
    joint_motion_error,
    joint_motion_from_sdk,
    joint_state_error,
    joint_state_from_sdk,
    model_joint_state_error,
    model_joint_state_from_sdk,
    robot_state_error,
    robot_state_from_sdk,
)
from lebai_driver.parameters import DEFAULT_JOINT_NAMES


_DEPTH = 10


def register_status_publishers(node, connection, callback_group=None, sdk_gate=None):
    joint_names = _parameter_value(
        node,
        'joint_names',
        DEFAULT_JOINT_NAMES,
    )
    gripper_joint_name = _parameter_value(
        node,
        'gripper_joint_name',
        'gripper_r_joint1',
    )
    io_device = _parameter_value(node, 'io_state_device', 'robot')
    io_counts = {
        'digital_input_count': _parameter_value(node, 'io_state_digital_input_count', 0),
        'digital_output_count': _parameter_value(node, 'io_state_digital_output_count', 0),
        'analog_input_count': _parameter_value(node, 'io_state_analog_input_count', 0),
        'analog_output_count': _parameter_value(node, 'io_state_analog_output_count', 0),
        'dio_count': _parameter_value(node, 'io_state_dio_count', 0),
    }

    registrations = [
        _PublisherRegistration(
            JointState,
            'status/joint_states',
            _parameter_value(node, 'joint_state_publish_rate', 20.0),
            lambda robot: joint_state_from_sdk(robot, joint_names),
            lambda exc: joint_state_error(exc, joint_names),
        ),
        _PublisherRegistration(
            JointState,
            'claw/joint_states',
            _parameter_value(node, 'gripper_state_publish_rate', 10.0),
            lambda robot: gripper_joint_state_from_claw(robot, gripper_joint_name),
            lambda exc: gripper_joint_state_error(exc, gripper_joint_name),
        ),
        _PublisherRegistration(
            JointState,
            'model/joint_states',
            _parameter_value(node, 'joint_state_publish_rate', 20.0),
            lambda robot: model_joint_state_from_sdk(
                robot,
                joint_names,
                gripper_joint_name,
            ),
            lambda exc: model_joint_state_error(exc, joint_names, gripper_joint_name),
        ),
        _PublisherRegistration(
            RobotState,
            'status/robot',
            _parameter_value(node, 'robot_state_publish_rate', 10.0),
            robot_state_from_sdk,
            robot_state_error,
        ),
        _PublisherRegistration(
            JointMotion,
            'status/joint_motion',
            _parameter_value(node, 'joint_motion_publish_rate', 20.0),
            joint_motion_from_sdk,
            joint_motion_error,
        ),
        _PublisherRegistration(
            IOState,
            'io/state',
            _parameter_value(node, 'io_state_publish_rate', 10.0),
            lambda robot: io_state_from_sdk(robot, io_device, **io_counts),
            lambda exc: io_state_error(exc, io_device),
        ),
        _PublisherRegistration(
            ClawState,
            'claw/state',
            _parameter_value(node, 'gripper_state_publish_rate', 10.0),
            claw_state_from_sdk,
            claw_state_error,
        ),
    ]

    handles = []
    for registration in registrations:
        publisher = node.create_publisher(registration.msg_type, registration.topic, _DEPTH)
        timer = node.create_timer(
            _period(registration.rate),
            _make_publish_callback(node, connection, publisher, registration, sdk_gate),
            callback_group=callback_group,
        )
        handles.append((publisher, timer))
    return handles


def _make_publish_callback(node, connection, publisher, registration, sdk_gate=None):
    def callback():
        if sdk_gate is not None:
            with sdk_gate.status_access() as enabled:
                if not enabled:
                    return
                _publish_status(node, connection, publisher, registration)
            return

        _publish_status(node, connection, publisher, registration)

    return callback


def _publish_status(node, connection, publisher, registration):
    try:
        message = registration.build_message(connection.robot)
    except Exception as exc:
        message = registration.build_error_message(exc)
    message.header.stamp = node.get_clock().now().to_msg()
    publisher.publish(message)


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


class _PublisherRegistration:
    def __init__(self, msg_type, topic, rate, build_message, build_error_message):
        self.msg_type = msg_type
        self.topic = topic
        self.rate = rate
        self.build_message = build_message
        self.build_error_message = build_error_message
