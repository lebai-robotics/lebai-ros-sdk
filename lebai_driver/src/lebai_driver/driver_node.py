import rospy

from lebai_driver.claw_services import register_claw_services
from lebai_driver.connection import RobotConnection
from lebai_driver.gripper_action import register_gripper_action
from lebai_driver.io_services import register_io_services
from lebai_driver.led_signal_services import register_led_signal_services
from lebai_driver.motion_services import register_motion_services
from lebai_driver.parameters import DEFAULT_PARAMETERS
from lebai_driver.resource_services import register_resource_services
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate
from lebai_driver.start_stop_services import register_start_stop_services
from lebai_driver.status import register_status_publishers
from lebai_driver.trajectory_action import register_trajectory_action


class LebaiDriverNode:
    def __init__(self, node, robot_factory=None):
        def parameter(name):
            return node.parameter(name, DEFAULT_PARAMETERS[name])

        self.namespace = parameter('namespace')
        self.connection = RobotConnection(parameter('robot_ip'), parameter('simulator'),
                                          robot_factory=robot_factory)
        joint_names = parameter('joint_names')
        trajectory_name = parameter('trajectory_action_name')
        gripper_name = parameter('gripper_action_name')

        self._admission = node.admission
        gate = StatusServiceGate(self._admission)
        self.status_publishers = register_status_publishers(node, self.connection, sdk_gate=gate)
        self.services = []
        for register in (register_start_stop_services, register_motion_services,
                         register_io_services, register_led_signal_services,
                         register_resource_services, register_claw_services):
            self.services.extend(register(node, self.connection, sdk_gate=gate))

        self.trajectory_action = register_trajectory_action(self.connection, joint_names,
                                                            action_name=trajectory_name,
                                                            admission=self._admission)
        self.gripper_action = register_gripper_action(self.connection, action_name=gripper_name,
                                                     admission=self._admission)

    def shutdown(self):
        self._admission.shutdown()


def main():
    rospy.init_node('lebai_driver')
    LebaiDriverNode(RosNodeAdapter())
    rospy.spin()
