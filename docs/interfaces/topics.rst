话题 Topics
===========

以下表格是当前 runtime 的完整 topic 清单。除 TF 外，topic 名称在 node 中是
相对名称，并在默认 ``/lebai`` 命名空间下解析为表中路径。修改 ``namespace``
启动参数后，这些 topic 的前缀会随之变化。

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

``/lebai/status/joint_states`` 和 ``/lebai/status/joint_motion`` 使用固定的
机械臂关节顺序 ``joint_1`` 到 ``joint_6``；这些名称不是运行时参数。

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
   * - ``/lebai/robot_description``
     - ``std_msgs/msg/String``
     - ``robot_state_publisher`` 以 transient-local QoS 发布的 URDF 描述。
   * - ``/tf``
     - ``tf2_msgs/msg/TFMessage``
     - 机器人动态 TF。
   * - ``/tf_static``
     - ``tf2_msgs/msg/TFMessage``
     - 机器人静态 TF。

``/lebai/model/joint_states`` 会包含机器人本体关节和 claw 映射出的 gripper
源关节，用于 RViz 显示。

默认 ``driver.launch.py`` 在驱动命名空间中启动
``robot_state_publisher``，由该 node 发布相对 topic
``robot_description``；默认路径因此是 ``/lebai/robot_description``。只有
``publish_robot_description:=true`` 时才会启动该 node 并发布这个
transient-local URDF topic；设为 ``false`` 时该 topic 不存在。

``/tf`` 和 ``/tf_static`` 是 ROS 2 标准全局传输，不随驱动 ``namespace``
添加前缀。命名空间也不会自动修改 ``world``、``base_link`` 等 frame ID；
同时运行多套模型时需要由系统集成方规划 frame 命名。

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

启动时需要设置 IO device 和数量参数，否则该 topic 不会轮询具体引脚：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py \
     io_state_device:=ROBOT \
     io_state_digital_input_count:=8 \
     io_state_digital_output_count:=8

当前参数是字符串。请使用 released SDK 的大写规范名；未知值或小写值可能
回退到 ``ROBOT``。强类型 device enum 仍需要协调 SDK 和 ROS 接口发布。

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
