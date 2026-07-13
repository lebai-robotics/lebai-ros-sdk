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

启动 MoveIt
-----------

两个公开 launch 默认把驱动、MoveIt、RViz、robot_state_publisher 和静态 TF
节点放在 ``lebai`` 命名空间中，也就是使用 ``namespace:=lebai``。因此默认的
MoveIt 相对 action ``move_action`` 解析为 ``/lebai/move_action``。驱动也注册
两个相对 action
``lebai_trajectory_controller/follow_joint_trajectory`` 和
``lebai_gripper_controller/gripper_cmd``，默认分别解析为
``/lebai/lebai_trajectory_controller/follow_joint_trajectory`` 和
``/lebai/lebai_gripper_controller/gripper_cmd``。

机械臂状态、MoveIt controller 配置和 ``FollowJointTrajectory`` action 使用
固定关节名 ``joint_1`` 到 ``joint_6``；这些名称不能通过 launch 参数重映射。

连接仿真控制器时，将 ``robot_ip`` 指向仿真控制器所在主机。下面示例使用本机
``127.0.0.1``：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     robot_ip:=127.0.0.1 \
     simulator:=true

连接真实控制器时，从终端读取实际控制器 IP，并省略 ``simulator:=true``：

.. code-block:: bash

   read -r -p "Controller IP: " ROBOT_IP
   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     robot_ip:="$ROBOT_IP"

启动 LM3-L1 MoveIt：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3_l1.launch.py \
     robot_ip:=127.0.0.1 \
     simulator:=true

需要启动另一套命名空间时，显式传入 ``namespace``。例如：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     namespace:=robot_1 \
     robot_ip:=127.0.0.1 \
     simulator:=true

此时对应的 action 为 ``/robot_1/move_action``、
``/robot_1/lebai_trajectory_controller/follow_joint_trajectory`` 和
``/robot_1/lebai_gripper_controller/gripper_cmd``。MoveIt 教程脚本同样接受
``--namespace robot_1``；它们的 action 名称默认保持相对形式，会解析到所选
命名空间。

默认会加载带 gripper 的配置。只使用机械臂本体时，设置
``has_gripper:=false``：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     robot_ip:=127.0.0.1 \
     simulator:=true \
     has_gripper:=false

RViz 中的操作
-------------

启动后，在 RViz 的 MotionPlanning 面板中选择 planning group：

- ``manipulator``：拖动末端交互 marker，点击 ``Plan`` 做机械臂规划，点击
  ``Execute`` 执行轨迹。执行前需要先启动机械臂。
- ``gripper``：选择 ``open`` 或 ``closed`` 命名状态，再执行 gripper action。

点击 ``Execute`` 后，MoveIt 会通过驱动执行机械臂轨迹或 claw 开合命令。

检查连接
--------

启动后可以检查 joint states、MoveIt 控制 action 和 TF：

.. code-block:: bash

   ros2 topic echo /lebai/status/joint_states --once
   ros2 topic echo /lebai/model/joint_states --once
   ros2 action info /lebai/move_action
   ros2 action info /lebai/lebai_trajectory_controller/follow_joint_trajectory
   ros2 action info /lebai/lebai_gripper_controller/gripper_cmd
   ros2 topic echo /tf --once

``ros2 action info`` 应该显示 MoveIt action client 和驱动 action server 都存在。
如果只有 client、没有 server，通常说明 ``lebai_driver`` 没有正常启动或工作空间
没有重新构建并 source。

这些 launch 仅保证其配置的驱动和 MoveIt 自有 node、topic、service 和 action
接口使用所选命名空间；不承诺 legacy RViz 工具 topic 或第三方接口也随之隔离。
TF 仍使用 ROS 2 标准的全局 ``/tf`` 和 ``/tf_static`` 传输。这里不承诺 TF
frame ID 隔离，同时启动多套具有相同 ``world``、``base_link`` 等 frame ID 的
模型时，需要由系统集成方另行规划 frame 命名。
