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

def test_status_access_is_available_when_no_exclusive_call_is_pending():
    from lebai_driver.sdk_gate import StatusServiceGate

    gate = StatusServiceGate()

    with gate.status_access() as enabled:
        assert enabled is True


def test_status_access_skips_while_exclusive_call_is_active():
    from lebai_driver.sdk_gate import StatusServiceGate

    gate = StatusServiceGate()

    with gate.exclusive_access():
        with gate.status_access() as enabled:
            assert enabled is False
