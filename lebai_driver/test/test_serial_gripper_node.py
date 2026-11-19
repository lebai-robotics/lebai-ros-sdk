from io import BytesIO
import sys
from types import SimpleNamespace
from unittest.mock import Mock, call

from lebai_interfaces.msg import GripperState
from lebai_interfaces.srv import Command, SetGripperForce, SetGripperPosition, SetGripperVelocity

from lebai_driver.ros_adapter import RosNodeAdapter


def test_serial_gripper_services_and_state_share_lazy_port(fake_rospy, monkeypatch):
    from lebai_driver.serial_gripper_node import LebaiSerialGripperNode

    monkeypatch.setitem(sys.modules, 'pylebai.gripper', None)
    fake_rospy.parameters.update({'~port_name': '/dev/custom', '~gripper_state_publish_rate': 4.0})
    factory = Mock()
    gripper = factory.return_value
    gripper.get_current_position.return_value = 12
    gripper.get_current_force.return_value = 34
    gripper.get_current_velocity.return_value = 56
    gripper.is_calibrated.return_value = True
    LebaiSerialGripperNode(RosNodeAdapter(fake_rospy), gripper_factory=factory)
    factory.assert_not_called()
    services = {service.name: service for service in fake_rospy.services}
    definitions = [
        ('set_position', SetGripperPosition, {'position': 42}, (42,)),
        ('set_force', SetGripperForce, {'force': 73}, (73,)),
        ('set_velocity', SetGripperVelocity, {'velocity': 91, 'persistent': True}, (91, True)),
        ('do_calibration', Command, {}, ()),
        ('turn_on_auto_calibration', Command, {}, ()),
        ('turn_off_auto_calibration', Command, {}, ()),
    ]
    assert len(services) == len(definitions)
    for method, service_type, values, args in definitions:
        service = services['gripper/' + method]
        assert service.srv_type == service_type
        response = service.handler(service_type._request_class(**values))
        response.serialize(BytesIO())
        assert response.result.success
        getattr(gripper, method).assert_called_once_with(*args)
    publisher, = fake_rospy.publishers
    assert (publisher.name, publisher.msg_type, publisher.queue_size) == ('gripper/state', GripperState, 10)
    publisher.publish = Mock()
    timer, = fake_rospy.timers
    assert timer.duration.to_sec() == 0.25
    timer.callback(None)
    assert gripper.mock_calls[-4:] == [
        call.get_current_position(), call.get_current_force(), call.get_current_velocity(False),
        call.is_calibrated(),
    ]
    state, = publisher.publish.call_args.args
    state.serialize(BytesIO())
    assert state.header.stamp == fake_rospy.stamp
    assert state.connected and state.calibrated
    assert (state.position, state.force, state.velocity) == (12.0, 34.0, 56.0)
    factory.assert_called_once_with('/dev/custom')


def test_default_gripper_factory_is_lazy_and_retries_failed_open(fake_rospy, monkeypatch):
    from lebai_driver.serial_gripper_node import LebaiSerialGripperNode

    monkeypatch.setitem(sys.modules, 'pylebai.gripper', None)
    LebaiSerialGripperNode(RosNodeAdapter(fake_rospy))
    factory = Mock(side_effect=RuntimeError('port unavailable'))
    monkeypatch.setitem(sys.modules, 'pylebai.gripper', SimpleNamespace(Gripper=factory))
    service = fake_rospy.services[0]
    response = service.handler(service.srv_type._request_class())
    response.serialize(BytesIO())
    assert not response.result.success and response.result.code == 1
    assert response.result.message == 'port unavailable'
    publisher, = fake_rospy.publishers
    publisher.publish = Mock()
    fake_rospy.timers[0].callback(None)
    state, = publisher.publish.call_args.args
    state.serialize(BytesIO())
    assert not state.connected and state.message == 'port unavailable'
    assert state.header.stamp == fake_rospy.stamp
    assert factory.call_args_list == [call('/dev/ttyUSB0'), call('/dev/ttyUSB0')]
