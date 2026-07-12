import rclpy

from fakes import FakeRobotFactory


def test_driver_node_declares_runtime_parameters():
    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    try:
        node = LebaiDriverNode(robot_factory=FakeRobotFactory())

        expected_names = {
            'robot_ip',
            'simulator',
            'namespace',
            'joint_state_publish_rate',
            'robot_state_publish_rate',
            'joint_motion_publish_rate',
            'io_state_publish_rate',
            'gripper_state_publish_rate',
            'gripper_joint_name',
            'io_state_device',
            'io_state_digital_input_count',
            'io_state_digital_output_count',
            'io_state_analog_input_count',
            'io_state_analog_output_count',
            'io_state_dio_count',
        }

        for name in expected_names:
            assert node.has_parameter(name)
        assert not node.has_parameter('joint_names')
        assert node.get_parameter('gripper_joint_name').value == 'gripper_r_joint1'
        assert node.get_name() == 'lebai_driver'
        assert node.trajectory_action is not None
        assert node.gripper_action is not None
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_node_isolates_services_from_default_group():
    from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

    from lebai_driver.driver_node import LebaiDriverNode
    from lebai_driver.sdk_gate import StatusServiceGate

    rclpy.init()
    node = None
    try:
        node = LebaiDriverNode(robot_factory=FakeRobotFactory())

        assert isinstance(node.service_callback_group, MutuallyExclusiveCallbackGroup)
        assert isinstance(node.service_sdk_gate, StatusServiceGate)
        assert not hasattr(node, 'status_callback_group')
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_node_preserves_single_sdk_connection_for_status_and_motion():
    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    robot_factory = FakeRobotFactory()
    try:
        node = LebaiDriverNode(robot_factory=robot_factory)

        assert not hasattr(node, 'model_state_callback_group')
        assert not hasattr(node, 'status_connection')

        _robot = node.connection.robot

        assert _robot.robot_ip == '127.0.0.1'
        assert robot_factory.calls == [('127.0.0.1', False)]
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_main_uses_multithreaded_executor_for_actions():
    from rclpy.executors import MultiThreadedExecutor

    from lebai_driver.driver_node import create_executor

    rclpy.init()
    executor = None
    try:
        executor = create_executor()
        assert isinstance(executor, MultiThreadedExecutor)
    finally:
        if executor is not None:
            executor.shutdown()
        rclpy.shutdown()
