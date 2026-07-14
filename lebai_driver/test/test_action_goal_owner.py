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

from threading import Barrier, Thread

import pytest


def _owner_class():
    try:
        from lebai_driver.action_goal_owner import ActionGoalOwner
    except ModuleNotFoundError:
        pytest.fail('ActionGoalOwner is not implemented', pytrace=False)
    return ActionGoalOwner


def _new_owner():
    return _owner_class()()


def test_action_goal_owner_atomically_reserves_one_goal():
    owner = _new_owner()
    barrier = Barrier(3)
    results = {}

    def reserve(goal_id):
        barrier.wait()
        results[goal_id] = owner.try_reserve(goal_id)

    threads = [Thread(target=reserve, args=(goal_id,)) for goal_id in ('a', 'b')]
    for thread in threads:
        thread.start()
    barrier.wait()
    for thread in threads:
        thread.join(timeout=1.0)

    assert sorted(results.values()) == [False, True]
    winner = next(goal_id for goal_id, reserved in results.items() if reserved)
    loser = next(goal_id for goal_id, reserved in results.items() if not reserved)
    assert owner.is_owner(winner) is True
    assert owner.is_owner(loser) is False


def test_action_goal_owner_ignores_stale_release():
    owner = _new_owner()

    assert owner.try_reserve('first') is True
    assert owner.release('stale') is False
    assert owner.is_owner('first') is True
    assert owner.release('first') is True
    assert owner.is_owner('first') is False
    assert owner.try_reserve('second') is True


def test_action_goal_owner_treats_none_as_a_regular_goal_id():
    owner = _new_owner()

    assert owner.try_reserve(None) is True
    assert owner.is_owner(None) is True
    assert owner.try_reserve('second') is False
    assert owner.release(None) is True


def test_action_goal_owner_reclaims_only_expired_pending_reservation():
    class Clock:
        now = 10.0

        def monotonic(self):
            return self.now

    clock = Clock()
    owner = _owner_class()(
        pending_timeout_sec=1.0,
        monotonic=clock.monotonic,
    )

    assert owner.try_reserve('pending') is True
    clock.now = 10.5
    assert owner.try_reserve('too-soon') is False
    clock.now = 11.0
    assert owner.try_reserve('replacement') is True
    assert owner.activate('replacement') is True
    clock.now = 20.0
    assert owner.try_reserve('cannot-reclaim-active') is False
