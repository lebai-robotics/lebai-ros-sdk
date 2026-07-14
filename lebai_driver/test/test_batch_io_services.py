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
    GetAnalogInputs,
    GetAnalogOutputs,
    GetDigitalInputs,
    GetDigitalOutputs,
    SetAnalogOutputs,
    SetDigitalOutputs,
)

from fakes import FakeNode, FakeRobot


def _register(robot):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.io_services import register_io_services

    node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    services = register_io_services(node, connection)
    callbacks = {
        name: callback
        for _srv_type, name, callback in node.services
    }
    return node, services, callbacks


def test_batch_io_services_register_sdk_category_names():
    robot = FakeRobot()

    node, services, _callbacks = _register(robot)

    registered = [(srv_type, name) for srv_type, name, _callback in node.services]
    assert (GetDigitalInputs, 'io/get_dis') in registered
    assert (GetDigitalOutputs, 'io/get_dos') in registered
    assert (GetAnalogInputs, 'io/get_ais') in registered
    assert (GetAnalogOutputs, 'io/get_aos') in registered
    assert (SetDigitalOutputs, 'io/set_dos') in registered
    assert (SetAnalogOutputs, 'io/set_aos') in registered
    assert len(services) == 14


def test_batch_digital_getters_return_bool_values():
    robot = FakeRobot()
    robot.digital_inputs.update({
        ('base', 1): 1,
        ('base', 2): 0,
        ('base', 3): True,
    })
    robot.digital_outputs.update({
        ('flange', 0): False,
        ('flange', 1): 1,
    })
    _node, _services, callbacks = _register(robot)

    dis_response = callbacks['io/get_dis'](
        GetDigitalInputs.Request(device='base', pin=1, num=3),
        GetDigitalInputs.Response(),
    )
    dos_response = callbacks['io/get_dos'](
        GetDigitalOutputs.Request(device='flange', pin=0, num=2),
        GetDigitalOutputs.Response(),
    )

    assert robot.calls == [
        ('get_dis', ('base', 1, 3), {}),
        ('get_dos', ('flange', 0, 2), {}),
    ]
    assert dis_response.result.success is True
    assert dis_response.values == [True, False, True]
    assert dos_response.result.success is True
    assert dos_response.values == [False, True]


def test_batch_analog_getters_return_float_values():
    robot = FakeRobot()
    robot.analog_inputs.update({
        ('base', 0): 1,
        ('base', 1): 2.5,
    })
    robot.analog_outputs.update({
        ('base', 2): 3,
        ('base', 3): 4.25,
    })
    _node, _services, callbacks = _register(robot)

    ais_response = callbacks['io/get_ais'](
        GetAnalogInputs.Request(device='base', pin=0, num=2),
        GetAnalogInputs.Response(),
    )
    aos_response = callbacks['io/get_aos'](
        GetAnalogOutputs.Request(device='base', pin=2, num=2),
        GetAnalogOutputs.Response(),
    )

    assert robot.calls == [
        ('get_ais', ('base', 0, 2), {}),
        ('get_aos', ('base', 2, 2), {}),
    ]
    assert ais_response.result.success is True
    assert list(ais_response.values) == [1.0, 2.5]
    assert aos_response.result.success is True
    assert list(aos_response.values) == [3.0, 4.25]


def test_batch_setters_map_request_to_sdk_calls():
    robot = FakeRobot()
    _node, _services, callbacks = _register(robot)

    dos_response = callbacks['io/set_dos'](
        SetDigitalOutputs.Request(device='base', pin=4, values=[True, False, True]),
        SetDigitalOutputs.Response(),
    )
    aos_response = callbacks['io/set_aos'](
        SetAnalogOutputs.Request(device='base', pin=2, values=[1.25, 2.5]),
        SetAnalogOutputs.Response(),
    )

    assert robot.calls == [
        ('set_dos', ('base', 4, [True, False, True]), {}),
        ('set_aos', ('base', 2, [1.25, 2.5]), {}),
    ]
    assert dos_response.result.success is True
    assert aos_response.result.success is True
    assert robot.digital_outputs[('base', 4)] is True
    assert robot.digital_outputs[('base', 5)] is False
    assert robot.digital_outputs[('base', 6)] is True
    assert robot.analog_outputs[('base', 2)] == 1.25
    assert robot.analog_outputs[('base', 3)] == 2.5


def test_batch_io_service_maps_sdk_exception_to_result():
    robot = FakeRobot()
    robot.exceptions['get_dis'] = RuntimeError('digital inputs unavailable')
    _node, _services, callbacks = _register(robot)

    response = callbacks['io/get_dis'](
        GetDigitalInputs.Request(device='base', pin=1, num=2),
        GetDigitalInputs.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'digital inputs unavailable'
