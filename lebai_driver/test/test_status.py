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

from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from lebai_interfaces.msg import ClawState, IOState, JointMotion, RobotState
from pylebai import l_master
import pytest
from sensor_msgs.msg import JointState

from fakes import FakeClawData, FakeNode, FakeRobot


def _register(robot, node=None):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.status import register_status_publishers

    if node is None:
        node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    handles = register_status_publishers(node, connection)
    return node, handles


def _sdk_pose(**overrides):
    values = {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'rx': 0.0,
        'ry': 0.0,
        'rz': 0.0,
    }
    values.update(overrides)
    pose = l_master.CartesianPose()
    for name, value in values.items():
        pose[name] = value
    return pose


def _sdk_vector(values):
    vector = l_master.DoubleVector()
    for value in values:
        vector.push_back(value)
    return vector


def _sdk_joint_motion_data():
    data = l_master.JointMotionData()
    data.actual_joint_pose = _sdk_vector([1, 2, 3])
    data.target_joint_pose = _sdk_vector([4, 5, 6])
    data.actual_joint_speed = _sdk_vector([0.1, 0.2, 0.3])
    data.target_joint_speed = _sdk_vector([0.4, 0.5, 0.6])
    data.actual_joint_torque = _sdk_vector([10, 11, 12])
    data.target_joint_torque = _sdk_vector([13, 14, 15])
    data.actual_tcp_pose = _sdk_pose(x=1, y=2, z=3, rx=math.pi / 2)
    data.target_tcp_pose = _sdk_pose(x=6, y=5, z=4, rz=math.pi / 2)
    data.actual_flange_pose = _sdk_pose(x=0.5, ry=math.pi / 2)
    return data


def test_sdk_swig_pose_converts_euler_zyx_to_ros_quaternion():
    from lebai_driver.conversions import pose_from_sdk

    sdk_pose = _sdk_pose(
        x=1.0,
        y=2.0,
        z=3.0,
        rx=math.pi / 2.0,
        rz=math.pi / 2.0,
    )

    pose = pose_from_sdk(sdk_pose)

    assert not isinstance(sdk_pose, dict)
    assert isinstance(pose, Pose)
    assert pose.position == Point(x=1.0, y=2.0, z=3.0)
    assert [
        pose.orientation.x,
        pose.orientation.y,
        pose.orientation.z,
        pose.orientation.w,
    ] == pytest.approx([0.5, 0.5, 0.5, 0.5])


def test_sdk_pose_requires_every_finite_field():
    from lebai_driver.conversions import pose_from_sdk

    missing = _sdk_pose()
    del missing['rz']

    with pytest.raises(ValueError, match='rz'):
        pose_from_sdk(missing)
    with pytest.raises(ValueError, match='finite'):
        pose_from_sdk(_sdk_pose(ry=float('nan')))
    with pytest.raises(ValueError, match='finite'):
        pose_from_sdk(_sdk_pose(x=float('inf')))


def test_ros_pose_normalizes_quaternion_and_converts_to_sdk_euler_zyx():
    from lebai_driver.conversions import pose_to_sdk

    pose = Pose(
        position=Point(x=1.0, y=2.0, z=3.0),
        orientation=Quaternion(x=1.0, y=1.0, z=1.0, w=1.0),
    )

    sdk_pose = pose_to_sdk(pose)

    assert sdk_pose == pytest.approx({
        'x': 1.0,
        'y': 2.0,
        'z': 3.0,
        'rx': math.pi / 2.0,
        'ry': 0.0,
        'rz': math.pi / 2.0,
    })


@pytest.mark.parametrize(
    'orientation',
    [
        Quaternion(x=0.0, y=0.0, z=0.0, w=0.0),
        Quaternion(x=float('nan'), y=0.0, z=0.0, w=1.0),
        Quaternion(x=0.0, y=float('inf'), z=0.0, w=1.0),
    ],
)
def test_ros_pose_rejects_zero_or_nonfinite_quaternion(orientation):
    from lebai_driver.conversions import pose_to_sdk

    with pytest.raises(ValueError, match='quaternion'):
        pose_to_sdk(Pose(orientation=orientation))


