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

from lebai_interfaces.srv import GetSignals, SetLed, SetSignals

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok
from lebai_driver.sdk_gate import exclusive_access


def register_led_signal_services(node, connection, callback_group=None, sdk_gate=None):
    definitions = [
        (SetLed, 'led/set_led', _set_led),
        (GetSignals, 'signal/get_signals', _get_signals),
        (SetSignals, 'signal/set_signals', _set_signals),
    ]

    services = []
    for srv_type, service_name, handler in definitions:
        services.append(
            node.create_service(
                srv_type,
                service_name,
                _make_led_signal_callback(connection, handler, sdk_gate),
                callback_group=callback_group,
            )
        )
    return services


def _make_led_signal_callback(connection, handler, sdk_gate=None):
    def callback(request, response):
        try:
            with exclusive_access(sdk_gate):
                handler(connection.robot, request, response)
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _set_led(robot, request, response):
    del response
    mode = int(request.mode)
    speed = int(request.speed)
    color = [int(value) for value in request.color]
    if mode < 0 or mode > 6:
        raise ValueError('mode must be between 0 and 6')
    if speed < 0 or speed > 3:
        raise ValueError('speed must be between 0 and 3')
    if len(color) > 4:
        raise ValueError('color must contain at most 4 values')
    if any(value < 0 or value > 15 for value in color):
        raise ValueError('color values must be between 0 and 15')
    robot.set_led(mode, speed, color)


def _get_signals(robot, request, response):
    response.values = [int(value) for value in robot.get_signals(request.index, request.length)]


def _set_signals(robot, request, response):
    del response
    robot.set_signals(request.index, list(request.values))
