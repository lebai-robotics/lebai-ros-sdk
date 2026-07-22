快速开始
========

启动仿真控制器
--------------

如果本机已有 Lebai 控制器仿真程序，并监听 ``127.0.0.1``，可以直接启动驱动：

.. code-block:: bash

   source /opt/ros/humble/setup.bash
   source install/setup.bash
   ros2 launch lebai_driver driver.launch.py robot_ip:=127.0.0.1 simulator:=true

启动真实控制器
--------------

从终端读取实际控制器 IP，再启动驱动：

.. code-block:: bash

   read -r -p "Controller IP: " ROBOT_IP
   ros2 launch lebai_driver driver.launch.py robot_ip:="$ROBOT_IP"

默认命名空间是 ``/lebai``。如果需要修改命名空间：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py \
     robot_ip:="$ROBOT_IP" \
     namespace:=my_robot

查看机器人状态
--------------

.. code-block:: bash

   ros2 topic echo /lebai/status/robot
   ros2 topic echo /lebai/status/joint_states
   ros2 topic echo /lebai/status/joint_motion

机械臂状态和 ``FollowJointTrajectory`` action 固定使用 ``joint_1`` 到
``joint_6``，不支持运行时重映射。两个驱动 action 使用相对名称，在默认
命名空间下可以这样检查：

.. code-block:: bash

   ros2 action info /lebai/lebai_trajectory_controller/follow_joint_trajectory
   ros2 action info /lebai/lebai_gripper_controller/gripper_cmd

修改 ``namespace`` 后，这两个路径的 ``/lebai`` 前缀也相应改变。

查看模型关节状态和 TF
---------------------

驱动默认启动 ``robot_state_publisher``，并使用 ``lm3_with_gripper.xacro``。

.. code-block:: bash

   ros2 topic echo /lebai/model/joint_states
   ros2 topic echo /tf

仅启动 ``lebai_driver`` 时，可以在 RViz 中查看实时模型：

.. code-block:: bash

   source /opt/ros/humble/setup.bash
   source install/setup.bash
   rviz2 \
     -d "$(ros2 pkg prefix lebai_lm3_support)/share/lebai_lm3_support/rviz/view.rviz" \
     --ros-args -r __ns:=/lebai

该 RViz 配置的 ``RobotModel`` display 使用相对名称
``robot_description``。上面的 ``__ns:=/lebai`` 让它解析为驱动发布的
``/lebai/robot_description``，并通过全局 ``/tf`` 显示实时姿态。使用其他
驱动命名空间时，应把 RViz 的 ``__ns`` 设为相同值。MoveIt 规划和执行请使用
``lebai_lm3_moveit_config`` 的启动文件和 RViz ``MotionPlanning`` 面板。

如果只想启动驱动，不发布机器人模型：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py publish_robot_description:=false

如果要切换机器人模型：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_model:=lm3.xacro

常用模型文件：

.. code-block:: text

   lm3.xacro
   lm3_l1.xacro
   lm3_with_gripper.xacro
   lm3_l1_with_gripper.xacro

只显示模型
----------

如果只想检查 URDF、TF 和 RViz 显示效果，不连接控制器，可以使用
``lebai_lm3_support`` 中的 display launch。

显示 LM3：

.. code-block:: bash

   ros2 launch lebai_lm3_support display_lm3.launch.py

显示独立 gripper：

.. code-block:: bash

   ros2 launch lebai_lm3_support display_gripper.launch

调用启停服务
------------

.. code-block:: bash

   ros2 service call /lebai/start_stop/start_sys lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/stop_sys lebai_interfaces/srv/Command

控制内置 claw
-------------

设置 claw 开合幅度和力：

.. code-block:: bash

   ros2 service call /lebai/claw/set_claw lebai_interfaces/srv/SetClaw "{amplitude: 40.0, force: 50.0}"

读取 claw 状态：

.. code-block:: bash

   ros2 service call /lebai/claw/get_claw lebai_interfaces/srv/GetClaw
   ros2 topic echo /lebai/claw/state
   ros2 topic echo /lebai/claw/joint_states

控制 IO
-------

设置数字输出：

.. code-block:: bash

   ros2 service call /lebai/io/set_do lebai_interfaces/srv/SetDigitalOutput "{device: ROBOT, pin: 0, value: true}"

读取数字输入：

.. code-block:: bash

   ros2 service call /lebai/io/get_di lebai_interfaces/srv/GetDigitalInput "{device: ROBOT, pin: 0}"

IO device 当前仍是字符串。请使用大写规范名，例如 ``ROBOT``、``FLANGE``；
未知值或小写值可能由 released SDK 回退到 ``ROBOT``。

启动控制器发现
--------------

.. code-block:: bash

   ros2 launch lebai_driver discovery.launch.py
   ros2 service call /lebai/discovery/resolve lebai_interfaces/srv/ResolveControllers

启动独立 gripper
----------------

连接串口 gripper 后启动节点：

.. code-block:: bash

   ros2 launch lebai_driver serial_gripper.launch.py port_name:=/dev/ttyUSB0

设置 gripper 位置、力和速度：

.. code-block:: bash

   ros2 service call /lebai/gripper/set_position lebai_interfaces/srv/SetGripperPosition "{position: 50}"
   ros2 service call /lebai/gripper/set_force lebai_interfaces/srv/SetGripperForce "{force: 50}"
   ros2 service call /lebai/gripper/set_velocity lebai_interfaces/srv/SetGripperVelocity "{velocity: 50, persistent: false}"

查看 gripper 状态：

.. code-block:: bash

   ros2 topic echo /lebai/gripper/state

运行示例
--------

基础驱动和 MoveIt 示例见 :doc:`examples`。
