from lebai_interfaces.srv import Command

from fakes import FakeNode, FakeRobot


def test_start_stop_services_register_sdk_category_names():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.start_stop_services import register_start_stop_services

    node = FakeNode()
    robot = FakeRobot()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)

    services = register_start_stop_services(node, connection)

    expected_names = [
        'start_stop/start_sys',
        'start_stop/stop_sys',
        'start_stop/powerdown',
        'start_stop/stop',
        'start_stop/estop',
        'start_stop/start_teach_mode',
        'start_stop/end_teach_mode',
        'start_stop/pause_move',
        'start_stop/resume_move',
        'start_stop/reboot',
    ]

    assert [service[1] for service in node.services] == expected_names
    assert len(services) == len(expected_names)
    assert all(service[0] is Command for service in node.services)


def test_start_stop_services_use_provided_callback_group():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.start_stop_services import register_start_stop_services

    node = FakeNode()
    robot = FakeRobot()
    callback_group = object()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)

    register_start_stop_services(node, connection, callback_group=callback_group)

    assert node.service_callback_groups
    assert set(node.service_callback_groups.values()) == {callback_group}


def test_start_stop_service_calls_sdk_method_and_returns_success():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.start_stop_services import register_start_stop_services

    node = FakeNode()
    robot = FakeRobot()
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    register_start_stop_services(node, connection)
    callback = dict((name, callback) for _srv_type, name, callback in node.services)[
        'start_stop/start_sys'
    ]

    response = callback(Command.Request(), Command.Response())

    assert robot.calls == [('start_sys', (), {})]
    assert response.result.success is True
    assert response.result.code == 0


def test_start_stop_service_calls_robot_directly_without_sdk_access_lock():
    from lebai_driver.start_stop_services import register_start_stop_services

    class DirectOnlyConnection:
        def __init__(self):
            self.robot = FakeRobot()

        def sdk_access(self):
            raise AssertionError('start/stop services should not use sdk_access')

    node = FakeNode()
    connection = DirectOnlyConnection()
    register_start_stop_services(node, connection)
    callback = dict((name, callback) for _srv_type, name, callback in node.services)[
        'start_stop/start_sys'
    ]

    response = callback(Command.Request(), Command.Response())

    assert connection.robot.calls == [('start_sys', (), {})]
    assert response.result.success is True
    assert response.result.code == 0


def test_start_stop_service_maps_sdk_exception_to_result():
    from lebai_driver.connection import RobotConnection
    from lebai_driver.start_stop_services import register_start_stop_services

    node = FakeNode()
    robot = FakeRobot()
    robot.exceptions['stop_sys'] = RuntimeError('controller offline')
    connection = RobotConnection('127.0.0.1', robot_factory=lambda *_args, **_kwargs: robot)
    register_start_stop_services(node, connection)
    callback = dict((name, callback) for _srv_type, name, callback in node.services)[
        'start_stop/stop_sys'
    ]

    response = callback(Command.Request(), Command.Response())

    assert response.result.success is False
    assert response.result.code == 1
    assert response.result.message == 'controller offline'
