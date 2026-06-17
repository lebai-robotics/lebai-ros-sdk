节点和参数
==========

驱动节点
--------

主驱动节点通过 ``driver.launch.py`` 启动：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_ip:=127.0.0.1 simulator:=true

该节点提供机器人状态 topic、机器人控制 service，以及给 MoveIt 使用的机械臂
轨迹 action。

MoveIt 轨迹执行
----------------

主驱动节点提供 ``/lebai_trajectory_controller``：

.. code-block:: text

   control_msgs/action/FollowJointTrajectory

MoveIt 配置中的 ``lebai_trajectory_controller`` 会连接到该 action。驱动会校验
轨迹关节名和 ``joint_names`` 参数一致，然后把相邻 trajectory point 转换为
``pylebai.move_pvat(positions, velocities, accelerations, duration)`` 调用。
该 action 当前只覆盖机械臂关节；gripper 轨迹执行仍是后续工作。

常用参数
--------

.. list-table::
   :header-rows: 1

   * - 参数
     - 默认值
     - 用途
   * - ``robot_ip``
     - ``127.0.0.1``
     - 控制器 IP。
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
   * - ``joint_names``
     - ``['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']``
     - 发布到 ``/lebai/model/joint_states`` 的机械臂关节名；必须和 URDF 关节名一致，RViz/TF 才能显示完整模型。
   * - ``gripper_joint_name``
     - ``gripper_r_joint1``
     - claw 幅度映射到模型时使用的 gripper 关节名。

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
     io_state_device:=robot \
     io_state_digital_input_count:=8 \
     io_state_digital_output_count:=8 \
     io_state_analog_input_count:=2 \
     io_state_analog_output_count:=2 \
     io_state_dio_count:=0

机器人模型和 TF
---------------

默认启动时会同时启动 ``robot_state_publisher``。它订阅
``/lebai/model/joint_states``，并发布 ``/tf`` 和 ``/tf_static``。

可用模型文件：

.. code-block:: text

   lm3.xacro
   lm3_l1.xacro
   lm3_with_gripper.xacro
   lm3_l1_with_gripper.xacro

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
