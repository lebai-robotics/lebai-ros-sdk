MoveIt
======

本页介绍如何用 MoveIt 1 和 RViz 操作 LM3。先按 :doc:`install` 构建并加载
Catkin 工作空间环境。

启动 MoveIt
-----------

选择与你的 LM3 对应的模式，将 ``192.168.1.104`` 换成控制器的实际 IP。

**带夹爪的 LM3（默认）**

.. code-block:: bash

   roslaunch lebai_lm3_moveit_config lm3.launch has_gripper:=true robot_ip:=192.168.1.104

**仅机械臂**

.. code-block:: bash

   roslaunch lebai_lm3_moveit_config lm3.launch has_gripper:=false robot_ip:=192.168.1.104

以上命令会启动驱动和 RViz。连接本机仿真时，使用
``robot_ip:=127.0.0.1 simulator:=true``。在无界面环境中运行时，加上
``use_rviz:=false``。

RViz 中的操作
-------------

1. 在 RViz 的 ``MotionPlanning`` 面板选择 ``manipulator`` 规划组，设置目标姿态。
2. 点击 ``Plan``，检查规划出的轨迹。
3. 准备执行后，按 :doc:`quickstart` 调用 ``/lebai/start_stop/start_sys``，
   再点击 ``Execute``。

带夹爪模式可选择 ``gripper`` 规划组，用 ``open`` 或 ``closed`` 作为目标，
再规划并执行。

分开启动驱动和 MoveIt
---------------------

在两个终端分别运行下方命令。示例使用仅机械臂模式，带夹爪时将第二条命令的
``has_gripper`` 设为 ``true``。

.. code-block:: bash

   roslaunch lebai_driver driver.launch robot_ip:=192.168.1.104 publish_robot_description:=false
   roslaunch lebai_lm3_moveit_config lm3.launch has_gripper:=false launch_driver:=false

检查连接
--------

如果 RViz 中模型没有更新，先在另一个终端查看机械臂关节状态。

.. code-block:: bash

   rostopic echo -n 1 /lebai/status/joint_states

带夹爪模式的组合关节查询见 :doc:`interfaces/topics`。Python 用法见 :doc:`examples`。
