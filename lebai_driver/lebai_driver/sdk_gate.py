from contextlib import contextmanager
from threading import Lock


class StatusServiceGate:
    def __init__(self):
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
            yield enabled
        finally:
            self._sdk_lock.release()

    @contextmanager
    def exclusive_access(self):
        with self._pending_lock:
            self._pending_exclusive += 1

        acquired = False
        try:
            self._sdk_lock.acquire()
            acquired = True
            yield
        finally:
            if acquired:
                self._sdk_lock.release()
            with self._pending_lock:
                self._pending_exclusive -= 1
