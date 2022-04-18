.. _melodic_execution:

运行
============

.. contents:: 目录
   :depth: 2
   :local:

现在您可以开始尝试通过 ``lebai-ros-sdk`` 连接一台乐白机械臂。

.. note::

  请先确保乐白机械臂正常工作并确保机械臂和您的 ``ROS`` 运行系统的网络连接。

在运行程序前，确保您已经正确的编译 ``lebai-ros-sdk``，并且设置了工作空间。

.. code-block:: bash

  # remember to run the source  
  source ~/lebai_ws/install/setup.bash

基本驱动程序
----------------------

按照如下方式启动基本的驱动程序：

.. tabs::
  
  .. group-tab:: 无界面

    .. code-block:: bash

      roslaunch lebai_lm3_support robot_interface_lm3.launch robot_ip:=xxx.xxx.xxx.xxx has_gripper:=0

    * ``robot_ip`` 是乐白机械臂的 ``IP`` 地址。
    * ``has_gripper`` 是机械臂末端是否有乐白夹爪。有夹爪设置为 ``1``，没有夹爪设置为 ``0``。


  .. group-tab:: 有界面

    .. code-block:: bash

      roslaunch lebai_lm3_support robot_interface_lm3_with_visual.launch robot_ip:=xxx.xxx.xxx.xxx has_gripper:=0

    * ``robot_ip`` 是乐白机械臂的 ``IP`` 地址。
    * ``has_gripper`` 是机械臂末端是否有乐白夹爪。有夹爪设置为 ``1``，没有夹爪设置为 ``0``。

运行成功后，您可以打开另一个终端，并通过命令行查看。

.. code-block:: bash

  rosservice list
  rostopic list

``MoveIt`` 程序
----------------------

按照如下方式启动 `MoveIt <https://moveit.ros.org/>`_ 驱动程序：

.. code-block:: bash
  
  roslaunch lebai_lm3_moveit_config run.launch sim:=false robot_ip:=xxx.xxx.xxx.xxx
  
  * ``sim`` 是否虚拟模式，当设置为虚拟模式时，不连接真实机械臂。
  * ``robot_ip`` 是乐白机械臂的 ``IP`` 地址。

.. note::
  在使用 ``MoveIt`` 控制机械臂之前，请确保机械臂处于启动状态。

* ``robot_ip`` 是乐白机械臂的 ``IP`` 地址。

目前， ``MoveIt`` 只能用来控制机械臂的关节运动，不能控制夹爪运动。

