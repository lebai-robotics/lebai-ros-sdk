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
            'joint_names',
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
        assert list(node.get_parameter('joint_names').value) == [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6',
        ]
        assert node.get_name() == 'lebai_driver'
        assert node.trajectory_action is not None
        assert node.gripper_action is not None
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_node_separates_status_and_service_callback_groups():
    from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    try:
        node = LebaiDriverNode(robot_factory=FakeRobotFactory())

        assert isinstance(node.status_callback_group, MutuallyExclusiveCallbackGroup)
        assert isinstance(node.service_callback_group, MutuallyExclusiveCallbackGroup)
        assert node.status_callback_group is not node.service_callback_group
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_node_prioritizes_model_joint_state_callback_group():
    from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    try:
        node = LebaiDriverNode(robot_factory=FakeRobotFactory())

        assert isinstance(
            node.model_state_callback_group,
            MutuallyExclusiveCallbackGroup,
        )
        assert node.model_state_callback_group is not node.status_callback_group
        assert node.model_state_callback_group is not node.service_callback_group
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


def test_driver_node_uses_separate_status_connection():
    from lebai_driver.driver_node import LebaiDriverNode

    rclpy.init()
    node = None
    robot_factory = FakeRobotFactory()
    try:
        node = LebaiDriverNode(robot_factory=robot_factory)

        assert node.status_connection is not node.connection
        assert node.status_connection.robot_ip == node.connection.robot_ip
        assert node.status_connection.simulator == node.connection.simulator

        _status_robot = node.status_connection.robot
        _command_robot = node.connection.robot

        assert _status_robot is not _command_robot
        assert robot_factory.calls == [
            ('127.0.0.1', False),
            ('127.0.0.1', False),
        ]
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
