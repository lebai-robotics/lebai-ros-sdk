话题 Topics
===========

以下 topic 使用默认 ``/lebai`` 命名空间。修改 ``namespace`` 启动参数后，topic
前缀也会随之变化。

机器人状态
----------

.. list-table::
   :header-rows: 1

   * - Topic
     - 类型
     - 用途
   * - ``/lebai/status/robot``
     - ``lebai_interfaces/msg/RobotState``
     - 读取控制器状态、急停原因和连接状态。
   * - ``/lebai/status/joint_states``
     - ``sensor_msgs/msg/JointState``
     - 读取机器人本体关节位置、速度和力矩。
   * - ``/lebai/status/joint_motion``
     - ``lebai_interfaces/msg/JointMotion``
     - 读取实际和目标关节/TCP 运动数据。

``JointMotion`` 的 ``actual_tcp_pose``、``target_tcp_pose`` 和
``actual_flange_pose`` 字段均为 ``geometry_msgs/msg/Pose``。位置使用
``position``，姿态使用归一化四元数 ``orientation``；驱动会按控制器的
Euler ZYX 定义 ``Rz(rz) * Ry(ry) * Rx(rx)`` 转换 ``rx``、``ry``、``rz``。

常用命令：

.. code-block:: bash

   ros2 topic echo /lebai/status/robot
   ros2 topic echo /lebai/status/joint_states
   ros2 topic echo /lebai/status/joint_motion

机器人模型
----------

.. list-table::
   :header-rows: 1

   * - Topic
     - 类型
     - 用途
   * - ``/lebai/model/joint_states``
     - ``sensor_msgs/msg/JointState``
     - 给 ``robot_state_publisher`` 使用的组合关节状态。
   * - ``/tf``
     - ``tf2_msgs/msg/TFMessage``
     - 机器人动态 TF。
   * - ``/tf_static``
     - ``tf2_msgs/msg/TFMessage``
     - 机器人静态 TF。

``/lebai/model/joint_states`` 会包含机器人本体关节和 claw 映射出的 gripper
源关节，用于 RViz 显示。

IO 状态
-------

.. list-table::
   :header-rows: 1

   * - Topic
     - 类型
     - 用途
   * - ``/lebai/io/state``
     - ``lebai_interfaces/msg/IOState``
     - 读取指定设备的 IO 快照。

启动时需要设置 IO 数量参数，否则该 topic 不会轮询具体引脚。

.. code-block:: bash

   ros2 topic echo /lebai/io/state

Claw 状态
---------

.. list-table::
   :header-rows: 1

   * - Topic
     - 类型
     - 用途
   * - ``/lebai/claw/state``
     - ``lebai_interfaces/msg/ClawState``
     - 读取机器人内置 claw 的力、开合幅度和保持状态。
   * - ``/lebai/claw/joint_states``
     - ``sensor_msgs/msg/JointState``
     - 读取 claw 幅度映射出的单关节状态。

.. code-block:: bash

   ros2 topic echo /lebai/claw/state
   ros2 topic echo /lebai/claw/joint_states

独立 gripper 状态
-----------------

.. list-table::
   :header-rows: 1

   * - Topic
     - 类型
     - 用途
   * - ``/lebai/gripper/state``
     - ``lebai_interfaces/msg/GripperState``
     - 读取独立串口 gripper 的位置、力、速度和标定状态。

.. code-block:: bash

   ros2 topic echo /lebai/gripper/state
