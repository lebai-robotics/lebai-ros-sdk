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
        self.claw = FakeClawData()

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

    def set_do(self, device, pin, value):
        self._record('set_do', device, pin, value)
        self.digital_outputs[(device, pin)] = bool(value)

    def get_di(self, device, pin):
        self._record('get_di', device, pin)
        return self.digital_inputs.get((device, pin), False)

    def get_do(self, device, pin):
        self._record('get_do', device, pin)
        return self.digital_outputs.get((device, pin), False)

    def set_ao(self, device, pin, value):
        self._record('set_ao', device, pin, value)
        self.analog_outputs[(device, pin)] = value

    def get_ai(self, device, pin):
        self._record('get_ai', device, pin)
        return self.analog_inputs.get((device, pin), 0.0)

    def get_ao(self, device, pin):
        self._record('get_ao', device, pin)
        return self.analog_outputs.get((device, pin), 0.0)

    def set_dio_mode(self, device, pin, is_output):
        self._record('set_dio_mode', device, pin, is_output)
        self.dio_modes[(device, pin)] = bool(is_output)

    def get_dio_mode(self, device, pin):
        self._record('get_dio_mode', device, pin)
        return self.dio_modes.get((device, pin), False)

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


class FakeRobotFactory:
    def __init__(self):
        self.calls = []

    def __call__(self, robot_ip, simulator=False):
        self.calls.append((robot_ip, simulator))
        return FakeRobot(robot_ip=robot_ip, simulator=simulator)


class FakeNode:
    def __init__(self):
        self.services = []

    def create_service(self, srv_type, name, callback):
        self.services.append((srv_type, name, callback))
        return callback


class FakeDiscovery:
    def __init__(self, controllers=None):
        self.controllers = controllers or []
        self.calls = []

    def resolve(self):
        self.calls.append(('resolve', (), {}))
        return self.controllers


class FakeStandaloneGripper:
    def __init__(self):
        self.calls = []

    def move(self, position):
        self.calls.append(('move', (position,), {}))
