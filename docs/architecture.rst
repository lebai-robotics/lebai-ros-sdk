节点和参数
==========

驱动节点
--------

``lebai_driver`` 通过 ``driver.launch`` 启动，默认节点名为
``/lebai/lebai_driver``。它提供机器人状态话题、控制服务，以及机械臂轨迹和
内置夹爪的 action。连接控制器的命令见 :doc:`quickstart`。

.. _node-launch-parameters:

常用参数
--------

.. list-table::
   :header-rows: 1
   :widths: 37 33 30
   :class: launch-parameters

   * - 参数
     - 默认值
     - 用途
   * - ``robot_ip``
     - ``127.0.0.1``
     - 真实控制器或仿真控制器的地址。
   * - ``simulator``
     - ``false``
     - 启用 Python SDK 的仿真模式。
   * - ``namespace``
     - ``lebai``
     - 节点、话题和服务的命名空间。
   * - ``joint_names``
     - ``[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6]``
     - 按控制器顺序排列的六个机械臂关节名。
   * - ``trajectory_action_name``
     - ``/lebai_trajectory_controller``
     - 机械臂轨迹 action 的绝对名称。
   * - ``gripper_action_name``
     - ``/lebai_gripper_controller/gripper_cmd``
     - 内置夹爪 action 的绝对名称。
   * - ``gripper_joint_name``
     - ``gripper_r_joint1``
     - 内置夹爪模型的主动关节名。
   * - ``publish_robot_description``
     - ``true``
     - 加载 URDF 参数并启动 ``robot_state_publisher``。
   * - ``robot_model``
     - ``lm3_with_gripper.xacro``
     - ``lebai_lm3_support/urdf`` 下的模型文件。

在同一个 ROS master 下运行多个驱动时，为每个驱动设置独立的命名空间和 action
名称，并配置各客户端使用对应的 action 名称。

.. _driver-status-rates:

状态发布频率参数
----------------

.. list-table::
   :header-rows: 1
   :widths: 37 33 30
   :class: launch-parameters

   * - 参数
     - 默认值
     - 对应话题
   * - ``joint_state_publish_rate``
     - ``20.0`` Hz
     - ``/lebai/status/joint_states`` 和 ``/lebai/model/joint_states``
   * - ``robot_state_publish_rate``
     - ``10.0`` Hz
     - ``/lebai/status/robot``
   * - ``joint_motion_publish_rate``
     - ``20.0`` Hz
     - ``/lebai/status/joint_motion``
   * - ``io_state_publish_rate``
     - ``10.0`` Hz
     - ``/lebai/io/state``
   * - ``gripper_state_publish_rate``
     - ``10.0`` Hz
     - ``/lebai/claw/state`` 和 ``/lebai/claw/joint_states``

发布频率必须大于 0。消息类型和查询命令见 :doc:`interfaces/topics`。

.. _driver-io-parameters:

I/O 状态参数
------------

.. list-table::
   :header-rows: 1
   :widths: 37 33 30
   :class: launch-parameters

   * - 参数
     - 默认值
     - 用途
   * - ``io_state_device``
     - ``robot``
     - I/O 状态发布器读取的设备。
   * - ``io_state_digital_input_count``
     - ``0``
     - 读取的数字输入数量。
   * - ``io_state_digital_output_count``
     - ``0``
     - 读取的数字输出数量。
   * - ``io_state_analog_input_count``
     - ``0``
     - 读取的模拟输入数量。
   * - ``io_state_analog_output_count``
     - ``0``
     - 读取的模拟输出数量。
   * - ``io_state_dio_count``
     - ``0``
     - 读取 DIO 模式的引脚数量。

每组 I/O 从 0 号引脚开始读取，数量为 0 时对应的状态数组为空。

机器人模型和 TF
---------------

默认启动的 ``robot_state_publisher`` 使用 ``/lebai/robot_description`` 参数，
订阅 ``/lebai/model/joint_states``，并发布全局的 ``/tf`` 和 ``/tf_static``。
LM3 可以用 ``lm3.xacro`` 加载本体模型，或用 ``lm3_with_gripper.xacro`` 加载带
夹爪模型。若由 MoveIt 或其他节点发布同一模型的 TF，可将
``publish_robot_description`` 设为 ``false``，避免重复发布。

发现节点
--------

``discovery.launch`` 启动独立的控制器发现节点。默认命名空间为 ``lebai``，
发现服务为 ``/lebai/discovery/resolve``。启动和调用命令见 :doc:`quickstart`。

独立串口夹爪节点
----------------

``serial_gripper.launch`` 启动串口夹爪节点。``port_name`` 默认为
``/dev/ttyUSB0``，``namespace`` 默认为 ``lebai``，
``gripper_state_publish_rate`` 默认为 ``10.0`` Hz。节点发布
``/lebai/gripper/state``，操作方式见 :doc:`quickstart`。
