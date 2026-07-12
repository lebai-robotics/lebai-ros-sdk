from types import SimpleNamespace

import pytest

from lebai_interfaces.msg import Result

import io_example
import lebai_tutorials_common
import move_example


class FakeLogger:
    def __init__(self):
        self.infos = []
        self.errors = []

    def info(self, message):
        self.infos.append(message)

    def error(self, message):
        self.errors.append(message)


class FakeFuture:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error

    def done(self):
        return True

    def result(self):
        if self.error is not None:
            raise self.error
        return self.response


class FakeClient:
    def __init__(self, future):
        self.future = future
        self.requests = []
        self.waits = []

    def wait_for_service(self, timeout_sec):
        self.waits.append(timeout_sec)
        return True

    def call_async(self, request):
        self.requests.append(request)
        return self.future


class FakeNode:
    def __init__(self, client):
        self.client = client
        self.logger = FakeLogger()
        self.created_clients = []

    def create_client(self, service_type, name):
        self.created_clients.append((service_type, name))
        return self.client

    def get_logger(self):
        return self.logger


class FakeRclpy:
    def __init__(self):
        self.spins = []

    def ok(self):
        return True

    def spin_once(self, node):
        self.spins.append(node)


def _response(success, code=0, message=''):
    return SimpleNamespace(
        result=Result(success=success, code=code, message=message),
    )


def _call_shared_helper(monkeypatch, future):
    client = FakeClient(future)
    node = FakeNode(client)
    fake_rclpy = FakeRclpy()
    request = object()
    monkeypatch.setattr(lebai_tutorials_common, 'rclpy', fake_rclpy, raising=False)

    outcome = lebai_tutorials_common.call_service(
        node,
        client,
        request,
        'example/service',
    )

    assert client.requests == [request]
    assert fake_rclpy.spins == [node]
    return outcome, node.logger


def test_shared_service_helper_reports_success(monkeypatch):
    outcome, logger = _call_shared_helper(
        monkeypatch,
        FakeFuture(response=_response(True)),
    )

    assert outcome is True
    assert logger.errors == []
    assert logger.infos == ['Service "example/service" succeeded.']


def test_shared_service_helper_reports_driver_failure_code_and_message(monkeypatch):
    outcome, logger = _call_shared_helper(
        monkeypatch,
        FakeFuture(response=_response(False, code=17, message='motion rejected')),
    )

    assert outcome is False
    assert logger.infos == []
    assert len(logger.errors) == 1
    assert '17' in logger.errors[0]
    assert 'motion rejected' in logger.errors[0]


def test_shared_service_helper_reports_transport_exception(monkeypatch):
    outcome, logger = _call_shared_helper(
        monkeypatch,
        FakeFuture(error=RuntimeError('connection reset')),
    )

    assert outcome is False
    assert logger.infos == []
    assert len(logger.errors) == 1
    assert 'connection reset' in logger.errors[0]


@pytest.mark.parametrize(
    ('module', 'example_type', 'method_name', 'label'),
    [
        (move_example, move_example.MoveExample, 'send_move_joint', 'motion/movej'),
        (move_example, move_example.MoveExample, 'send_move_linear', 'motion/movel'),
        (io_example, io_example.IOExample, 'set_do', 'io/set_do'),
        (io_example, io_example.IOExample, 'set_ao', 'io/set_ao'),
    ],
    ids=['movej', 'movel', 'set_do', 'set_ao'],
)
def test_service_methods_delegate_to_shared_helper(
    monkeypatch,
    module,
    example_type,
    method_name,
    label,
):
    client = FakeClient(FakeFuture())
    node = FakeNode(client)
    expected_outcome = object()
    calls = []

    def fake_call_service(call_node, call_client, request, call_label):
        calls.append((call_node, call_client, request, call_label))
        return expected_outcome

    monkeypatch.setattr(module, 'call_service', fake_call_service, raising=False)

    outcome = getattr(example_type, method_name)(node)

    assert outcome is expected_outcome
    assert len(calls) == 1
    assert calls[0][0:2] == (node, client)
    assert calls[0][3] == label
    assert client.waits == [1.0]


@pytest.mark.parametrize(
    ('module', 'example_name', 'method_names'),
    [
        (move_example, 'MoveExample', ('send_move_joint', 'send_move_linear')),
        (io_example, 'IOExample', ('set_do', 'set_ao')),
    ],
    ids=['move', 'io'],
)
@pytest.mark.parametrize(
    ('method_outcomes', 'expected_outcome'),
    [((True, True), True), ((False, True), False)],
    ids=['success', 'partial-failure'],
)
def test_run_combines_command_outcomes_and_destroys_node(
    monkeypatch,
    module,
    example_name,
    method_names,
    method_outcomes,
    expected_outcome,
):
    class FakeExample:
        def __init__(self):
            self.calls = []
            self.destroyed = False
            self.outcomes = iter(method_outcomes)

        def __getattr__(self, name):
            if name not in method_names:
                raise AttributeError(name)

            def call():
                self.calls.append(name)
                return next(self.outcomes)

            return call

        def destroy_node(self):
            self.destroyed = True

    example = FakeExample()
    monkeypatch.setattr(module, example_name, lambda: example)

    assert module.run() is expected_outcome
    assert example.calls == list(method_names)
    assert example.destroyed is True


@pytest.mark.parametrize('module', [move_example, io_example], ids=['move', 'io'])
@pytest.mark.parametrize(
    ('run_outcome', 'exit_code'),
    [(True, 0), (False, 1)],
    ids=['success', 'failure'],
)
def test_main_exits_with_run_outcome_and_always_shuts_down(
    monkeypatch,
    module,
    run_outcome,
    exit_code,
):
    lifecycle = []
    monkeypatch.setattr(module, 'run', lambda: run_outcome)
    monkeypatch.setattr(module.rclpy, 'init', lambda: lifecycle.append('init'))
    monkeypatch.setattr(module.rclpy, 'shutdown', lambda: lifecycle.append('shutdown'))

    with pytest.raises(SystemExit) as raised:
        module.main()

    assert raised.value.code == exit_code
    assert lifecycle == ['init', 'shutdown']
