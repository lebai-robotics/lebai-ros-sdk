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

import rclpy
from rclpy.node import Node

from lebai_interfaces.msg import ControllerInfo
from lebai_interfaces.srv import ResolveControllers

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok


class LebaiDiscoveryNode(Node):
    def __init__(self, discovery_factory=None):
        super().__init__('lebai_discovery')
        self.discovery_services = register_discovery_services(
            self,
            discovery_factory or _default_discovery_factory,
        )


def register_discovery_services(node, discovery_factory):
    return [
        node.create_service(
            ResolveControllers,
            'discovery/resolve',
            _make_resolve_callback(discovery_factory),
        )
    ]


def _make_resolve_callback(discovery_factory):
    def callback(request, response):
        del request
        try:
            response.controllers = [
                _controller_info_from_sdk(controller)
                for controller in discovery_factory().resolve()
            ]
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response

    return callback


def _controller_info_from_sdk(data):
    return ControllerInfo(
        hostname=str(_value(data, 'hostname')),
        ip_address=str(_value(data, 'ip_address')),
        mac_address=str(_value(data, 'mac_address')),
        model=str(_value(data, 'model')),
        ds_version=str(_value(data, 'ds_version')),
        rc_version=str(_value(data, 'rc_version')),
        id=str(_value(data, 'id')),
    )


def _value(data, name, default=''):
    if isinstance(data, dict):
        return data.get(name, default)
    return getattr(data, name, default)


def _default_discovery_factory():
    from pylebai.zeroconf import Discovery

    return Discovery()


def main(args=None):
    rclpy.init(args=args)
    node = LebaiDiscoveryNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
