import rospy
from lebai_interfaces.msg import ControllerInfo
from lebai_interfaces.srv import ResolveControllers

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok
from lebai_driver.ros_adapter import RosNodeAdapter


class LebaiDiscoveryNode:
    def __init__(self, node, discovery_factory=None):
        self._factory = discovery_factory or _default_discovery_factory
        self.service = node.create_service(ResolveControllers, 'discovery/resolve', self.resolve)

    def resolve(self, request, response):
        try:
            response.controllers = [_controller_info(item) for item in self._factory().resolve()]
        except Exception as exc:
            response.result = fail(exception_message(exc))
        else:
            response.result = ok()
        return response


def _controller_info(data):
    def field(name):
        value = data.get(name, '') if isinstance(data, dict) else getattr(data, name, '')
        return str(value)

    return ControllerInfo(hostname=field('hostname'), ip_address=field('ip_address'),
                          mac_address=field('mac_address'), model=field('model'),
                          ds_version=field('ds_version'), rc_version=field('rc_version'), id=field('id'))


def _default_discovery_factory():
    from pylebai.zeroconf import Discovery

    return Discovery()


def main():
    rospy.init_node('lebai_discovery')
    LebaiDiscoveryNode(RosNodeAdapter())
    rospy.spin()