def test_ros_pose_and_twist_reject_nonfinite_components():
    from lebai_driver.conversions import pose_to_sdk, twist_to_sdk

    with pytest.raises(ValueError, match='finite'):
        pose_to_sdk(Pose(
            position=Point(x=float('nan')),
            orientation=Quaternion(w=1.0),
        ))
    with pytest.raises(ValueError, match='finite'):
        twist_to_sdk(Twist(linear=Vector3(x=float('inf'))))


def test_ros_twist_maps_linear_and_angular_components_directly():
    from lebai_driver.conversions import twist_to_sdk

    twist = Twist(
        linear=Vector3(x=1.0, y=2.0, z=3.0),
        angular=Vector3(x=4.0, y=5.0, z=6.0),
    )

    assert twist_to_sdk(twist) == {
        'x': 1.0,
        'y': 2.0,
        'z': 3.0,
        'rx': 4.0,
        'ry': 5.0,
        'rz': 6.0,
    }


def test_robot_state_conversion_maps_sdk_fields():
    from lebai_driver.conversions import robot_state_from_sdk

    robot = FakeRobot()
    robot.robot_state = 5
    robot.estop_reason = 7
    robot.disconnected = True
    robot.down = False

    message = robot_state_from_sdk(robot)

    assert isinstance(message, RobotState)
    assert message.connected is True
    assert message.state == 5
    assert message.estop_reason == 7
    assert message.is_disconnected is True
    assert message.is_down is False
    assert robot.calls == [
        ('get_robot_state', (), {}),
        ('get_estop_reason', (), {}),
        ('is_disconnected', (), {}),
        ('is_down', (), {}),
    ]


def test_joint_state_and_motion_conversion_use_one_released_sdk_snapshot_each():
    from lebai_driver.conversions import joint_motion_from_sdk, joint_state_from_sdk

    robot = FakeRobot()
    robot.kin_data = _sdk_joint_motion_data()

    joint_state = joint_state_from_sdk(robot, ['j1', 'j2', 'j3'])
    motion = joint_motion_from_sdk(robot)

    assert isinstance(joint_state, JointState)
    assert joint_state.name == ['j1', 'j2', 'j3']
    assert list(joint_state.position) == [1.0, 2.0, 3.0]
    assert list(joint_state.velocity) == [0.1, 0.2, 0.3]
    assert list(joint_state.effort) == [10.0, 11.0, 12.0]
    assert isinstance(motion, JointMotion)
    assert motion.connected is True
    assert list(motion.actual_joint_positions) == [1.0, 2.0, 3.0]
    assert list(motion.target_joint_positions) == [4.0, 5.0, 6.0]
    assert list(motion.actual_joint_speed) == [0.1, 0.2, 0.3]
    assert list(motion.target_joint_speed) == [0.4, 0.5, 0.6]
    assert list(motion.actual_joint_torques) == [10.0, 11.0, 12.0]
    assert list(motion.target_joint_torques) == [13.0, 14.0, 15.0]
    assert motion.actual_tcp_pose.position.x == 1.0
    assert motion.actual_tcp_pose.orientation.x == pytest.approx(math.sqrt(0.5))
    assert motion.target_tcp_pose.orientation.z == pytest.approx(math.sqrt(0.5))
    assert motion.actual_flange_pose.position.x == 0.5
    assert motion.actual_flange_pose.orientation.y == pytest.approx(math.sqrt(0.5))
    assert robot.calls == [
        ('get_kin_data', (), {}),
        ('get_kin_data', (), {}),
    ]


