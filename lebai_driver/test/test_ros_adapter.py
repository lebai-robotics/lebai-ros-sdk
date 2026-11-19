from lebai_interfaces.srv import Command, CommandRequest, CommandResponse
from std_msgs.msg import String


def test_service_adapter_constructs_and_returns_generated_response(fake_rospy):
    from lebai_driver.ros_adapter import RosNodeAdapter

    node = RosNodeAdapter(fake_rospy)
    request = CommandRequest()

    def callback(received_request, response):
        assert received_request is request
        assert isinstance(response, CommandResponse)
        assert not response.result.message
        response.result.message = 'done'
        return response

    service = node.create_service(Command, 'test/command', callback)

    assert fake_rospy.services == [service]
    assert service.name == 'test/command'
    assert service.srv_type is Command
    first_response = service.handler(request)
    assert first_response.result.message == 'done'
    assert service.handler(request) is not first_response


def test_service_adapter_returns_populated_response_when_callback_returns_none(fake_rospy):
    from lebai_driver.ros_adapter import RosNodeAdapter

    def callback(_request, response):
        response.result.message = 'done'

    service = RosNodeAdapter(fake_rospy).create_service(Command, 'test/command', callback)
    response = service.handler(CommandRequest())

    assert isinstance(response, CommandResponse)
    assert response.result.message == 'done'


def test_timer_discards_ros_event_and_stops_dispatch_after_shutdown(fake_rospy):
    from lebai_driver.ros_adapter import RosNodeAdapter

    node = RosNodeAdapter(fake_rospy)
    calls = []

    def callback():
        calls.append('tick')

    timer = node.create_timer(0.125, callback)

    assert fake_rospy.timers == [timer]
    assert timer.duration.to_nsec() == 125_000_000
    timer.callback(object())
    fake_rospy.shutdown = True
    timer.callback(object())
    assert calls == ['tick']


def test_private_parameter_uses_tilde_name_and_default(fake_rospy):
    from lebai_driver.ros_adapter import RosNodeAdapter

    node = RosNodeAdapter(fake_rospy)
    fake_rospy.parameters['~robot_ip'] = '192.168.1.100'

    assert node.parameter('robot_ip', '127.0.0.1') == '192.168.1.100'
    assert node.parameter('simulator', False) is False
    assert fake_rospy.parameter_calls == [('~robot_ip', '127.0.0.1'), ('~simulator', False)]


def test_publisher_defaults_to_queue_size_ten(fake_rospy):
    from lebai_driver.ros_adapter import RosNodeAdapter

    node = RosNodeAdapter(fake_rospy)
    publisher = node.create_publisher(String, 'status/test')

    assert fake_rospy.publishers == [publisher]
    assert publisher.name == 'status/test'
    assert publisher.msg_type is String
    assert publisher.queue_size == 10


def test_now_uses_ros_time(fake_rospy):
    from lebai_driver.ros_adapter import RosNodeAdapter

    assert RosNodeAdapter(fake_rospy).now() is fake_rospy.stamp


def test_logging_forwards_messages_and_arguments(fake_rospy):
    from lebai_driver.ros_adapter import RosNodeAdapter

    node = RosNodeAdapter(fake_rospy)
    node.loginfo('Connected to %s', '127.0.0.1')
    node.logerr('Disconnected', exc_info=True)

    assert fake_rospy.logs == [
        ('info', ('Connected to %s', '127.0.0.1'), {}),
        ('error', ('Disconnected',), {'exc_info': True}),
    ]


def test_on_shutdown_registers_callback(fake_rospy):
    from lebai_driver.ros_adapter import RosNodeAdapter

    node = RosNodeAdapter(fake_rospy)

    def callback():
        pass

    node.on_shutdown(callback)

    assert fake_rospy.shutdown_callbacks == [callback]
