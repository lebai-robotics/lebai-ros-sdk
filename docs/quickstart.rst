快速开始
========

启动仿真控制器
--------------

如果本机已有 Lebai 控制器仿真程序，并监听 ``127.0.0.1``，可以直接启动驱动：

.. code-block:: bash

   source /opt/ros/jazzy/setup.bash
   source .venv/bin/activate
   source install/setup.bash
   ros2 launch lebai_driver driver.launch.py robot_ip:=127.0.0.1 simulator:=true

启动真实控制器
--------------

将 ``robot_ip`` 替换为机器人控制器 IP：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_ip:=192.168.1.100

默认命名空间是 ``/lebai``。如果需要修改命名空间：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_ip:=192.168.1.100 namespace:=my_robot

查看机器人状态
--------------

.. code-block:: bash

   ros2 topic echo /lebai/status/robot
   ros2 topic echo /lebai/status/joint_states
   ros2 topic echo /lebai/status/joint_motion

查看模型关节状态和 TF
---------------------

驱动默认启动 ``robot_state_publisher``，并使用 ``lm3_with_gripper.xacro``。

.. code-block:: bash

   ros2 topic echo /lebai/model/joint_states
   ros2 topic echo /tf

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

   ros2 service call /lebai/io/set_do lebai_interfaces/srv/SetDigitalOutput "{device: robot, pin: 0, value: true}"

读取数字输入：

.. code-block:: bash

   ros2 service call /lebai/io/get_di lebai_interfaces/srv/GetDigitalInput "{device: robot, pin: 0}"

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

.. code-block:: bash

   ros2 run lebai_tutorials move_example.py
   ros2 run lebai_tutorials io_example.py
   ros2 run lebai_tutorials joint_state_subscriber.py
