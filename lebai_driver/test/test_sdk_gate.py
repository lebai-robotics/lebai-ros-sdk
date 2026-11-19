from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest


def test_status_access_is_available_when_idle():
    from lebai_driver.sdk_gate import StatusServiceGate

    gate = StatusServiceGate()

    with gate.status_access() as enabled:
        assert enabled is True


def test_status_access_skips_while_exclusive_call_is_active():
    from lebai_driver.sdk_gate import StatusServiceGate, exclusive_access

    gate = StatusServiceGate()

    with exclusive_access(gate):
        with gate.status_access() as enabled:
            assert enabled is False


def test_status_access_skips_while_exclusive_call_is_pending(monkeypatch):
    from lebai_driver.sdk_gate import StatusServiceGate

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

    with ThreadPoolExecutor(max_workers=1) as executor:
        exclusive_call = executor.submit(run_exclusive)
        try:
            assert acquisition_started.wait(timeout=5)
            with gate.status_access() as enabled:
                assert enabled is False
        finally:
            allow_acquisition.set()
        assert exclusive_call.result(timeout=5) == 'entered'


@pytest.mark.parametrize('access_method', ['status_access', 'exclusive_access'])
def test_gate_releases_access_after_exception(access_method):
    from lebai_driver.sdk_gate import StatusServiceGate

    gate = StatusServiceGate()

    with pytest.raises(RuntimeError, match='SDK unavailable'):
        with getattr(gate, access_method)():
            raise RuntimeError('SDK unavailable')

    with gate.status_access() as enabled:
        assert enabled is True


def test_exclusive_access_accepts_missing_gate():
    from lebai_driver.sdk_gate import exclusive_access

    with exclusive_access(None) as access:
        assert access is None
