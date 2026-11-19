from io import BytesIO
from types import SimpleNamespace

import pytest
from lebai_interfaces.msg import CartesianPose, ClawState, IOState, JointMotion, RobotState
from sensor_msgs.msg import JointState


POSE_FIELDS = ('x', 'y', 'z', 'rx', 'ry', 'rz')


def _pose_values(pose):
    return tuple(getattr(pose, field) for field in POSE_FIELDS)


def _round_trip(message, message_class):
    assert isinstance(message, message_class)
    buffer = BytesIO()
    message.serialize(buffer)
    return message_class().deserialize(buffer.getvalue())


@pytest.fixture
def motion_robot():
    return SimpleNamespace(
        get_actual_joint_positions=lambda: [1, 2, 3],
        get_target_joint_positions=lambda: [4, 5, 6],
        get_actual_joint_speed=lambda: (0.1, 0.2, 0.3),
        get_target_joint_speed=lambda: (0.4, 0.5, 0.6),
        get_actual_joint_torques=lambda: [10, 11, 12],
        get_target_joint_torques=lambda: [13, 14, 15],
        get_actual_tcp_pose=lambda: {'x': 1, 'y': 2, 'z': 3, 'rx': 4, 'ry': 5, 'rz': 6},
        get_target_tcp_pose=lambda: [6, 5, 4, 3, 2, 1],
        get_kin_data=lambda: {'actual_flange_pose': SimpleNamespace(x=0.5, rz=0.6)},
        get_claw=lambda: SimpleNamespace(force=3.5, amplitude=25.0, hold_on=True),
    )


@pytest.mark.parametrize(
    'data, expected',
    [
        ({'x': 1, 'y': 2, 'z': 3, 'rx': 4, 'ry': 5, 'rz': 6}, (1, 2, 3, 4, 5, 6)),
        ([1, 2, 3, 4, 5, 6], (1, 2, 3, 4, 5, 6)),
        ((1, 2, 3), (1, 2, 3, 0, 0, 0)),
        (SimpleNamespace(x=7, rz=8), (7, 0, 0, 0, 0, 8)),
    ],
    ids=['dict', 'list', 'tuple', 'object'],
)
def test_cartesian_pose_maps_sdk_values(data, expected):
    from lebai_driver.conversions import cartesian_pose_from_sdk

    message = _round_trip(cartesian_pose_from_sdk(data), CartesianPose)

    assert _pose_values(message) == expected


def test_robot_state_maps_sdk_flags_and_codes():
    from lebai_driver.conversions import robot_state_from_sdk

    robot = SimpleNamespace(
        get_robot_state=lambda: '5',
        get_estop_reason=lambda: 7,
        is_disconnected=lambda: 1,
        is_down=lambda: 0,
    )

    message = _round_trip(robot_state_from_sdk(robot), RobotState)

    assert message.connected is True
    assert message.state == 5
    assert message.estop_reason == 7
    assert message.is_disconnected is True
    assert message.is_down is False
    assert message.message == ''


def test_joint_state_maps_actual_joint_readings(motion_robot):
    from lebai_driver.conversions import joint_state_from_sdk

    message = _round_trip(joint_state_from_sdk(motion_robot, ['joint1', 'joint2', 'joint3']), JointState)

    assert message.name == ['joint1', 'joint2', 'joint3']
    assert list(message.position) == [1.0, 2.0, 3.0]
    assert list(message.velocity) == [0.1, 0.2, 0.3]
    assert list(message.effort) == [10.0, 11.0, 12.0]


def test_joint_motion_maps_actual_and_target_readings(motion_robot):
    from lebai_driver.conversions import joint_motion_from_sdk

    message = _round_trip(joint_motion_from_sdk(motion_robot), JointMotion)

    assert message.connected is True
    assert list(message.actual_joint_positions) == [1.0, 2.0, 3.0]
    assert list(message.target_joint_positions) == [4.0, 5.0, 6.0]
    assert list(message.actual_joint_speed) == [0.1, 0.2, 0.3]
    assert list(message.target_joint_speed) == [0.4, 0.5, 0.6]
    assert list(message.actual_joint_torques) == [10.0, 11.0, 12.0]
    assert list(message.target_joint_torques) == [13.0, 14.0, 15.0]
    assert _pose_values(message.actual_tcp_pose) == (1, 2, 3, 4, 5, 6)
    assert _pose_values(message.target_tcp_pose) == (6, 5, 4, 3, 2, 1)
    assert _pose_values(message.actual_flange_pose) == (0.5, 0, 0, 0, 0, 0.6)
    assert message.message == ''


