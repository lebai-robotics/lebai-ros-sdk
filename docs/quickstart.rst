快速开始
========

运行下列命令前，先按 :doc:`install` 构建并加载 Catkin 工作空间环境。

启动仿真控制器
--------------

连接已运行的仿真控制器时，设置 ``simulator:=true``，并填写仿真主机的可达地址。
下方示例使用本机仿真控制器。

.. code-block:: bash

   roslaunch lebai_driver driver.launch robot_ip:=127.0.0.1 simulator:=true

启动真实控制器
--------------

将 ``192.168.1.104`` 换成控制器的实际 IP 地址。

.. code-block:: bash

   roslaunch lebai_driver driver.launch robot_ip:=192.168.1.104

.. _driver-launch-parameters:

命名空间、关节名和其他启动选项见 :doc:`architecture`。

查看机器人状态
--------------

在另一个终端中查看连接状态和关节状态。

.. code-block:: bash

   rostopic echo -n 1 /lebai/status/robot
   rostopic echo -n 1 /lebai/status/joint_states

完整的话题和查询命令见 :doc:`interfaces/topics`。

查看模型关节状态和 TF
---------------------

驱动默认启动 ``robot_state_publisher``。可查看组合模型的关节状态和动态 TF。

.. code-block:: bash

   rostopic echo -n 1 /lebai/model/joint_states
   rostopic echo -n 1 /tf

调用启停服务
------------

准备好执行运动后，调用 ``start_sys`` 使能机器人，并检查 ``result.success``。

.. code-block:: bash

   rosservice call /lebai/start_stop/start_sys '{}'

停止、急停和其他系统服务见 :doc:`interfaces/services`。

启动控制器发现
--------------

发现节点可以独立于机器人驱动运行。

.. code-block:: bash

   roslaunch lebai_driver discovery.launch
   # 在另一个已加载工作空间环境的终端中执行
   rosservice call /lebai/discovery/resolve '{}'

启动串口夹爪
------------

启动串口夹爪节点时，将 ``port_name`` 设为所连接夹爪的设备路径。

.. code-block:: bash

   roslaunch lebai_driver serial_gripper.launch port_name:=/dev/ttyUSB0
   # 在另一个已加载工作空间环境的终端中执行
   rostopic echo -n 1 /lebai/gripper/state

串口夹爪节点提供独立的 ``gripper/*`` 接口。机器人驱动的 ``claw/*`` 接口用于
访问接入机器人控制器的内置夹爪。

运行示例
--------

Python 驱动示例见 :doc:`examples`。LM3 的规划和 RViz 操作见 :doc:`moveit`。
