import math


GRIPPER_MAX_JOINT_POSITION = math.pi / 3.0
GRIPPER_JOINT_NAME = "gripper_r_joint1"
MANIPULATOR_JOINT_NAMES = (
    "joint_1",
    "joint_2",
    "joint_3",
    "joint_4",
    "joint_5",
    "joint_6",
)


def amplitude_to_gripper_joint(amplitude):
    amplitude = float(amplitude)
    if amplitude < 0.0 or amplitude > 100.0:
        raise ValueError("amplitude must be in the range [0, 100]")
    return GRIPPER_MAX_JOINT_POSITION * amplitude / 100.0


def parse_joint_positions(value):
    positions = [float(item.strip()) for item in value.split(",") if item.strip()]
    if len(positions) != len(MANIPULATOR_JOINT_NAMES):
        raise ValueError("expected six comma-separated joint positions")
    return positions