def test_io_and_claw_conversion_maps_sdk_fields():
    from lebai_driver.conversions import claw_state_from_sdk, io_state_from_sdk

    robot = FakeRobot()
    robot.digital_inputs[('robot', 0)] = True
    robot.digital_outputs[('robot', 1)] = True
    robot.analog_inputs[('robot', 0)] = 1.25
    robot.analog_inputs[('robot', 1)] = -2.5
    robot.analog_outputs[('robot', 0)] = 3.5
    robot.analog_outputs[('robot', 1)] = 4.75
    robot.dio_modes[('robot', 0)] = True
    robot.claw = FakeClawData(force=3.5, amplitude=4.5, hold_on=True)

    io_state = io_state_from_sdk(
        robot,
        device='robot',
        digital_input_count=2,
        digital_output_count=2,
        analog_input_count=2,
        analog_output_count=2,
        dio_count=2,
    )
    claw_state = claw_state_from_sdk(robot)

    assert isinstance(io_state, IOState)
    assert io_state.connected is True
    assert io_state.device == 'robot'
    assert list(io_state.digital_inputs) == [True, False]
    assert list(io_state.digital_outputs) == [False, True]
    assert list(io_state.analog_inputs) == [1.25, -2.5]
    assert list(io_state.analog_outputs) == [3.5, 4.75]
    assert list(io_state.dio_modes) == [True, False]
    assert isinstance(claw_state, ClawState)
    assert claw_state.connected is True
    assert claw_state.force == 3.5
    assert claw_state.amplitude == 4.5
    assert claw_state.hold_on is True
    assert robot.calls == [
        ('get_dis', ('robot', 0, 2), {}),
        ('get_dos', ('robot', 0, 2), {}),
        ('get_ais', ('robot', 0, 2), {}),
        ('get_aos', ('robot', 0, 2), {}),
        ('get_dio_mode', ('robot', 0), {}),
        ('get_dio_mode', ('robot', 1), {}),
        ('get_claw', (), {}),
    ]


def test_io_conversion_skips_batch_calls_for_zero_counts():
    from lebai_driver.conversions import io_state_from_sdk

    robot = FakeRobot()

    message = io_state_from_sdk(robot, device='robot')

    assert list(message.digital_inputs) == []
    assert list(message.digital_outputs) == []
    assert list(message.analog_inputs) == []
    assert list(message.analog_outputs) == []
    assert robot.calls == []


@pytest.mark.parametrize(
    ('method_name', 'count_name'),
    [
        ('get_dis', 'digital_input_count'),
        ('get_dos', 'digital_output_count'),
        ('get_ais', 'analog_input_count'),
        ('get_aos', 'analog_output_count'),
    ],
)
def test_io_conversion_rejects_batch_length_mismatch(method_name, count_name):
    from lebai_driver.conversions import io_state_from_sdk

    robot = FakeRobot()
    setattr(robot, method_name, lambda *_args: [0])

    with pytest.raises(ValueError, match='returned 1 values, expected 2'):
        io_state_from_sdk(robot, device='robot', **{count_name: 2})


def test_claw_amplitude_maps_to_independent_gripper_joint_angle():
    from lebai_driver.conversions import gripper_joint_state_from_claw

    robot = FakeRobot()
    robot.claw = FakeClawData(amplitude=50.0)

    message = gripper_joint_state_from_claw(robot, 'gripper_r_joint1')

    assert isinstance(message, JointState)
    assert message.name == ['gripper_r_joint1']
    assert list(message.position) == [0.5235987755982988]
    assert list(message.velocity) == []
    assert list(message.effort) == []


def test_claw_amplitude_mapping_clamps_to_zero_and_one_hundred_percent():
    from lebai_driver.conversions import gripper_joint_state_from_claw

    robot = FakeRobot()
    robot.claw = FakeClawData(amplitude=-20.0)
    closed = gripper_joint_state_from_claw(robot, 'gripper_r_joint1')

    robot.claw = FakeClawData(amplitude=150.0)
    open_ = gripper_joint_state_from_claw(robot, 'gripper_r_joint1')

    assert list(closed.position) == [0.0]
    assert list(open_.position) == [1.0471975511965976]


def test_model_joint_state_combines_arm_and_gripper_source_joint():
    from lebai_driver.conversions import model_joint_state_from_sdk

    robot = FakeRobot()
    robot.actual_joint_positions = [1, 2, 3]
    robot.actual_joint_speed = [0.1, 0.2, 0.3]
    robot.actual_joint_torques = [10, 11, 12]
    robot.claw = FakeClawData(amplitude=25.0)

    message = model_joint_state_from_sdk(
        robot,
        ['joint1', 'joint2', 'joint3'],
        'gripper_r_joint1',
    )

    assert isinstance(message, JointState)
    assert message.name == ['joint1', 'joint2', 'joint3', 'gripper_r_joint1']
    assert list(message.position) == [1.0, 2.0, 3.0, 0.2617993877991494]
    assert list(message.velocity) == [0.1, 0.2, 0.3, 0.0]
    assert list(message.effort) == [10.0, 11.0, 12.0, 0.0]


