.. _noetic_execution:

运行
============

.. contents:: 目录
   :depth: 2
   :local:

现在您可以开始尝试通过 ``lebai-ros-sdk`` 连接一台乐白机械臂。

.. note::

  请先确保乐白机械臂正常工作并确保机械臂和您的 ``ROS`` 运行系统的网络连接。

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
  
  roslaunch lebai_lm3_moveit_config real_robot.launch robot_ip:=xxx.xxx.xxx.xxx

.. note::
  在使用 ``MoveIt`` 控制机械臂之前，请确保机械臂处于启动状态。

* ``robot_ip`` 是乐白机械臂的 ``IP`` 地址。

目前， ``MoveIt`` 只能用来控制机械臂的关节运动，不能控制夹爪运动。

修正匹配 ``DH`` 参数
----------------------

每一台机械臂出厂之前的 ``DH`` 参数都经过校准，而 ``ROS`` 程序中使用的数据来自于固定的 ``urdf`` 模型文件。
因此，您可能会遇到机械臂 ``web`` 人机交互界面的坐标点位和 ``ROS`` 系统中的坐标点位不一致，存在一些偏差（通常不会很大）的问题。

为了解决该问题，您需要手动修正 ``ROS`` 端 ``urdf`` 文件中的相关配置，使其和实际机械臂的内部参数设置吻合。

由于目前 ``web`` 界面无法直接查看机械臂的实际 ``DH`` 参数，``lebai-ros-sdk`` 也没有提供相关的接口，您可以通过如下方式获取控制器内部设定的参数：

创建文件 ``get_lebai_dh_param.py``，写入如下内容，注意使用实际连接的机械臂 ``IP`` 地址。

.. code-block:: python3

  import lebai
  
  robot = lebai.LebaiRobot('xxx.xxx.xxx.xxx')
  dh = [list(x.__dict__.values()) for x in robot.get_dh_params()]
  for data in dh:
    print(', '.join(f'{d:.6f}' for d in data))

运行该文件

.. code-block:: bash

  python3 get_lebai_dh_param.py

您会获得类似如下的结果:

.. code-block:: bash

  0.000000, 0.000000, 0.000000, 0.000000
  0.213658, 0.000000, 0.000000, 0.000000
  0.000000, 0.000000, 1.570800, 0.000000
  0.000000, -0.280268, 0.000000, 0.000000
  0.120732, -0.258787, 0.000000, 0.000000
  0.097480, 0.000000, 1.570800, 0.000000
  0.084991, 0.000000, -1.570800, 0.000000
  0.000000, 0.000000, 0.000000, 0.000000

在 ``lebai-ros-sdk`` 源代码的 ``lebai_lm3_support/urdf/lm3_macro.xacro`` 文件中找到：

.. code-block:: xml

  <!-- Robot DH parameters define joint-->
  <xacro:property name="d1" value="0.21583" />
  <xacro:property name="d4" value="0.12063" />
  <xacro:property name="d5" value="0.09833" />
  <xacro:property name="d6" value="0.08343" />
  <xacro:property name="a2" value="-0.28" />
  <xacro:property name="a3" value="-0.26"/>

相关部分，上述几个数据与上述的 ``get_lebai_dh_param.py`` 程序的输出结果关系为：

.. code-block:: bash

  xx, xx, xx, xx
  d1, xx, xx, xx
  xx, xx, xx, xx
  xx, a2, xx, xx
  d4, a3, xx, xx
  d5, xx, xx, xx
  d6, xx, xx, xx
  xx, xx, xx, xx

按照对应关系，修改 ``lm3_macro.xacro`` 文件中的 ``d1`` , ``d4`` , ``d5`` , ``d6`` , ``a2`` , ``a3`` 值。

完成修改后，您需要重新编译安装 ``lebia-ros-sdk``。

.. code-block:: bash

  cd ~/lebai_ws
  catkin_make install

您可以再次运行 ``lebai-ros-sdk`` 的程序，现在坐标位置应该完全一致。

