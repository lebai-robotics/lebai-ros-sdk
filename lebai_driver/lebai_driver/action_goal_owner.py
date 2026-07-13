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

import math
import time
from threading import Lock


_UNOWNED = object()
DEFAULT_PENDING_TIMEOUT_SEC = 1.0


class ActionGoalOwner:
    def __init__(
        self,
        pending_timeout_sec=DEFAULT_PENDING_TIMEOUT_SEC,
        monotonic=time.monotonic,
    ):
        pending_timeout_sec = float(pending_timeout_sec)
        if not math.isfinite(pending_timeout_sec) or pending_timeout_sec <= 0.0:
            raise ValueError('pending_timeout_sec must be finite and positive')
        self._lock = Lock()
        self._monotonic = monotonic
        self._pending_timeout_sec = pending_timeout_sec
        self._goal_id = _UNOWNED
        self._reserved_at = None
        self._active = False

    def try_reserve(self, goal_id):
        with self._lock:
            if self._goal_id is not _UNOWNED:
                pending_age = self._monotonic() - self._reserved_at
                if self._active or pending_age < self._pending_timeout_sec:
                    return False
            self._goal_id = goal_id
            self._reserved_at = self._monotonic()
            self._active = False
            return True

    def activate(self, goal_id):
        with self._lock:
            if self._goal_id != goal_id:
                return False
            self._active = True
            return True

    def is_owner(self, goal_id):
        with self._lock:
            return self._goal_id == goal_id

    def release(self, goal_id):
        with self._lock:
            if self._goal_id != goal_id:
                return False
            self._goal_id = _UNOWNED
            self._reserved_at = None
            self._active = False
            return True
