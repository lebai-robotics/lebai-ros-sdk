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

from lebai_interfaces.srv import ResolveControllers

from fakes import FakeControllerInfo, FakeDiscovery, FakeNode


def _register(discovery):
    from lebai_driver.discovery_node import register_discovery_services

    node = FakeNode()
    services = register_discovery_services(node, lambda: discovery)
    callbacks = {
        name: callback
        for _srv_type, name, callback in node.services
    }
    return node, services, callbacks


def test_discovery_service_registers_sdk_category_name():
    node, services, _callbacks = _register(FakeDiscovery())

    assert [(srv_type, name) for srv_type, name, _callback in node.services] == [
        (ResolveControllers, 'discovery/resolve'),
    ]
    assert len(services) == 1


def test_resolve_controllers_converts_sdk_controller_info():
    discovery = FakeDiscovery([
        FakeControllerInfo(
            hostname='lebai-1',
            ip_address='192.168.0.10',
            mac_address='00:11:22:33:44:55',
            model='LM3',
            ds_version='1.2.3',
            rc_version='4.5.6',
            id='abc',
        ),
    ])
    _node, _services, callbacks = _register(discovery)

    response = callbacks['discovery/resolve'](
        ResolveControllers.Request(),
        ResolveControllers.Response(),
    )

    assert discovery.calls == [('resolve', (), {})]
    assert response.result.success is True
    assert len(response.controllers) == 1
    controller = response.controllers[0]
    assert controller.hostname == 'lebai-1'
    assert controller.ip_address == '192.168.0.10'
    assert controller.mac_address == '00:11:22:33:44:55'
    assert controller.model == 'LM3'
    assert controller.ds_version == '1.2.3'
    assert controller.rc_version == '4.5.6'
    assert controller.id == 'abc'


def test_resolve_controllers_maps_sdk_exception_to_result():
    discovery = FakeDiscovery()
    discovery.resolve = lambda: (_ for _ in ()).throw(RuntimeError('discovery failed'))
    _node, _services, callbacks = _register(discovery)

    response = callbacks['discovery/resolve'](
        ResolveControllers.Request(),
        ResolveControllers.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'discovery failed'


def test_discovery_node_uses_injected_factory_without_importing_pylebai():
    import rclpy

    from lebai_driver.discovery_node import LebaiDiscoveryNode

    rclpy.init()
    node = None

    try:
        node = LebaiDiscoveryNode(discovery_factory=lambda: FakeDiscovery())

        assert node.get_name() == 'lebai_discovery'
        assert len(node.discovery_services) == 1
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()
