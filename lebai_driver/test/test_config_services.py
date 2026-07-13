from lebai_interfaces.srv import LoadResourceList

from fakes import FakeNode, FakeRobot


def _register(robot):
    from lebai_driver.connection import RobotConnection
    from lebai_driver.config_services import register_config_services

    node = FakeNode()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    services = register_config_services(node, connection)
    callbacks = {
        name: callback
        for _srv_type, name, callback in node.services
    }
    return node, services, callbacks


def test_config_services_register_sdk_category_names():
    robot = FakeRobot()

    node, services, _callbacks = _register(robot)

    assert [(srv_type, name) for srv_type, name, _callback in node.services] == [
        (LoadResourceList, 'config/load_tcp_list'),
        (LoadResourceList, 'config/load_pose_list'),
        (LoadResourceList, 'config/load_frame_list'),
        (LoadResourceList, 'config/load_trajectory_list'),
    ]
    assert len(services) == 4


def test_config_list_services_forward_directory_and_return_names():
    robot = FakeRobot()
    robot.resource_lists['tcp']['tools'] = ['flange_tcp', 'camera_tcp']
    robot.resource_lists['pose']['waypoints'] = ['home', 'pick']
    robot.resource_lists['frame']['fixtures'] = ['table', 'conveyor']
    robot.resource_lists['trajectory']['jobs'] = ['cycle_a', 'cycle_b']
    _node, _services, callbacks = _register(robot)

    tcp_response = callbacks['config/load_tcp_list'](
        LoadResourceList.Request(directory='tools'),
        LoadResourceList.Response(),
    )
    pose_response = callbacks['config/load_pose_list'](
        LoadResourceList.Request(directory='waypoints'),
        LoadResourceList.Response(),
    )
    frame_response = callbacks['config/load_frame_list'](
        LoadResourceList.Request(directory='fixtures'),
        LoadResourceList.Response(),
    )
    trajectory_response = callbacks['config/load_trajectory_list'](
        LoadResourceList.Request(directory='jobs'),
        LoadResourceList.Response(),
    )

    assert robot.calls == [
        ('load_tcp_list', ('tools',), {}),
        ('load_pose_list', ('waypoints',), {}),
        ('load_frame_list', ('fixtures',), {}),
        ('load_trajectory_list', ('jobs',), {}),
    ]
    assert tcp_response.result.success is True
    assert list(tcp_response.names) == ['flange_tcp', 'camera_tcp']
    assert pose_response.result.success is True
    assert list(pose_response.names) == ['home', 'pick']
    assert frame_response.result.success is True
    assert list(frame_response.names) == ['table', 'conveyor']
    assert trajectory_response.result.success is True
    assert list(trajectory_response.names) == ['cycle_a', 'cycle_b']


def test_config_list_services_convert_entries_to_strings():
    robot = FakeRobot()
    robot.resource_lists['tcp'][''] = ['tcp_1', 2]
    _node, _services, callbacks = _register(robot)

    response = callbacks['config/load_tcp_list'](
        LoadResourceList.Request(directory=''),
        LoadResourceList.Response(),
    )

    assert response.result.success is True
    assert list(response.names) == ['tcp_1', '2']


def test_config_list_service_maps_sdk_exception_to_result():
    robot = FakeRobot()
    robot.exceptions['load_pose_list'] = RuntimeError('pose list unavailable')
    _node, _services, callbacks = _register(robot)

    response = callbacks['config/load_pose_list'](
        LoadResourceList.Request(directory='waypoints'),
        LoadResourceList.Response(),
    )

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'pose list unavailable'
