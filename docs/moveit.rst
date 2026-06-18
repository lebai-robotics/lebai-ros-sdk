MoveIt
======

本页说明如何启动 LM3/LM3-L1 的 MoveIt 配置，并通过 RViz 做规划和执行。

准备工作
--------

先在工作空间根目录构建源码包：

.. code-block:: bash

   cd ~/lebai/lebai_ws
   source /opt/ros/humble/setup.bash
   colcon build --symlink-install
   source install/setup.bash

启动 LM3 MoveIt
---------------

连接仿真控制器时，将 ``robot_ip`` 指向仿真控制器所在主机。下面示例使用本机
``127.0.0.1``：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     robot_ip:=127.0.0.1 \
     simulator:=true

连接真实控制器时，将 ``robot_ip`` 改成控制器 IP，并省略
``simulator:=true``：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     robot_ip:=192.168.1.100

启动 LM3-L1 MoveIt：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3_l1.launch.py \
     robot_ip:=127.0.0.1 \
     simulator:=true

默认会加载带 gripper 的模型和 MoveIt 语义配置。只使用机械臂本体时，设置
``has_gripper:=false``：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     robot_ip:=127.0.0.1 \
     simulator:=true \
     has_gripper:=false

launch 会启动：

- ``lebai_driver``，并关闭驱动内部的 ``robot_state_publisher``。
- ``robot_state_publisher``，使用 MoveIt 选择的机器人模型。
- ``move_group``。
- RViz，加载 ``lebai_lm3_moveit_config/launch/moveit.rviz``。
- ``world`` 到 ``base_link`` 的静态 TF。

gripper 模式
------------

``has_gripper`` 控制机器人模型、SRDF 和 joint states 来源：

.. list-table::
   :header-rows: 1

   * - ``has_gripper``
     - 模型
     - joint states
     - MoveIt group
   * - ``true``
     - ``lm3_with_gripper.xacro`` 或 ``lm3_l1_with_gripper.xacro``
     - ``/lebai/model/joint_states``
     - ``manipulator`` 和 ``gripper``
   * - ``false``
     - ``lm3.xacro`` 或 ``lm3_l1.xacro``
     - ``/lebai/status/joint_states``
     - ``manipulator``

带 gripper 时，MoveIt 只控制主动关节 ``gripper_r_joint1``。URDF 中其它 gripper
关节是 mimic 关节。gripper 命名状态为：

.. list-table::
   :header-rows: 1

   * - 状态
     - ``gripper_r_joint1``
     - claw 幅度
   * - ``open``
     - ``1.0471975512``
     - ``100``
   * - ``closed``
     - ``0.0``
     - ``0``

RViz 中的操作
-------------

启动后，在 RViz 的 MotionPlanning 面板中选择 planning group：

- ``manipulator``：拖动末端交互 marker，点击 ``Plan`` 做机械臂规划，点击
  ``Execute`` 执行轨迹。
- ``gripper``：选择 ``open`` 或 ``closed`` 命名状态，或设置
  ``gripper_r_joint1`` 目标角度，再执行 gripper action。

机械臂执行使用 MoveIt Simple Controller Manager 连接
``/lebai_trajectory_controller``。驱动会把轨迹点转换为
``pylebai.move_pvat(positions, velocities, accelerations, duration)`` 调用，并等待
控制器回到非运动状态。

gripper 执行使用 ``/lebai_gripper_controller/gripper_cmd``。驱动将
``gripper_r_joint1`` 映射为 claw 幅度：

.. code-block:: text

   amplitude = position / (pi / 3) * 100

然后调用 ``pylebai.set_claw(force, amplitude)``。

检查连接
--------

启动后可以检查 joint states、MoveIt 控制 action 和 TF：

.. code-block:: bash

   ros2 topic echo /lebai/status/joint_states --once
   ros2 topic echo /lebai/model/joint_states --once
   ros2 action info /lebai_trajectory_controller
   ros2 action info /lebai_gripper_controller/gripper_cmd
   ros2 topic echo /tf --once

``ros2 action info`` 应该显示 MoveIt action client 和驱动 action server 都存在。
如果只有 client、没有 server，通常说明 ``lebai_driver`` 没有正常启动或工作空间
没有重新构建并 source。

常见问题
--------

``robot_interface.launch.py`` 找不到
   旧构建缓存可能仍引用已经删除的 launch 文件。清理相关包的 build/install 后重新
   构建，或重新构建整个工作空间。

``LoadResourceList`` 等接口导入失败
   工作空间中安装的 ``lebai_interfaces`` 不是当前源码版本。重新构建
   ``lebai_interfaces`` 和 ``lebai_driver``，然后重新 ``source install/setup.bash``。

规划开始状态碰撞
   如果使用 ``has_gripper:=true``，确认当前安装的是包含 gripper SRDF 碰撞忽略配置
   的版本。gripper 内部碰撞应由 SRDF 忽略。

执行时报 ``start point deviates from current robot state``
   MoveIt 规划的起点和控制器当前关节状态差异超过
   ``trajectory_execution.allowed_start_tolerance``。等上一段轨迹完全结束后再规划，
   或在 RViz 中先同步当前状态后重新规划。
