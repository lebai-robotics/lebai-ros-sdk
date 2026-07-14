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

import math

from geometry_msgs.msg import Point, Pose, Quaternion
from lebai_interfaces.msg import ClawState, IOState, JointMotion, RobotState
from sensor_msgs.msg import JointState
from tf_transformations import euler_from_quaternion, quaternion_from_euler

from lebai_driver.errors import exception_message


_POSE_FIELDS = ('x', 'y', 'z', 'rx', 'ry', 'rz')
_GRIPPER_MAX_ANGLE = math.pi / 3.0


def pose_from_sdk(data):
    values = _sdk_pose_values(data)
    quaternion = quaternion_from_euler(
        values['rx'],
        values['ry'],
        values['rz'],
        axes='sxyz',
    )
    return Pose(
        position=Point(
            x=values['x'],
            y=values['y'],
            z=values['z'],
        ),
        orientation=Quaternion(
            x=float(quaternion[0]),
            y=float(quaternion[1]),
            z=float(quaternion[2]),
            w=float(quaternion[3]),
        ),
    )


def pose_to_sdk(pose):
    position = _finite_values({
        'x': pose.position.x,
        'y': pose.position.y,
        'z': pose.position.z,
    }, 'ROS pose position')
    quaternion = _finite_values({
        'x': pose.orientation.x,
        'y': pose.orientation.y,
        'z': pose.orientation.z,
        'w': pose.orientation.w,
    }, 'ROS pose quaternion')
    quaternion_values = [
        quaternion['x'],
        quaternion['y'],
        quaternion['z'],
        quaternion['w'],
    ]
    norm = math.hypot(*quaternion_values)
    if norm == 0.0 or not math.isfinite(norm):
        raise ValueError('ROS pose quaternion must be finite and nonzero')
    normalized = [value / norm for value in quaternion_values]
    rx, ry, rz = euler_from_quaternion(normalized, axes='sxyz')
    return {
        **position,
        'rx': float(rx),
        'ry': float(ry),
        'rz': float(rz),
    }


def twist_to_sdk(twist):
    return _finite_values({
        'x': twist.linear.x,
        'y': twist.linear.y,
        'z': twist.linear.z,
        'rx': twist.angular.x,
        'ry': twist.angular.y,
        'rz': twist.angular.z,
    }, 'ROS twist')


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
    return joint_state_from_kin_data(robot.get_kin_data(), joint_names)


def joint_state_from_kin_data(data, joint_names):
    message = JointState()
    message.name = list(joint_names)
    message.position = _float_list(data.actual_joint_pose)
    message.velocity = _float_list(data.actual_joint_speed)
    message.effort = _float_list(data.actual_joint_torque)
    return message


def joint_state_error(exc, joint_names):
    message = JointState()
    message.name = list(joint_names)
    del exc
    return message


def joint_motion_from_sdk(robot):
    return joint_motion_from_kin_data(robot.get_kin_data())


def joint_motion_from_kin_data(data):
    message = JointMotion()
    message.connected = True
    message.actual_joint_positions = _float_list(data.actual_joint_pose)
    message.target_joint_positions = _float_list(data.target_joint_pose)
    message.actual_joint_speed = _float_list(data.actual_joint_speed)
    message.target_joint_speed = _float_list(data.target_joint_speed)
    message.actual_joint_torques = _float_list(data.actual_joint_torque)
    message.target_joint_torques = _float_list(data.target_joint_torque)
    message.actual_tcp_pose = pose_from_sdk(data.actual_tcp_pose)
    message.target_tcp_pose = pose_from_sdk(data.target_tcp_pose)
    message.actual_flange_pose = pose_from_sdk(data.actual_flange_pose)
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
    message.digital_inputs = _batch_io_values(
        robot.get_dis,
        'get_dis',
        device,
        digital_input_count,
        bool,
    )
    message.digital_outputs = _batch_io_values(
        robot.get_dos,
        'get_dos',
        device,
        digital_output_count,
        bool,
    )
    message.analog_inputs = _batch_io_values(
        robot.get_ais,
        'get_ais',
        device,
        analog_input_count,
        float,
    )
    message.analog_outputs = _batch_io_values(
        robot.get_aos,
        'get_aos',
        device,
        analog_output_count,
        float,
    )
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
    return model_joint_state_from_kin_data(
        robot,
        robot.get_kin_data(),
        joint_names,
        gripper_joint_name,
    )


def model_joint_state_from_kin_data(
    robot,
    data,
    joint_names,
    gripper_joint_name,
):
    message = joint_state_from_kin_data(data, joint_names)
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


def _sdk_pose_values(data):
    values = {}
    for name in _POSE_FIELDS:
        try:
            value = data[name]
        except (IndexError, KeyError, TypeError) as exc:
            raise ValueError('SDK Cartesian pose missing field %s' % name) from exc
        try:
            values[name] = float(value)
        except (OverflowError, TypeError, ValueError) as exc:
            raise ValueError(
                'SDK Cartesian pose field %s must be numeric' % name
            ) from exc
    return _finite_values(values, 'SDK Cartesian pose')


def _finite_values(values, label):
    converted = {name: float(value) for name, value in values.items()}
    nonfinite = [
        name
        for name, value in converted.items()
        if not math.isfinite(value)
    ]
    if nonfinite:
        raise ValueError(
            '%s fields must be finite: %s' % (label, ', '.join(nonfinite))
        )
    return converted


def _float_list(values):
    if values is None:
        return []
    return [float(value) for value in values]


def _batch_io_values(getter, getter_name, device, count, convert):
    count = int(count)
    if count <= 0:
        return []
    values = list(getter(device, 0, count))
    if len(values) != count:
        raise ValueError(
            'SDK %s returned %d values, expected %d'
            % (getter_name, len(values), count)
        )
    return [convert(value) for value in values]


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