def test_model_joint_state_error_uses_zero_positions_for_robot_state_publisher():
    from lebai_driver.conversions import model_joint_state_error

    message = model_joint_state_error(
        RuntimeError('robot unavailable'),
        ['joint1', 'joint2'],
        'gripper_r_joint1',
    )

    assert message.name == ['joint1', 'joint2', 'gripper_r_joint1']
    assert list(message.position) == [0.0, 0.0, 0.0]
    assert list(message.velocity) == []
    assert list(message.effort) == []


def test_status_publishers_register_topics_and_periods():
    node, handles = _register(FakeRobot())

    published_topics = [
        (publisher.msg_type, publisher.name, publisher.depth)
        for publisher in node.publishers
    ]

    assert published_topics == [
        (JointState, 'status/joint_states', 10),
        (JointState, 'claw/joint_states', 10),
        (JointState, 'model/joint_states', 10),
        (RobotState, 'status/robot', 10),
        (JointMotion, 'status/joint_motion', 10),
        (IOState, 'io/state', 10),
        (ClawState, 'claw/state', 10),
    ]
    assert len(node.timers) == 5
    assert len(handles) == 7


def test_status_publishers_always_use_fixed_arm_joint_names():
    advertised_joint_names = [f'robot1_joint_{index}' for index in range(1, 7)]
    node = FakeNode({
        'joint_names': advertised_joint_names,
        'gripper_joint_name': 'custom_gripper_joint',
    })
    robot = FakeRobot()
    robot.actual_joint_positions = [0.0] * 6
    robot.actual_joint_speed = [0.0] * 6
    robot.actual_joint_torques = [0.0] * 6

    node, handles = _register(robot, node=node)
    timers = {publisher.name: timer for publisher, timer in handles}
    timers['status/joint_states'].callback()

    fixed_joint_names = [f'joint_{index}' for index in range(1, 7)]
    assert 'joint_names' not in node.parameter_requests
    assert node.publishers[0].messages[-1].name == fixed_joint_names
    assert node.publishers[2].messages[-1].name == [
        *fixed_joint_names,
        'custom_gripper_joint',
    ]


def test_status_publishers_publish_messages_and_map_errors_to_message_field():
    robot = FakeRobot()
    robot.actual_joint_positions = [1.0]
    robot.actual_joint_speed = [2.0]
    robot.actual_joint_torques = [3.0]
    robot.robot_state = 9
    node, handles = _register(robot)

    for timer in node.timers:
        timer.callback()

    (
        joint_state,
        gripper_joint_state,
        model_joint_state,
        robot_state,
        joint_motion,
        io_state,
        claw_state,
    ) = [
        publisher.messages[-1]
        for publisher in node.publishers
    ]
    assert joint_state.header.stamp.sec == 12
    assert list(joint_state.position) == [1.0]
    assert gripper_joint_state.header.stamp.sec == 12
    assert gripper_joint_state.name == ['gripper_r_joint1']
    assert model_joint_state.header.stamp.sec == 12
    assert model_joint_state.name == [
        'joint_1',
        'joint_2',
        'joint_3',
        'joint_4',
        'joint_5',
        'joint_6',
        'gripper_r_joint1',
    ]
    assert robot_state.header.stamp.sec == 12
    assert robot_state.connected is True
    assert robot_state.state == 9
    assert joint_motion.header.stamp.sec == 12
    assert joint_motion.connected is True
    assert io_state.header.stamp.sec == 12
    assert io_state.connected is True
    assert claw_state.header.stamp.sec == 12
    assert claw_state.connected is True

    robot.exceptions['get_robot_state'] = RuntimeError('status offline')
    timers = {publisher.name: timer for publisher, timer in handles}
    timers['status/robot'].callback()

    failed_state = node.publishers[3].messages[-1]
    assert failed_state.connected is False
    assert failed_state.message == 'status offline'
