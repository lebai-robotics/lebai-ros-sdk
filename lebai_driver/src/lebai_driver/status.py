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
from lebai_driver.parameters import DEFAULT_PARAMETERS


_DEPTH = 10


def register_status_publishers(node, connection, sdk_gate=None):
    joint_names = _parameter(node, 'joint_names')
    gripper_joint_name = _parameter(node, 'gripper_joint_name')
    io_device = _parameter(node, 'io_state_device')
    io_counts = {
        'digital_input_count': _parameter(node, 'io_state_digital_input_count'),
        'digital_output_count': _parameter(node, 'io_state_digital_output_count'),
        'analog_input_count': _parameter(node, 'io_state_analog_input_count'),
        'analog_output_count': _parameter(node, 'io_state_analog_output_count'),
        'dio_count': _parameter(node, 'io_state_dio_count'),
    }
    joint_period = _period(_parameter(node, 'joint_state_publish_rate'))
    gripper_period = _period(_parameter(node, 'gripper_state_publish_rate'))

    registrations = [
        _PublisherRegistration(
            JointState,
            'status/joint_states',
            joint_period,
            lambda robot: joint_state_from_sdk(robot, joint_names),
            lambda exc: joint_state_error(exc, joint_names),
        ),
        _PublisherRegistration(
            JointState,
            'claw/joint_states',
            gripper_period,
            lambda robot: gripper_joint_state_from_claw(robot, gripper_joint_name),
            lambda exc: gripper_joint_state_error(exc, gripper_joint_name),
        ),
        _PublisherRegistration(
            JointState,
            'model/joint_states',
            joint_period,
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
            _period(_parameter(node, 'robot_state_publish_rate')),
            robot_state_from_sdk,
            robot_state_error,
        ),
        _PublisherRegistration(
            JointMotion,
            'status/joint_motion',
            _period(_parameter(node, 'joint_motion_publish_rate')),
            joint_motion_from_sdk,
            joint_motion_error,
        ),
        _PublisherRegistration(
            IOState,
            'io/state',
            _period(_parameter(node, 'io_state_publish_rate')),
            lambda robot: io_state_from_sdk(robot, io_device, **io_counts),
            lambda exc: io_state_error(exc, io_device),
        ),
        _PublisherRegistration(
            ClawState,
            'claw/state',
            gripper_period,
            claw_state_from_sdk,
            claw_state_error,
        ),
    ]

    handles = []
    for registration in registrations:
        publisher = node.create_publisher(registration.msg_type, registration.topic, _DEPTH)
        timer = node.create_timer(
            registration.period,
            _make_publish_callback(node, connection, publisher, registration, sdk_gate),
        )
        handles.append((publisher, timer))
    return handles


def _make_publish_callback(node, connection, publisher, registration, sdk_gate):
    def callback():
        if sdk_gate is not None:
            with sdk_gate.status_access() as enabled:
                if not enabled:
                    return
                _publish_status(node, connection, publisher, registration, sdk_gate.admission)
            return

        _publish_status(node, connection, publisher, registration)

    return callback


def _publish_status(node, connection, publisher, registration, admission=None):
    try:
        robot = connection.robot
        message = registration.build_message(admission.methods(robot) if admission is not None else robot)
    except Exception as exc:
        message = registration.build_error_message(exc)
    message.header.stamp = node.now()
    publisher.publish(message)


def _parameter(node, name):
    return node.parameter(name, DEFAULT_PARAMETERS[name])


def _period(rate):
    rate = float(rate)
    if rate <= 0.0:
        raise ValueError('publish rate must be positive')
    return 1.0 / rate


class _PublisherRegistration:
    def __init__(self, msg_type, topic, period, build_message, build_error_message):
        self.msg_type = msg_type
        self.topic = topic
        self.period = period
        self.build_message = build_message
        self.build_error_message = build_error_message
