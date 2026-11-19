import math

from lebai_interfaces.msg import CartesianPose, ClawState, IOState, JointMotion, RobotState
from sensor_msgs.msg import JointState

from lebai_driver.errors import exception_message


_POSE_FIELDS = ('x', 'y', 'z', 'rx', 'ry', 'rz')
_GRIPPER_MAX_ANGLE = math.pi / 3.0


def cartesian_pose_from_sdk(data):
    values = [_value(data, index, name, 0.0) for index, name in enumerate(_POSE_FIELDS)]
    return CartesianPose(
        x=float(values[0]),
        y=float(values[1]),
        z=float(values[2]),
        rx=float(values[3]),
        ry=float(values[4]),
        rz=float(values[5]),
    )


def robot_state_from_sdk(robot):
    return RobotState(
        connected=True,
        state=int(robot.get_robot_state()),
        estop_reason=int(robot.get_estop_reason()),
        is_disconnected=bool(robot.is_disconnected()),
        is_down=bool(robot.is_down()),
    )


def robot_state_error(exc):
    return RobotState(connected=False, message=exception_message(exc))


def joint_state_from_sdk(robot, joint_names):
    message = JointState()
    message.name = list(joint_names)
    message.position = _float_list(robot.get_actual_joint_positions())
    message.velocity = _float_list(robot.get_actual_joint_speed())
    message.effort = _float_list(robot.get_actual_joint_torques())
    return message


def joint_state_error(exc, joint_names):
    message = JointState()
    message.name = list(joint_names)
    del exc
    return message


def joint_motion_from_sdk(robot):
    message = JointMotion()
    message.connected = True
    message.actual_joint_positions = _float_list(robot.get_actual_joint_positions())
    message.target_joint_positions = _float_list(robot.get_target_joint_positions())
    message.actual_joint_speed = _float_list(robot.get_actual_joint_speed())
    message.target_joint_speed = _float_list(robot.get_target_joint_speed())
    message.actual_joint_torques = _float_list(robot.get_actual_joint_torques())
    message.target_joint_torques = _float_list(robot.get_target_joint_torques())
    message.actual_tcp_pose = cartesian_pose_from_sdk(robot.get_actual_tcp_pose())
    message.target_tcp_pose = cartesian_pose_from_sdk(robot.get_target_tcp_pose())
    message.actual_flange_pose = cartesian_pose_from_sdk(_actual_flange_pose(robot))
    return message


def joint_motion_error(exc):
    return JointMotion(connected=False, message=exception_message(exc))


def io_state_from_sdk(
    robot,
    device,
    digital_input_count=0,
    digital_output_count=0,
    analog_input_count=0,
    analog_output_count=0,
    dio_count=0,
):
    message = IOState()
    message.connected = True
    message.device = device
    message.digital_inputs = [
        bool(robot.get_di(device, pin))
        for pin in range(int(digital_input_count))
    ]
    message.digital_outputs = [
        bool(robot.get_do(device, pin))
        for pin in range(int(digital_output_count))
    ]
    message.analog_inputs = [
        float(robot.get_ai(device, pin))
        for pin in range(int(analog_input_count))
    ]
    message.analog_outputs = [
        float(robot.get_ao(device, pin))
        for pin in range(int(analog_output_count))
    ]
    message.dio_modes = [
        bool(robot.get_dio_mode(device, pin))
        for pin in range(int(dio_count))
    ]
    return message


def io_state_error(exc, device):
    return IOState(connected=False, device=device, message=exception_message(exc))


def claw_state_from_sdk(robot):
    data = robot.get_claw()
    message = ClawState()
    message.connected = True
    message.force = float(_value(data, 0, 'force', 0.0))
    message.amplitude = float(_value(data, 1, 'amplitude', 0.0))
    message.hold_on = bool(_value(data, 2, 'hold_on', False))
    return message


def claw_state_error(exc):
    return ClawState(connected=False, message=exception_message(exc))


def gripper_joint_state_from_claw(robot, joint_name):
    claw_state = claw_state_from_sdk(robot)
    message = JointState()
    message.name = [joint_name]
    message.position = [_amplitude_to_gripper_angle(claw_state.amplitude)]
    return message


def model_joint_state_from_sdk(robot, joint_names, gripper_joint_name):
    message = joint_state_from_sdk(robot, joint_names)
    gripper_joint_state = gripper_joint_state_from_claw(robot, gripper_joint_name)
    message.name.append(gripper_joint_state.name[0])
    message.position.append(gripper_joint_state.position[0])
    message.velocity.append(0.0)
    message.effort.append(0.0)
    return message


def gripper_joint_state_error(exc, joint_name):
    message = JointState()
    message.name = [joint_name]
    del exc
    return message


def model_joint_state_error(exc, joint_names, gripper_joint_name):
    message = joint_state_error(exc, joint_names)
    message.name.append(gripper_joint_name)
    message.position = [0.0 for _name in message.name]
    return message


def _actual_flange_pose(robot):
    data = robot.get_kin_data()
    return _value(data, 0, 'actual_flange_pose', {})


def _float_list(values):
    if values is None:
        return []
    return [float(value) for value in values]


def _amplitude_to_gripper_angle(amplitude):
    amplitude = max(0.0, min(100.0, float(amplitude)))
    return _GRIPPER_MAX_ANGLE * amplitude / 100.0


def _value(data, index, name, default):
    if data is None:
        return default
    if isinstance(data, dict):
        return data.get(name, default)
    if hasattr(data, name):
        return getattr(data, name)
    try:
        return data[index]
    except (IndexError, KeyError, TypeError):
        return default
