from builtin_interfaces.msg import Time


class FakeRobot:
    def __init__(self, robot_ip='127.0.0.1', simulator=False):
        self.robot_ip = robot_ip
        self.simulator = simulator
        self.calls = []
        self.exceptions = {}
        self.digital_inputs = {}
        self.digital_outputs = {}
        self.analog_inputs = {}
        self.analog_outputs = {}
        self.dio_modes = {}
        self.led = None
        self.signals = {}
        self.claw = FakeClawData()
        self.next_motion_id = 100
        self.running_motion_id = 0
        self.motion_states = {}
        self.robot_state = 0
        self.estop_reason = 0
        self.disconnected = False
        self.down = False
        self.actual_joint_positions = []
        self.target_joint_positions = []
        self.actual_joint_speed = []
        self.target_joint_speed = []
        self.actual_joint_torques = []
        self.target_joint_torques = []
        self.actual_tcp_pose = {}
        self.target_tcp_pose = {}
        self.actual_flange_pose = {}

    def _record(self, name, *args, **kwargs):
        self.calls.append((name, args, kwargs))
        if name in self.exceptions:
            raise self.exceptions[name]

    def start_sys(self):
        self._record('start_sys')

    def stop_sys(self):
        self._record('stop_sys')

    def powerdown(self):
        self._record('powerdown')

    def stop(self):
        self._record('stop')

    def estop(self):
        self._record('estop')

    def start_teach_mode(self):
        self._record('start_teach_mode')

    def end_teach_mode(self):
        self._record('end_teach_mode')

    def pause_move(self):
        self._record('pause_move')

    def resume_move(self):
        self._record('resume_move')

    def reboot(self):
        self._record('reboot')

    def movej(self, target, acceleration, velocity, time, blend_radius):
        self._record('movej', target, acceleration, velocity, time, blend_radius)
        return self._next_motion_id()

    def movel(self, target, acceleration, velocity, time, blend_radius):
        self._record('movel', target, acceleration, velocity, time, blend_radius)
        return self._next_motion_id()

    def movec(self, via, target, rad, acceleration, velocity, time, blend_radius):
        self._record('movec', via, target, rad, acceleration, velocity, time, blend_radius)
        return self._next_motion_id()

    def speedj(self, acceleration, velocities, time=0.0):
        self._record('speedj', acceleration, velocities, time)
        return self._next_motion_id()

    def speedl(self, acceleration, velocity, time=0.0, reference=None):
        self._record('speedl', acceleration, velocity, time, reference)
        return self._next_motion_id()

    def move_pvat(self, positions, velocities, accelerations, duration):
        self._record('move_pvat', positions, velocities, accelerations, duration)

    def wait_move(self, motion_id=0):
        self._record('wait_move', motion_id)

    def stop_move(self):
        self._record('stop_move')

    def skip_move(self):
        self._record('skip_move')

    def get_running_motion(self):
        self._record('get_running_motion')
        return self.running_motion_id

    def get_motion_state(self, motion_id):
        self._record('get_motion_state', motion_id)
        return self.motion_states.get(motion_id, '')

    def _next_motion_id(self):
        motion_id = self.next_motion_id
        self.next_motion_id += 1
        return motion_id

    def get_robot_state(self):
        self._record('get_robot_state')
        return self.robot_state

    def get_estop_reason(self):
        self._record('get_estop_reason')
        return self.estop_reason

    def is_disconnected(self):
        self._record('is_disconnected')
        return self.disconnected

    def is_down(self):
        self._record('is_down')
        return self.down

    def get_actual_joint_positions(self):
        self._record('get_actual_joint_positions')
        return self.actual_joint_positions

    def get_target_joint_positions(self):
        self._record('get_target_joint_positions')
        return self.target_joint_positions

    def get_actual_joint_speed(self):
        self._record('get_actual_joint_speed')
        return self.actual_joint_speed

    def get_target_joint_speed(self):
        self._record('get_target_joint_speed')
        return self.target_joint_speed

    def get_actual_joint_torques(self):
        self._record('get_actual_joint_torques')
        return self.actual_joint_torques

    def get_target_joint_torques(self):
        self._record('get_target_joint_torques')
        return self.target_joint_torques

    def get_actual_tcp_pose(self):
        self._record('get_actual_tcp_pose')
        return self.actual_tcp_pose

    def get_target_tcp_pose(self):
        self._record('get_target_tcp_pose')
        return self.target_tcp_pose

    def get_kin_data(self):
        self._record('get_kin_data')
        return FakeJointMotionData(
            actual_flange_pose=self.actual_flange_pose,
        )

    def set_do(self, device, pin, value):
        self._record('set_do', device, pin, value)
        self.digital_outputs[(device, pin)] = bool(value)

    def get_di(self, device, pin):
        self._record('get_di', device, pin)
        return self.digital_inputs.get((device, pin), False)

    def get_do(self, device, pin):
        self._record('get_do', device, pin)
        return self.digital_outputs.get((device, pin), False)

    def set_dos(self, device, pin, values):
        values = list(values)
        self._record('set_dos', device, pin, values)
        for offset, value in enumerate(values):
            self.digital_outputs[(device, pin + offset)] = bool(value)

    def get_dis(self, device, pin, num):
        self._record('get_dis', device, pin, num)
        return [
            self.digital_inputs.get((device, index), False)
            for index in range(pin, pin + num)
        ]

    def get_dos(self, device, pin, num):
        self._record('get_dos', device, pin, num)
        return [
            self.digital_outputs.get((device, index), False)
            for index in range(pin, pin + num)
        ]

    def set_ao(self, device, pin, value):
        self._record('set_ao', device, pin, value)
        self.analog_outputs[(device, pin)] = value

    def get_ai(self, device, pin):
        self._record('get_ai', device, pin)
        return self.analog_inputs.get((device, pin), 0.0)

    def get_ao(self, device, pin):
        self._record('get_ao', device, pin)
        return self.analog_outputs.get((device, pin), 0.0)

    def set_aos(self, device, pin, values):
        values = list(values)
        self._record('set_aos', device, pin, values)
        for offset, value in enumerate(values):
            self.analog_outputs[(device, pin + offset)] = float(value)

    def get_ais(self, device, pin, num):
        self._record('get_ais', device, pin, num)
        return [
            self.analog_inputs.get((device, index), 0.0)
            for index in range(pin, pin + num)
        ]

    def get_aos(self, device, pin, num):
        self._record('get_aos', device, pin, num)
        return [
            self.analog_outputs.get((device, index), 0.0)
            for index in range(pin, pin + num)
        ]

    def set_dio_mode(self, device, pin, is_output):
        self._record('set_dio_mode', device, pin, is_output)
        self.dio_modes[(device, pin)] = bool(is_output)

    def get_dio_mode(self, device, pin):
        self._record('get_dio_mode', device, pin)
        return self.dio_modes.get((device, pin), False)

    def set_led(self, mode, speed, color):
        self._record('set_led', mode, speed, color)
        self.led = {
            'mode': mode,
            'speed': speed,
            'color': list(color),
        }

    def get_signals(self, index, length):
        self._record('get_signals', index, length)
        return [
            self.signals.get(signal_index, 0)
            for signal_index in range(index, index + length)
        ]

    def set_signals(self, index, values):
        self._record('set_signals', index, values)
        for offset, value in enumerate(values):
            self.signals[index + offset] = int(value)

    def init_claw(self, force_initialization=False):
        self._record('init_claw', force_initialization)

    def set_claw(self, force, amplitude):
        self._record('set_claw', force, amplitude)
        self.claw.force = force
        self.claw.amplitude = amplitude

    def get_claw(self):
        self._record('get_claw')
        return self.claw


