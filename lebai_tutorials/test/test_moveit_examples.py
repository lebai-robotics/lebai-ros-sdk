import math

import pytest

from lebai_tutorials_common import (
    MANIPULATOR_JOINT_NAMES,
    amplitude_to_gripper_joint,
    parse_joint_positions,
)
from moveit_manipulator_example import make_joint_goal


def test_amplitude_to_gripper_joint_maps_percent_to_active_joint_angle():
    assert amplitude_to_gripper_joint(0) == 0.0
    assert amplitude_to_gripper_joint(50) == pytest.approx(math.pi / 6.0)
    assert amplitude_to_gripper_joint(100) == pytest.approx(math.pi / 3.0)


@pytest.mark.parametrize("amplitude", [-1, 100.1])
def test_amplitude_to_gripper_joint_rejects_values_outside_percent_range(amplitude):
    with pytest.raises(ValueError, match="amplitude"):
        amplitude_to_gripper_joint(amplitude)


def test_parse_joint_positions_accepts_exactly_six_comma_separated_values():
    assert parse_joint_positions("1, 2,3, 4.5, -5, 6") == [
        1.0,
        2.0,
        3.0,
        4.5,
        -5.0,
        6.0,
    ]


@pytest.mark.parametrize("value", ["1,2,3", "1,2,3,4,5,6,7"])
def test_parse_joint_positions_rejects_wrong_joint_count(value):
    with pytest.raises(ValueError, match="six"):
        parse_joint_positions(value)


def test_make_joint_goal_targets_manipulator_joint_constraints():
    target = [0.1, -0.2, 0.3, -0.4, 0.5, -0.6]

    goal = make_joint_goal(target, plan_only=True)

    assert goal.request.group_name == "manipulator"
    assert goal.planning_options.plan_only is True
    constraints = goal.request.goal_constraints[0].joint_constraints
    assert [constraint.joint_name for constraint in constraints] == list(MANIPULATOR_JOINT_NAMES)
    assert [constraint.position for constraint in constraints] == target
    assert all(constraint.tolerance_above == pytest.approx(0.01) for constraint in constraints)
    assert all(constraint.tolerance_below == pytest.approx(0.01) for constraint in constraints)
