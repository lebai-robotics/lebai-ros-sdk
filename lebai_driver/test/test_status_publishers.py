from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from threading import Event
from types import SimpleNamespace

import pytest
from genpy import Time
from lebai_interfaces.msg import ClawState, IOState, JointMotion, RobotState
from sensor_msgs.msg import JointState

from lebai_driver.connection import RobotConnection
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


class CountingConnection(RobotConnection):
    def __init__(self, robot):
        super().__init__('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
        self.robot_accesses = 0

    @property
    def robot(self):
        self.robot_accesses += 1
        return super().robot


@pytest.fixture
def status_robot():
    return SimpleNamespace(
        get_actual_joint_positions=lambda: [1, 2, 3, 4, 5, 6],
        get_target_joint_positions=lambda: [6, 5, 4, 3, 2, 1],
        get_actual_joint_speed=lambda: [0.1] * 6,
        get_target_joint_speed=lambda: [0.2] * 6,
        get_actual_joint_torques=lambda: [0.3] * 6,
        get_target_joint_torques=lambda: [0.4] * 6,
        get_actual_tcp_pose=lambda: {'x': 1},
        get_target_tcp_pose=lambda: {'y': 2},
        get_kin_data=lambda: {'actual_flange_pose': {'z': 3}},
        get_robot_state=lambda: 9,
        get_estop_reason=lambda: 0,
        is_disconnected=lambda: False,
        is_down=lambda: False,
        get_claw=lambda: (3.5, 50.0, True),
    )


@pytest.fixture
def status_rospy(fake_rospy, monkeypatch):
    create_publisher = fake_rospy.Publisher

    def capture_publisher(name, msg_type, queue_size):
        publisher = create_publisher(name, msg_type, queue_size)
        publisher.messages = []
        publisher.publish = publisher.messages.append
        return publisher

    monkeypatch.setattr(fake_rospy, 'Publisher', capture_publisher)
    return fake_rospy


def _register(rospy, connection, sdk_gate=None):
    from lebai_driver.status import register_status_publishers

    return register_status_publishers(RosNodeAdapter(rospy), connection, sdk_gate=sdk_gate)


def _tick(timer):
    timer.callback(object())


def test_status_publishers_register_topics_and_default_periods(status_rospy):
    connection = CountingConnection(None)
    handles = _register(status_rospy, connection)

    topics = [
        (publisher.msg_type, publisher.name, publisher.queue_size)
        for publisher in status_rospy.publishers
    ]
    assert topics == [
        (JointState, 'status/joint_states', 10),
        (JointState, 'claw/joint_states', 10),
        (JointState, 'model/joint_states', 10),
        (RobotState, 'status/robot', 10),
        (JointMotion, 'status/joint_motion', 10),
        (IOState, 'io/state', 10),
        (ClawState, 'claw/state', 10),
    ]
    assert [timer.duration.to_nsec() for timer in status_rospy.timers] == [
        50_000_000,
        100_000_000,
        50_000_000,
        100_000_000,
        50_000_000,
        100_000_000,
        100_000_000,
    ]
    assert handles == list(zip(status_rospy.publishers, status_rospy.timers))
    assert connection.robot_accesses == 0


def test_status_publishers_stamp_each_message_at_poll_time(status_rospy, status_robot):
    handles = _register(status_rospy, CountingConnection(status_robot), StatusServiceGate())
    stamp = Time(23, 456_789)
    status_rospy.stamp = stamp

    for _publisher, timer in handles:
        _tick(timer)

    messages = {publisher.name: publisher.messages[0] for publisher, _timer in handles}
    assert all(message.header.stamp == stamp for message in messages.values())
    assert messages['status/joint_states'].position == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    assert messages['claw/joint_states'].name == ['gripper_r_joint1']
    assert messages['model/joint_states'].name == [
        'joint_1',
        'joint_2',
        'joint_3',
        'joint_4',
        'joint_5',
        'joint_6',
        'gripper_r_joint1',
    ]
    assert messages['status/robot'].connected is True
    assert messages['status/robot'].state == 9
    assert messages['status/joint_motion'].connected is True
    assert messages['io/state'].connected is True
    assert messages['claw/state'].connected is True


def test_status_publishers_share_configured_arm_and_gripper_rates(status_rospy):
    status_rospy.parameters.update(
        {
            '~joint_state_publish_rate': 8,
            '~gripper_state_publish_rate': 4,
            '~robot_state_publish_rate': 5,
            '~joint_motion_publish_rate': 2,
            '~io_state_publish_rate': 1,
        }
    )

    handles = _register(status_rospy, CountingConnection(None))
    periods = {publisher.name: timer.duration.to_nsec() for publisher, timer in handles}

    assert periods == {
        'status/joint_states': 125_000_000,
        'claw/joint_states': 250_000_000,
        'model/joint_states': 125_000_000,
        'status/robot': 200_000_000,
        'status/joint_motion': 500_000_000,
        'io/state': 1_000_000_000,
        'claw/state': 250_000_000,
    }


def test_io_publisher_reads_configured_device_and_pin_counts(status_rospy, status_robot):
    status_rospy.parameters.update(
        {
            '~io_state_device': 'tool',
            '~io_state_digital_input_count': 2,
            '~io_state_digital_output_count': 1,
            '~io_state_analog_input_count': 1,
            '~io_state_analog_output_count': 2,
            '~io_state_dio_count': 1,
        }
    )
    status_robot.get_di = lambda device, pin: {('tool', 0): 0, ('tool', 1): 1}[device, pin]
    status_robot.get_do = lambda device, pin: {('tool', 0): 1}[device, pin]
    status_robot.get_ai = lambda device, pin: {('tool', 0): 1.5}[device, pin]
    status_robot.get_ao = lambda device, pin: {('tool', 0): 2.5, ('tool', 1): 3.5}[device, pin]
    status_robot.get_dio_mode = lambda device, pin: {('tool', 0): 1}[device, pin]

    handles = _register(status_rospy, CountingConnection(status_robot))
    publisher, timer = next(handle for handle in handles if handle[0].name == 'io/state')
    _tick(timer)

    message = publisher.messages[0]
    assert message.connected is True
    assert message.device == 'tool'
    assert message.digital_inputs == [False, True]
    assert message.digital_outputs == [True]
    assert message.analog_inputs == [1.5]
    assert message.analog_outputs == [2.5, 3.5]
    assert message.dio_modes == [True]


def test_status_publishers_publish_fallback_messages_on_sdk_errors(status_rospy, status_robot):
    def fail(*_args):
        raise RuntimeError('SDK offline')

    status_rospy.parameters.update({'~io_state_device': 'tool', '~io_state_digital_input_count': 1})
    status_robot.get_actual_joint_positions = fail
    status_robot.get_claw = fail
    status_robot.get_robot_state = fail
    status_robot.get_di = fail
    handles = _register(status_rospy, CountingConnection(status_robot), StatusServiceGate())

    for _publisher, timer in handles:
        _tick(timer)

    messages = {publisher.name: publisher.messages[0] for publisher, _timer in handles}
    assert all(message.header.stamp == status_rospy.stamp for message in messages.values())
    for topic in ('status/robot', 'status/joint_motion', 'io/state', 'claw/state'):
        assert messages[topic].connected is False
        assert messages[topic].message == 'SDK offline'
    assert messages['io/state'].device == 'tool'
    assert messages['status/joint_states'].position == []
    assert messages['claw/joint_states'].name == ['gripper_r_joint1']
    assert messages['claw/joint_states'].position == []
    assert messages['model/joint_states'].position == [0.0] * 7


@pytest.mark.parametrize('method, field, invalid, boundary', [
    ('get_robot_state', 'state', 2_147_483_648, 2_147_483_647),
    ('get_estop_reason', 'estop_reason', -2_147_483_649, -2_147_483_648),
])
def test_robot_status_recovers_from_out_of_range_sdk_code(
        status_rospy, status_robot, method, field, invalid, boundary):
    values = iter([invalid, boundary])
    setattr(status_robot, method, lambda: next(values))
    handles = _register(status_rospy, CountingConnection(status_robot))
    publisher, timer = next(handle for handle in handles if handle[0].name == 'status/robot')

    _tick(timer)
    _tick(timer)

    failed, recovered = publisher.messages
    for message in publisher.messages:
        message.serialize(BytesIO())
    assert not failed.connected
    assert failed.message == f"The '{field}' field must be an integer in [-2147483648, 2147483647]"
    assert recovered.connected
    assert getattr(recovered, field) == boundary


@pytest.mark.parametrize(
    'parameter, value',
    [
        ('joint_state_publish_rate', 0),
        ('gripper_state_publish_rate', -1),
        ('robot_state_publish_rate', 0),
        ('joint_motion_publish_rate', -1),
        ('io_state_publish_rate', 0),
    ],
)
def test_status_publishers_reject_nonpositive_rates(status_rospy, parameter, value):
    status_rospy.parameters[f'~{parameter}'] = value

    with pytest.raises(ValueError, match='publish rate must be positive'):
        _register(status_rospy, CountingConnection(None))

    assert status_rospy.publishers == []
    assert status_rospy.timers == []


def test_status_publishers_skip_sdk_poll_when_gate_denies_access(status_rospy, status_robot, monkeypatch):
    connection = CountingConnection(status_robot)
    gate = StatusServiceGate()
    sdk_lock = gate._sdk_lock
    acquisition_started = Event()
    allow_acquisition = Event()

    class DelayedExclusiveLock:
        def acquire(self, blocking=True):
            if blocking:
                acquisition_started.set()
                assert allow_acquisition.wait(timeout=5)
            return sdk_lock.acquire(blocking=blocking)

        def release(self):
            sdk_lock.release()

    def run_exclusive():
        with gate.exclusive_access():
            return 'entered'

    monkeypatch.setattr(gate, '_sdk_lock', DelayedExclusiveLock())
    handles = _register(status_rospy, connection, gate)

    with ThreadPoolExecutor(max_workers=1) as executor:
        exclusive_call = executor.submit(run_exclusive)
        try:
            assert acquisition_started.wait(timeout=5)
            for _publisher, timer in handles:
                _tick(timer)
            assert connection.robot_accesses == 0
            assert all(publisher.messages == [] for publisher, _timer in handles)
        finally:
            allow_acquisition.set()
        assert exclusive_call.result(timeout=5) == 'entered'

    publisher, timer = handles[0]
    _tick(timer)
    assert connection.robot_accesses == 1
    assert len(publisher.messages) == 1


def test_timer_callback_does_not_touch_sdk_after_shutdown(status_rospy, status_robot):
    connection = CountingConnection(status_robot)
    handles = _register(status_rospy, connection, StatusServiceGate())
    for _publisher, timer in handles:
        _tick(timer)
    assert connection.robot_accesses == 7

    status_rospy.shutdown = True
    for _publisher, timer in handles:
        _tick(timer)

    assert connection.robot_accesses == 7
    assert all(len(publisher.messages) == 1 for publisher, _timer in handles)
