节点和参数
==========

驱动节点
--------

主驱动节点通过 ``driver.launch.py`` 启动：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_ip:=127.0.0.1 simulator:=true

该节点提供机器人状态 topic、机器人控制 service，以及机械臂和夹爪 action。

常用参数
--------

.. list-table::
   :header-rows: 1

   * - 参数
     - 默认值
     - 用途
   * - ``robot_ip``
     - ``127.0.0.1``
     - 控制器地址；默认值仅适用于本机已运行的仿真控制器，真实控制器必须显式传入实际 IP。
   * - ``simulator``
     - ``false``
     - 连接仿真控制器时设为 ``true``。
   * - ``namespace``
     - ``lebai``
     - ROS 命名空间。
   * - ``publish_robot_description``
     - ``true``
     - 是否启动 ``robot_state_publisher``。
   * - ``robot_model``
     - ``lm3_with_gripper.xacro``
     - 要发布的 URDF/Xacro 模型。
   * - ``gripper_joint_name``
     - ``gripper_r_joint1``
     - claw 幅度映射到模型时使用的 gripper 关节名。

机械臂关节名不是运行时参数。状态 topic 和
``FollowJointTrajectory`` action 固定使用 ``joint_1`` 到 ``joint_6``，
不支持通过参数或 YAML 文件重映射。夹爪模型关节仍可通过单数参数
``gripper_joint_name`` 配置。

驱动 action 名称是相对名称：

.. code-block:: text

   lebai_trajectory_controller/follow_joint_trajectory
   lebai_gripper_controller/gripper_cmd

在默认 ``/lebai`` 命名空间下，它们分别解析为
``/lebai/lebai_trajectory_controller/follow_joint_trajectory`` 和
``/lebai/lebai_gripper_controller/gripper_cmd``。修改 ``namespace`` 后，
action、service 和除 TF 以外的驱动 topic 都解析到新的命名空间。

状态发布频率参数
----------------

.. list-table::
   :header-rows: 1

   * - 参数
     - 默认值
     - 对应 topic
   * - ``joint_state_publish_rate``
     - ``20.0``
     - ``/lebai/status/joint_states`` 和 ``/lebai/model/joint_states``
   * - ``robot_state_publish_rate``
     - ``10.0``
     - ``/lebai/status/robot``
   * - ``joint_motion_publish_rate``
     - ``20.0``
     - ``/lebai/status/joint_motion``
   * - ``io_state_publish_rate``
     - ``10.0``
     - ``/lebai/io/state``
   * - ``gripper_state_publish_rate``
     - ``10.0``
     - ``/lebai/claw/joint_states``

IO 状态参数
-----------

``/lebai/io/state`` 默认不轮询具体引脚。需要发布 IO 快照时，在启动时设置数量：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py \
     io_state_device:=ROBOT \
     io_state_digital_input_count:=8 \
     io_state_digital_output_count:=8 \
     io_state_analog_input_count:=2 \
     io_state_analog_output_count:=2 \
     io_state_dio_count:=0

``io_state_device`` 和 IO service 当前仍使用字符串。应使用 released SDK
的大写规范名，例如 ``ROBOT`` 或 ``FLANGE``；未知值或小写值可能由 SDK
回退到 ``ROBOT``。强类型 IO device enum 需要协调 SDK、``pylebai`` 和 ROS
接口版本，尚未提供。

机器人模型和 TF
---------------

默认启动时会同时启动 ``robot_state_publisher``。它订阅
``/lebai/model/joint_states``，并发布 ``/tf`` 和 ``/tf_static``。

``namespace`` 会作用于驱动拥有的 node 和接口，但 TF 仍使用 ROS 2 标准的
全局 ``/tf`` 和 ``/tf_static`` 传输；这里不承诺 ``world``、``base_link``
等 frame ID 也会自动隔离。

可用模型文件：

.. code-block:: text

   lm3.xacro
   lm3_l1.xacro
   lm3_with_gripper.xacro
   lm3_l1_with_gripper.xacro

公开 launch 文件
----------------

驱动包 ``lebai_driver`` 提供：

* ``driver.launch.py``：控制器连接、服务、状态 topic、action 和可选模型发布。
* ``discovery.launch.py``：局域网控制器发现。
* ``serial_gripper.launch.py``：独立串口 gripper。

模型包 ``lebai_lm3_support`` 提供：

* ``display_lm3.launch.py`` 和 ``display_lm3_l1.launch.py``：显示无 gripper
  的 LM3 或 LM3-L1。
* ``display_lm3_with_gripper.launch.py`` 和
  ``display_lm3_l1_with_gripper.launch.py``：显示带 gripper 的模型。
* ``display_gripper.launch`` 和兼容入口 ``display_gripper.py``：只显示
  gripper。
* ``standalone_lm3.launch.py``：通过 ``has_gripper`` 选择独立 LM3 显示。

MoveIt 包 ``lebai_lm3_moveit_config`` 提供 ``lm3.launch.py`` 和
``lm3_l1.launch.py``。这两个 launch 组合驱动、MoveIt、RViz、模型发布和
控制器 action；用法见 :doc:`moveit`。

发现节点
--------

.. code-block:: bash

   ros2 launch lebai_driver discovery.launch.py

服务：

.. code-block:: text

   /lebai/discovery/resolve

独立 gripper 节点
-----------------

.. code-block:: bash

   ros2 launch lebai_driver serial_gripper.launch.py port_name:=/dev/ttyUSB0

该节点用于单独连接串口 gripper，并发布 ``/lebai/gripper/state``。