class FakeClawData:
    def __init__(self, force=0.0, amplitude=0.0, hold_on=False):
        self.force = force
        self.amplitude = amplitude
        self.hold_on = hold_on


class FakeJointMotionData:
    def __init__(self, actual_flange_pose=None):
        self.actual_flange_pose = actual_flange_pose or {}


class FakeRobotFactory:
    def __init__(self):
        self.calls = []

    def __call__(self, robot_ip, simulator=False):
        self.calls.append((robot_ip, simulator))
        return FakeRobot(robot_ip=robot_ip, simulator=simulator)


class FakeNode:
    def __init__(self):
        self.services = []
        self.publishers = []
        self.timers = []
        self._now = Time(sec=12, nanosec=34)

    def create_service(self, srv_type, name, callback):
        self.services.append((srv_type, name, callback))
        return callback

    def create_publisher(self, msg_type, name, depth):
        publisher = FakePublisher(msg_type, name, depth)
        self.publishers.append(publisher)
        return publisher

    def create_timer(self, period, callback):
        timer = FakeTimer(period, callback)
        self.timers.append(timer)
        return timer

    def get_clock(self):
        return FakeClock(self._now)

    def get_parameter(self, name):
        from lebai_driver.parameters import DEFAULT_JOINT_NAMES

        values = {
            'joint_names': DEFAULT_JOINT_NAMES,
            'joint_state_publish_rate': 20.0,
            'robot_state_publish_rate': 10.0,
            'joint_motion_publish_rate': 20.0,
            'io_state_publish_rate': 10.0,
            'gripper_state_publish_rate': 10.0,
            'gripper_joint_name': 'gripper_r_joint1',
            'io_state_device': 'robot',
            'io_state_digital_input_count': 0,
            'io_state_digital_output_count': 0,
            'io_state_analog_input_count': 0,
            'io_state_analog_output_count': 0,
            'io_state_dio_count': 0,
        }
        return FakeParameter(values[name])


