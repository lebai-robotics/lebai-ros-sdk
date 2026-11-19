from threading import Lock

import rospy
from lebai_interfaces.msg import GripperState
from lebai_interfaces.srv import Command, SetGripperForce, SetGripperPosition, SetGripperVelocity

from lebai_driver.errors import exception_message
from lebai_driver.result import fail, ok
from lebai_driver.ros_adapter import RosNodeAdapter


class LebaiSerialGripperNode:
    def __init__(self, node, gripper_factory=None):
        self._node = node
        self._port = node.parameter('port_name', '/dev/ttyUSB0')
        self._factory = gripper_factory or _default_gripper_factory
        self._gripper = None
        # rospy runs service and timer callbacks on different threads sharing one serial port.
        self._lock = Lock()
        rate = float(node.parameter('gripper_state_publish_rate', 10.0))
        if rate <= 0:
            raise ValueError('publish rate must be positive')

        self.services = []
        for service_type, method, fields in (
            (SetGripperPosition, 'set_position', ('position',)),
            (SetGripperForce, 'set_force', ('force',)),
            (SetGripperVelocity, 'set_velocity', ('velocity', 'persistent')),
            (Command, 'do_calibration', ()),
            (Command, 'turn_on_auto_calibration', ()),
            (Command, 'turn_off_auto_calibration', ()),
        ):
            self.services.append(node.create_service(service_type, 'gripper/' + method,
                                                     self._command(method, fields)))
        self.publisher = node.create_publisher(GripperState, 'gripper/state', 10)
        self.timer = node.create_timer(1.0 / rate, self._publish_state)

    def _get_gripper(self):
        if self._gripper is None:
            self._gripper = self._factory(self._port)
        return self._gripper

    def _command(self, method, fields):
        def callback(request, response):
            try:
                args = [getattr(request, field) for field in fields]
                with self._lock:
                    getattr(self._get_gripper(), method)(*args)
            except Exception as exc:
                response.result = fail(exception_message(exc))
            else:
                response.result = ok()
            return response

        return callback

    def _publish_state(self):
        try:
            with self._lock:
                gripper = self._get_gripper()
                state = GripperState(connected=True,
                                     position=float(gripper.get_current_position()),
                                     force=float(gripper.get_current_force()),
                                     velocity=float(gripper.get_current_velocity(False)),
                                     calibrated=bool(gripper.is_calibrated()))
        except Exception as exc:
            state = GripperState(connected=False, message=exception_message(exc))
        state.header.stamp = self._node.now()
        self.publisher.publish(state)


def _default_gripper_factory(port_name):
    from pylebai.gripper import Gripper

    return Gripper(port_name)


def main():
    rospy.init_node('lebai_serial_gripper')
    LebaiSerialGripperNode(RosNodeAdapter())
    rospy.spin()
