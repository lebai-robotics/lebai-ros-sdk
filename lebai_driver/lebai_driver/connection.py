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

from threading import Lock


class RobotConnection:
    def __init__(self, robot_ip, simulator=False, robot_factory=None):
        if not robot_ip:
            raise ValueError('robot_ip is required')

        self.robot_ip = robot_ip
        self.simulator = simulator
        self._robot_factory = robot_factory or _default_robot_factory
        self._robot = None
        self._initialization_lock = Lock()

    @property
    def robot(self):
        if self._robot is None:
            with self._initialization_lock:
                if self._robot is None:
                    robot = self._robot_factory(
                        self.robot_ip,
                        simulator=self.simulator,
                    )
                    self._robot = robot
        return self._robot


def _default_robot_factory(robot_ip, simulator=False):
    import pylebai

    return pylebai.Robot(robot_ip, simulator=simulator)
