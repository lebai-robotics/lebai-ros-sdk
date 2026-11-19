.. _humble_execution:

运行
============

.. contents:: 目录
   :depth: 2
   :local:

现在您可以开始尝试通过 ``lebai-ros-sdk`` 连接一台乐白机械臂。

.. note::

  请先确保乐白机械臂正常工作并确保机械臂和您的 ``ROS 2`` 运行系统的网络连接。

如果您没有乐白机械臂硬件，也可以尝试通过容器（ ``Container`` ）来运行虚拟的乐白机械臂。
具体的方法您可以参考 `乐白机械臂Docker仿真 <https://help.lebai.ltd/dev/docker.html>`_ 。

.. note::

  记住，您运行 `乐白机械臂Docker仿真 <https://help.lebai.ltd/dev/docker.html>`_ 时需要设置容器的端口映射 ``-p 5181:5181`` 。

在运行程序前，确保您已经正确的编译 ``lebai-ros-sdk``，并且设置了工作空间。

.. code-block:: bash

  # remember to run the source
  source ~/lebai_ws/install/setup.bash

基本驱动程序
----------------------

按照如下方式启动基本的驱动程序：

    .. code-block:: bash

      ### For lm3
      ros2 launch lebai_lm3_support robot_interface_lm3.launch.py robot_ip:=xxx.xxx.xxx.xxx has_gripper:=false rviz2:=true
      ### For lm3-l1
      ros2 launch lebai_lm3_support robot_interface_lm3_l1.launch.py robot_ip:=xxx.xxx.xxx.xxx has_gripper:=false rviz2:=true

    * ``robot_ip`` 是乐白机械臂的 ``IP`` 地址。
    * ``has_gripper`` 是机械臂末端是否有乐白夹爪。有夹爪设置为 ``true``，没有夹爪设置为 ``false``。
    * ``rviz2`` 是否启动rviz2图形界面显示。

运行成功后，您可以打开另一个终端，并通过命令行查看。

.. code-block:: bash

  ros2 topic list
  ros2 service list

``MoveIt`` 程序
----------------------

按照如下方式启动 `MoveIt <https://moveit.ros.org/>`_ 驱动程序：

.. code-block:: bash

  # For lm3
  ros2 launch lebai_lm3_moveit_config lm3.launch.py robot_ip:=xxx.xxx.xxx.xxx
  # For lm3-l1
  ros2 launch lebai_lm3_moveit_config lm3_l1.launch.py robot_ip:=xxx.xxx.xxx.xxx

.. note::
  在使用 ``MoveIt`` 控制机械臂之前，请确保机械臂处于启动状态。

* ``robot_ip`` 是乐白机械臂的 ``IP`` 地址。

目前， ``MoveIt`` 只能用来控制机械臂的关节运动，不能控制夹爪运动。
