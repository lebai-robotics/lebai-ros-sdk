from io import BytesIO
from unittest.mock import Mock

import pytest

from lebai_interfaces.msg import Result
from lebai_interfaces.srv import LoadResourceList

from lebai_driver.connection import RobotConnection
from lebai_driver.ros_adapter import RosNodeAdapter
from lebai_driver.sdk_gate import StatusServiceGate


RESOURCE_SERVICES = (
    'load_tcp_list',
    'load_pose_list',
    'load_frame_list',
    'load_trajectory_list',
)


def _register(fake_rospy, robot, gate=None):
    from lebai_driver.resource_services import register_resource_services

    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    return register_resource_services(RosNodeAdapter(fake_rospy), connection, sdk_gate=gate)


def _load_response(fake_rospy, robot, method, directory, gate=None):
    services = _register(fake_rospy, robot, gate)
    handler = next(service.handler for service in services if service.name == f'resource/{method}')
    response = handler(LoadResourceList._request_class(directory=directory))
    assert isinstance(response, LoadResourceList._response_class)
    wire = BytesIO()
    response.serialize(wire)
    return LoadResourceList._response_class().deserialize(wire.getvalue())


def test_resource_services_register_sdk_category_names(fake_rospy):
    services = _register(fake_rospy, object())

    assert services == fake_rospy.services
    assert [(service.name, service.srv_type) for service in services] == [
        (f'resource/{method}', LoadResourceList) for method in RESOURCE_SERVICES
    ]


@pytest.mark.parametrize('method,directory', [
    ('load_tcp_list', ''),
    ('load_pose_list', 'waypoints'),
    ('load_frame_list', 'fixtures'),
    ('load_trajectory_list', 'jobs'),
])
def test_resource_service_forwards_directory_and_serializes_string_names(
    fake_rospy, method, directory,
):
    robot = Mock(spec=[method])
    getattr(robot, method).return_value = iter(['工具', 17])

    decoded = _load_response(fake_rospy, robot, method, directory)

    getattr(robot, method).assert_called_once_with(directory)
    assert decoded.result == Result(success=True, code=0, message='')
    assert decoded.names == ['工具', '17']


def test_resource_sdk_error_serializes_and_releases_gate(fake_rospy):
    gate = StatusServiceGate()

    def load_pose_list(_directory):
        with gate.status_access() as allowed:
            assert allowed is False
        raise RuntimeError('pose list unavailable')

    robot = Mock(spec=['load_pose_list'])
    robot.load_pose_list.side_effect = load_pose_list

    decoded = _load_response(fake_rospy, robot, 'load_pose_list', 'waypoints', gate)

    assert decoded.names == []
    assert decoded.result == Result(success=False, code=1, message='pose list unavailable')
    with gate.status_access() as allowed:
        assert allowed is True
