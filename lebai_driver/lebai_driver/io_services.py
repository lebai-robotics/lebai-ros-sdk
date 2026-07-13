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

from lebai_interfaces.srv import (
    GetAnalogInput,
    GetAnalogInputs,
    GetAnalogOutput,
    GetAnalogOutputs,
    GetDigitalInput,
    GetDigitalInputs,
    GetDigitalOutput,
    GetDigitalOutputs,
    GetDioMode,
    SetAnalogOutput,
    SetAnalogOutputs,
    SetDigitalOutput,
    SetDigitalOutputs,
    SetDioMode,
)

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok


def register_io_services(node, connection, callback_group=None):
    definitions = [
        (SetDigitalOutput, 'io/set_do', _set_do),
        (GetDigitalInput, 'io/get_di', _get_di),
        (GetDigitalOutput, 'io/get_do', _get_do),
        (SetDigitalOutputs, 'io/set_dos', _set_dos),
        (GetDigitalInputs, 'io/get_dis', _get_dis),
        (GetDigitalOutputs, 'io/get_dos', _get_dos),
        (SetAnalogOutput, 'io/set_ao', _set_ao),
        (GetAnalogInput, 'io/get_ai', _get_ai),
        (GetAnalogOutput, 'io/get_ao', _get_ao),
        (SetAnalogOutputs, 'io/set_aos', _set_aos),
        (GetAnalogInputs, 'io/get_ais', _get_ais),
        (GetAnalogOutputs, 'io/get_aos', _get_aos),
        (SetDioMode, 'io/set_dio_mode', _set_dio_mode),
        (GetDioMode, 'io/get_dio_mode', _get_dio_mode),
    ]

    services = []
    for srv_type, service_name, handler in definitions:
        services.append(
            node.create_service(
                srv_type,
                service_name,
                _make_io_callback(connection, handler),
                callback_group=callback_group,
            )
        )
    return services


def _make_io_callback(connection, handler):
    def callback(request, response):
        try:
            with connection.sdk_access() as robot:
                handler(robot, request, response)
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _set_do(robot, request, response):
    del response
    robot.set_do(request.device, request.pin, request.value)


def _get_di(robot, request, response):
    response.value = bool(robot.get_di(request.device, request.pin))


def _get_do(robot, request, response):
    response.value = bool(robot.get_do(request.device, request.pin))


def _set_dos(robot, request, response):
    del response
    robot.set_dos(request.device, request.pin, list(request.values))


def _get_dis(robot, request, response):
    response.values = [
        bool(value)
        for value in robot.get_dis(request.device, request.pin, request.num)
    ]


def _get_dos(robot, request, response):
    response.values = [
        bool(value)
        for value in robot.get_dos(request.device, request.pin, request.num)
    ]


def _set_ao(robot, request, response):
    del response
    robot.set_ao(request.device, request.pin, request.value)


def _get_ai(robot, request, response):
    response.value = float(robot.get_ai(request.device, request.pin))


def _get_ao(robot, request, response):
    response.value = float(robot.get_ao(request.device, request.pin))


def _set_aos(robot, request, response):
    del response
    robot.set_aos(request.device, request.pin, list(request.values))


def _get_ais(robot, request, response):
    response.values = [
        float(value)
        for value in robot.get_ais(request.device, request.pin, request.num)
    ]


def _get_aos(robot, request, response):
    response.values = [
        float(value)
        for value in robot.get_aos(request.device, request.pin, request.num)
    ]


def _set_dio_mode(robot, request, response):
    del response
    robot.set_dio_mode(request.device, request.pin, request.is_output)


def _get_dio_mode(robot, request, response):
    response.is_output = bool(robot.get_dio_mode(request.device, request.pin))
