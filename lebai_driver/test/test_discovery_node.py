from io import BytesIO
import sys
from types import SimpleNamespace
from unittest.mock import Mock

from lebai_interfaces.srv import ResolveControllers

from lebai_driver.ros_adapter import RosNodeAdapter


def test_resolve_converts_controllers_and_serializes_errors(fake_rospy, monkeypatch):
    from lebai_driver.discovery_node import LebaiDiscoveryNode

    monkeypatch.setitem(sys.modules, 'pylebai.zeroconf', None)
    controller = dict(hostname='arm', ip_address='10.0.0.1', mac_address='aa:bb',
                      model='LM3', ds_version='1', rc_version='2', id=123)
    factory = Mock()
    factory.return_value.resolve.side_effect = [
        [SimpleNamespace(**controller), {'hostname': 'second'}], RuntimeError('discovery failed')]
    LebaiDiscoveryNode(RosNodeAdapter(fake_rospy), discovery_factory=factory)
    service, = fake_rospy.services
    assert (service.name, service.srv_type) == ('discovery/resolve', ResolveControllers)
    factory.assert_not_called()
    response = service.handler(ResolveControllers._request_class())
    response.serialize(BytesIO())
    assert response.result.success
    first, second = response.controllers
    assert [getattr(first, key) for key in controller] == [str(v) for v in controller.values()]
    assert second.hostname == 'second' and second.ip_address == ''
    response = service.handler(ResolveControllers._request_class())
    response.serialize(BytesIO())
    assert not response.result.success and response.result.code == 1
    assert response.result.message == 'discovery failed' and response.controllers == []


def test_sdk_discovery_is_imported_on_request(fake_rospy, monkeypatch):
    from lebai_driver.discovery_node import LebaiDiscoveryNode

    monkeypatch.setitem(sys.modules, 'pylebai.zeroconf', None)
    LebaiDiscoveryNode(RosNodeAdapter(fake_rospy))
    factory = Mock()
    factory.return_value.resolve.return_value = []
    monkeypatch.setitem(sys.modules, 'pylebai.zeroconf', SimpleNamespace(Discovery=factory))
    assert fake_rospy.services[0].handler(ResolveControllers._request_class()).result.success
    factory.assert_called_once_with()


def test_discovery_does_not_open_sdk_after_shutdown_request(fake_rospy):
    from lebai_driver.discovery_node import LebaiDiscoveryNode

    factory = Mock()
    adapter = RosNodeAdapter(fake_rospy)
    node = LebaiDiscoveryNode(adapter, discovery_factory=factory)
    fake_rospy.shutdown = True
    assert not node.service.handler(ResolveControllers._request_class()).result.success
    factory.assert_not_called()
