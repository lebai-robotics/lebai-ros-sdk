from contextlib import contextmanager

from lebai_interfaces.srv import Command, GetClaw, SetClaw

from fakes import FakeClawData, FakeNode, FakeRobot


def _register(robot):
    from lebai_driver.claw_services import register_claw_services
    from lebai_driver.connection import RobotConnection

    node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    services = register_claw_services(node, connection)
    callbacks = {
        name: callback
        for _srv_type, name, callback in node.services
    }
    return node, services, callbacks


def test_claw_services_register_sdk_category_names():
    node, services, _callbacks = _register(FakeRobot())

    assert [(srv_type, name) for srv_type, name, _callback in node.services] == [
        (Command, 'claw/init_claw'),
        (SetClaw, 'claw/set_claw'),
        (GetClaw, 'claw/get_claw'),
    ]
    assert len(services) == 3


def test_init_claw_uses_non_forced_initialization():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    response = callbacks['claw/init_claw'](Command.Request(), Command.Response())

    assert robot.calls == [('init_claw', (False,), {})]
    assert response.result.success is True


def test_claw_service_wraps_sdk_call_with_exclusive_gate():
    from lebai_driver.claw_services import register_claw_services
    from lebai_driver.connection import RobotConnection

    class RecordingGate:
        def __init__(self):
            self.events = []

        @contextmanager
        def exclusive_access(self):
            self.events.append('enter')
            yield
            self.events.append('exit')

    class GuardedRobot(FakeRobot):
        def __init__(self, gate):
            super().__init__()
            self._gate = gate

        def init_claw(self, force):
            assert self._gate.events == ['enter']
            super().init_claw(force)

    node = FakeNode()
    gate = RecordingGate()
    robot = GuardedRobot(gate)
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    register_claw_services(node, connection, sdk_gate=gate)
    callback = dict((name, callback) for _srv_type, name, callback in node.services)[
        'claw/init_claw'
    ]

    response = callback(Command.Request(), Command.Response())

    assert gate.events == ['enter', 'exit']
    assert robot.calls == [('init_claw', (False,), {})]
    assert response.result.success is True


def test_set_claw_maps_request_to_sdk_call():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)
    request = SetClaw.Request(force=42.0, amplitude=73.0)

    response = callbacks['claw/set_claw'](request, SetClaw.Response())

    assert robot.calls == [('set_claw', (42.0, 73.0), {})]
    assert response.result.success is True


def test_get_claw_converts_sdk_data_to_state_message():
    robot = FakeRobot()
    robot.claw = FakeClawData(force=12.5, amplitude=88.0, hold_on=True)
    _node, _services, callbacks = _register(robot)

    response = callbacks['claw/get_claw'](GetClaw.Request(), GetClaw.Response())

    assert robot.calls == [('get_claw', (), {})]
    assert response.result.success is True
    assert response.state.connected is True
    assert response.state.force == 12.5
    assert response.state.amplitude == 88.0
    assert response.state.hold_on is True


def test_claw_service_maps_sdk_exception_to_result():
    robot = FakeRobot()
    robot.exceptions['get_claw'] = RuntimeError('claw unavailable')
    _node, _services, callbacks = _register(robot)

    response = callbacks['claw/get_claw'](GetClaw.Request(), GetClaw.Response())

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'claw unavailable'
