示例
====

``lebai_tutorials`` 提供可以直接运行的 Python 示例。运行前先构建工作空间：

.. code-block:: bash

   cd ~/lebai/lebai_ws
   source /opt/ros/humble/setup.bash
   colcon build --symlink-install
   source install/setup.bash

基础驱动示例
------------

基础示例需要先启动 ``lebai_driver``：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_ip:=127.0.0.1 simulator:=true

运行关节运动和直线运动示例：

.. code-block:: bash

   ros2 run lebai_tutorials move_example.py

运行 IO 示例：

.. code-block:: bash

   ros2 run lebai_tutorials io_example.py

订阅关节状态：

.. code-block:: bash

   ros2 run lebai_tutorials joint_state_subscriber.py

MoveIt 示例准备
---------------

MoveIt 示例需要先启动 MoveIt 配置。使用 gripper 示例时必须启用 gripper：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     robot_ip:=127.0.0.1 \
     simulator:=true \
     has_gripper:=true

连接真实控制器时，将 ``robot_ip`` 改成控制器 IP，并省略 ``simulator:=true``。

机械臂 MoveIt 示例
------------------

``moveit_manipulator_example.py`` 通过 MoveIt 的 ``manipulator`` group 发送
关节空间目标。默认会规划并执行轨迹：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_manipulator_example.py

只规划、不执行：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_manipulator_example.py --plan-only

指定 6 个关节目标，单位为弧度：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_manipulator_example.py \
     --joints="-0.35,-1.0,1.2,-1.1,-0.6,0.0"

gripper MoveIt 示例
-------------------

``moveit_gripper_amplitude_example.py`` 使用 MoveIt gripper 控制器 action，并用
claw 幅度百分比设置 gripper。幅度范围是 ``0`` 到 ``100``：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_gripper_amplitude_example.py --amplitude 50

幅度会映射到 gripper 主动关节 ``gripper_r_joint1``：

.. code-block:: text

   gripper_r_joint1 = amplitude / 100 * pi / 3

因此 ``--amplitude 0`` 对应关闭，``--amplitude 100`` 对应打开。