class FakePublisher:
    def __init__(self, msg_type, name, depth):
        self.msg_type = msg_type
        self.name = name
        self.depth = depth
        self.messages = []

    def publish(self, message):
        self.messages.append(message)


class FakeTimer:
    def __init__(self, period, callback):
        self.period = period
        self.callback = callback


class FakeParameter:
    def __init__(self, value):
        self.value = value


class FakeClock:
    def __init__(self, message):
        self.message = message

    def now(self):
        return self

    def to_msg(self):
        return self.message


class FakeDiscovery:
    def __init__(self, controllers=None):
        self.controllers = controllers or []
        self.calls = []

    def resolve(self):
        self.calls.append(('resolve', (), {}))
        return self.controllers


class FakeControllerInfo:
    def __init__(
        self,
        hostname='',
        ip_address='',
        mac_address='',
        model='',
        ds_version='',
        rc_version='',
        id='',
    ):
        self.hostname = hostname
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.model = model
        self.ds_version = ds_version
        self.rc_version = rc_version
        self.id = id


class FakeStandaloneGripper:
    def __init__(self, port_name='/dev/ttyUSB0'):
        self.port_name = port_name
        self.calls = []
        self.exceptions = {}
        self.position = 0
        self.force = 0
        self.velocity = 0
        self.persistent_velocity = 0
        self.calibrated = False

    def _record(self, name, *args, **kwargs):
        self.calls.append((name, args, kwargs))
        if name in self.exceptions:
            raise self.exceptions[name]

    def set_position(self, position):
        self._record('set_position', position)
        self.position = position

    def get_current_position(self):
        self._record('get_current_position')
        return self.position

    def set_force(self, force):
        self._record('set_force', force)
        self.force = force

    def get_current_force(self):
        self._record('get_current_force')
        return self.force

    def set_velocity(self, velocity, persistent):
        self._record('set_velocity', velocity, persistent)
        if persistent:
            self.persistent_velocity = velocity
        else:
            self.velocity = velocity

    def get_current_velocity(self, persistent):
        self._record('get_current_velocity', persistent)
        if persistent:
            return self.persistent_velocity
        return self.velocity

    def do_calibration(self):
        self._record('do_calibration')
        self.calibrated = True

    def is_calibrated(self):
        self._record('is_calibrated')
        return self.calibrated

    def turn_on_auto_calibration(self):
        self._record('turn_on_auto_calibration')

    def turn_off_auto_calibration(self):
        self._record('turn_off_auto_calibration')