def test_io_state_maps_sdk_pins():
    from lebai_driver.conversions import io_state_from_sdk

    robot = SimpleNamespace(
        get_di=lambda device, pin: {('robot', 0): 1, ('robot', 1): 0}[device, pin],
        get_do=lambda device, pin: {('robot', 0): 0, ('robot', 1): 1}[device, pin],
        get_ai=lambda device, pin: {('robot', 0): 1.5}[device, pin],
        get_ao=lambda device, pin: {('robot', 0): 2.5}[device, pin],
        get_dio_mode=lambda device, pin: {('robot', 0): 1}[device, pin],
    )

    message = io_state_from_sdk(
        robot,
        device='robot',
        digital_input_count=2,
        digital_output_count=2,
        analog_input_count=1,
        analog_output_count=1,
        dio_count=1,
    )
    message = _round_trip(message, IOState)

    assert message.connected is True
    assert message.device == 'robot'
    assert list(message.digital_inputs) == [True, False]
    assert list(message.digital_outputs) == [False, True]
    assert list(message.analog_inputs) == [1.5]
    assert list(message.analog_outputs) == [2.5]
    assert list(message.dio_modes) == [True]
    assert message.message == ''


@pytest.mark.parametrize(
    'claw_data',
    [
        SimpleNamespace(force=3.5, amplitude=4.5, hold_on=True),
        {'force': 3.5, 'amplitude': 4.5, 'hold_on': 1},
        (3.5, 4.5, True),
    ],
)
def test_claw_state_maps_sdk_reading(claw_data):
    from lebai_driver.conversions import claw_state_from_sdk

    robot = SimpleNamespace(get_claw=lambda: claw_data)
    message = _round_trip(claw_state_from_sdk(robot), ClawState)

    assert message.connected is True
    assert message.force == 3.5
    assert message.amplitude == 4.5
    assert message.hold_on is True
    assert message.message == ''


@pytest.mark.parametrize(
    'amplitude, angle',
    [
        (-20.0, 0.0),
        (0.0, 0.0),
        (50.0, 0.5235987755982988),
        (100.0, 1.0471975511965976),
        (150.0, 1.0471975511965976),
    ],
)
def test_claw_amplitude_maps_to_single_gripper_source_joint(amplitude, angle):
    from lebai_driver.conversions import gripper_joint_state_from_claw

    robot = SimpleNamespace(get_claw=lambda: SimpleNamespace(amplitude=amplitude))
    message = _round_trip(gripper_joint_state_from_claw(robot, 'gripper_r_joint1'), JointState)

    assert message.name == ['gripper_r_joint1']
    assert list(message.position) == pytest.approx([angle])
    assert list(message.velocity) == []
    assert list(message.effort) == []


def test_model_joint_state_appends_only_the_gripper_source_joint(motion_robot):
    from lebai_driver.conversions import model_joint_state_from_sdk

    message = model_joint_state_from_sdk(motion_robot, ['joint1', 'joint2', 'joint3'], 'gripper_r_joint1')
    message = _round_trip(message, JointState)

    assert message.name == ['joint1', 'joint2', 'joint3', 'gripper_r_joint1']
    assert list(message.position) == pytest.approx([1.0, 2.0, 3.0, 0.2617993877991494])
    assert list(message.velocity) == [0.1, 0.2, 0.3, 0.0]
    assert list(message.effort) == [10.0, 11.0, 12.0, 0.0]


@pytest.mark.parametrize(
    'converter, message_class, args',
    [
        ('robot_state_error', RobotState, ()),
        ('joint_motion_error', JointMotion, ()),
        ('io_state_error', IOState, ('tool',)),
        ('claw_state_error', ClawState, ()),
    ],
)
@pytest.mark.parametrize(
    'exc, expected',
    [(RuntimeError('SDK unavailable'), 'SDK unavailable'), (RuntimeError(), 'RuntimeError')],
)
def test_status_error_serializes_disconnected_state(converter, message_class, args, exc, expected):
    from lebai_driver import conversions

    message = _round_trip(getattr(conversions, converter)(exc, *args), message_class)

    assert message.connected is False
    assert message.message == expected
    if message_class is IOState:
        assert message.device == 'tool'


def test_model_joint_state_error_zero_fills_all_positions():
    from lebai_driver.conversions import model_joint_state_error

    message = model_joint_state_error(
        RuntimeError('robot unavailable'), ['joint1', 'joint2'], 'gripper_r_joint1'
    )
    message = _round_trip(message, JointState)

    assert message.name == ['joint1', 'joint2', 'gripper_r_joint1']
    assert list(message.position) == [0.0, 0.0, 0.0]
    assert list(message.velocity) == []
    assert list(message.effort) == []
