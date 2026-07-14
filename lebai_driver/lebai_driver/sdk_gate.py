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

from contextlib import contextmanager, nullcontext
from threading import Lock


def exclusive_access(sdk_gate):
    if sdk_gate is None:
        return nullcontext()
    return sdk_gate.exclusive_access()


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
