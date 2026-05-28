from lebai_interfaces.msg import ClawState, IOState, JointMotion, RobotState
from sensor_msgs.msg import JointState

from fakes import FakeClawData, FakeNode, FakeRobot


def _register(robot):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.status import register_status_publishers

    node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    handles = register_status_publishers(node, connection)
    return node, handles


def test_conversion_helpers_accept_dict_list_tuple_and_object_poses():
    from lebai_driver.conversions import cartesian_pose_from_sdk

    assert cartesian_pose_from_sdk({'x': 1, 'y': 2, 'z': 3, 'rx': 4, 'ry': 5, 'rz': 6}).x == 1.0
    assert cartesian_pose_from_sdk([1, 2, 3, 4, 5, 6]).rz == 6.0
    assert cartesian_pose_from_sdk((1, 2, 3)).z == 3.0
    assert cartesian_pose_from_sdk(type('Pose', (), {'x': 7, 'rz': 8})()).x == 7.0
    assert cartesian_pose_from_sdk(type('Pose', (), {'x': 7, 'rz': 8})()).rz == 8.0


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


def test_joint_state_and_motion_conversion_maps_sdk_fields():
    from lebai_driver.conversions import joint_motion_from_sdk, joint_state_from_sdk

    robot = FakeRobot()
    robot.actual_joint_positions = [1, 2, 3]
    robot.target_joint_positions = [4, 5, 6]
    robot.actual_joint_speed = [0.1, 0.2, 0.3]
    robot.target_joint_speed = [0.4, 0.5, 0.6]
    robot.actual_joint_torques = [10, 11, 12]
    robot.target_joint_torques = [13, 14, 15]
    robot.actual_tcp_pose = {'x': 1, 'y': 2, 'z': 3, 'rx': 4, 'ry': 5, 'rz': 6}
    robot.target_tcp_pose = {'x': 6, 'y': 5, 'z': 4, 'rx': 3, 'ry': 2, 'rz': 1}
    robot.actual_flange_pose = {'x': 0.5, 'rz': 0.6}

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
    assert motion.actual_tcp_pose.x == 1.0
    assert motion.target_tcp_pose.rz == 1.0
    assert motion.actual_flange_pose.x == 0.5
    assert motion.actual_flange_pose.rz == 0.6


def test_io_and_claw_conversion_maps_sdk_fields():
    from lebai_driver.conversions import claw_state_from_sdk, io_state_from_sdk

    robot = FakeRobot()
    robot.digital_inputs[('robot', 0)] = True
    robot.digital_outputs[('robot', 1)] = True
    robot.analog_inputs[('robot', 0)] = 1.5
    robot.analog_outputs[('robot', 0)] = 2.5
    robot.dio_modes[('robot', 0)] = True
    robot.claw = FakeClawData(force=3.5, amplitude=4.5, hold_on=True)

    io_state = io_state_from_sdk(
        robot,
        device='robot',
        digital_input_count=2,
        digital_output_count=2,
        analog_input_count=1,
        analog_output_count=1,
        dio_count=1,
    )
    claw_state = claw_state_from_sdk(robot)

    assert isinstance(io_state, IOState)
    assert io_state.connected is True
    assert io_state.device == 'robot'
    assert list(io_state.digital_inputs) == [True, False]
    assert list(io_state.digital_outputs) == [False, True]
    assert list(io_state.analog_inputs) == [1.5]
    assert list(io_state.analog_outputs) == [2.5]
    assert list(io_state.dio_modes) == [True]
    assert isinstance(claw_state, ClawState)
    assert claw_state.connected is True
    assert claw_state.force == 3.5
    assert claw_state.amplitude == 4.5
    assert claw_state.hold_on is True


def test_status_publishers_register_topics_and_periods():
    node, handles = _register(FakeRobot())

    published_topics = [
        (publisher.msg_type, publisher.name, publisher.depth)
        for publisher in node.publishers
    ]

    assert published_topics == [
        (JointState, 'status/joint_states', 10),
        (RobotState, 'status/robot', 10),
        (JointMotion, 'status/joint_motion', 10),
        (IOState, 'io/state', 10),
        (ClawState, 'claw/state', 10),
    ]
    assert [timer.period for timer in node.timers] == [0.05, 0.1, 0.05, 0.1, 0.1]
    assert len(handles) == 5


def test_status_publishers_publish_messages_and_map_errors_to_message_field():
    robot = FakeRobot()
    robot.actual_joint_positions = [1.0]
    robot.actual_joint_speed = [2.0]
    robot.actual_joint_torques = [3.0]
    robot.robot_state = 9
    node, _handles = _register(robot)

    for timer in node.timers:
        timer.callback()

    joint_state, robot_state, joint_motion, io_state, claw_state = [
        publisher.messages[-1]
        for publisher in node.publishers
    ]
    assert joint_state.header.stamp.sec == 12
    assert list(joint_state.position) == [1.0]
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
    node.timers[1].callback()

    failed_state = node.publishers[1].messages[-1]
    assert failed_state.connected is False
    assert failed_state.message == 'status offline'
