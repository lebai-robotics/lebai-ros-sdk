from contextlib import contextmanager, nullcontext
from threading import Condition, Event, Lock


def exclusive_access(sdk_gate):
    if sdk_gate is None:
        return nullcontext()
    return sdk_gate.exclusive_access()


@contextmanager
def service_robot(connection, sdk_gate):
    with exclusive_access(sdk_gate):
        robot = connection.robot
        yield sdk_gate.admission.methods(robot) if sdk_gate is not None else robot


class _SdkMethods:
    """Admit each method lookup within an already counted service or polling callback."""

    def __init__(self, sdk, admission):
        self._sdk = sdk
        self._admission = admission

    def __getattr__(self, name):
        self._admission.require_open()
        return getattr(self._sdk, name)


class SdkAdmission:
    """Close admission for a node and drain outstanding work without serializing it."""

    def __init__(self, shutdown_requested=lambda: False):
        self._shutdown_requested = shutdown_requested
        self.closed = Event()
        self._state = Condition()
        self._active = 0

    def is_closed(self):
        return self.closed.is_set() or self._shutdown_requested()

    def require_open(self):
        if self.is_closed():
            raise RuntimeError('driver is shutting down')

    def methods(self, sdk):
        return _SdkMethods(sdk, self)

    @contextmanager
    def command(self):
        with self.access() as admitted:
            if not admitted:
                raise RuntimeError('driver is shutting down')
            yield

    @contextmanager
    def access(self):
        with self._state:
            admitted = not self.is_closed()
            if admitted:
                self._active += 1
        try:
            yield admitted
        finally:
            if admitted:
                with self._state:
                    self._active -= 1
                    if self.closed.is_set() and not self._active:
                        self._state.notify_all()

    def shutdown(self):
        with self._state:
            self.closed.set()
            self._state.wait_for(lambda: self._active == 0)


class StatusServiceGate:
    def __init__(self, admission=None):
        self.admission = admission or SdkAdmission()
        self._sdk_lock = Lock()
        self._pending_lock = Lock()
        self._pending_exclusive = 0

    @contextmanager
    def status_access(self):
        with self._pending_lock:
            if self._pending_exclusive:
                yield False
                return

        acquired = self._sdk_lock.acquire(blocking=False)
        if not acquired:
            yield False
            return

        try:
            with self._pending_lock:
                enabled = self._pending_exclusive == 0
            with self.admission.access() as admitted:
                yield enabled and admitted
        finally:
            self._sdk_lock.release()

    @contextmanager
    def exclusive_access(self):
        self.admission.require_open()
        with self._pending_lock:
            self._pending_exclusive += 1

        acquired = False
        try:
            self._sdk_lock.acquire()
            acquired = True
            with self.admission.command():
                yield
        finally:
            if acquired:
                self._sdk_lock.release()
            with self._pending_lock:
                self._pending_exclusive -= 1
