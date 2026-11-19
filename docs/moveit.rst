MoveIt
======

本页说明如何为 LM3 启动 MoveIt 1，并在 RViz 中规划和执行。

准备工作
--------

按 :doc:`install` 构建并加载 Catkin 工作空间环境。连接真实控制器时，将示例 IP
换成控制器的实际地址。

启动 MoveIt
-----------

根据机械臂是否安装夹爪选择启动模式。

.. code-block:: bash

   roslaunch lebai_lm3_moveit_config lm3.launch has_gripper:=true robot_ip:=192.168.1.104
   roslaunch lebai_lm3_moveit_config lm3.launch has_gripper:=false robot_ip:=192.168.1.104

默认设置为 ``has_gripper:=true``。启动时会加载机械臂和夹爪模型，配置
``manipulator`` 和 ``gripper`` 规划组，并通过过滤器将
``/lebai/model/joint_states`` 中完整的测量数据转发到
``/lebai_moveit/joint_states``。读取夹爪失败时，即使机械臂的实际位置不为零，
公开话题也可能发布七个零位置。此时消息的速度和力矩数组为空，MoveIt 不会用这些
消息更新实测状态。夹爪规划组控制 ``gripper_r_joint1``，其余关节按 URDF 中的
``mimic`` 定义随之运动。仅机械臂模式加载 ``manipulator`` 规划组，并订阅
``/lebai/status/joint_states``。

``lm3.launch`` 默认启动驱动和 RViz。由它启动驱动时，必须提供 ``robot_ip``。
在无界面环境运行时，设置 ``use_rviz:=false``。连接本机仿真控制器时，传入
``simulator:=true robot_ip:=127.0.0.1``。

要复用单独启动的驱动，请关闭该驱动的机器人状态发布器。分别在两个终端运行下方
命令。MoveIt 会根据 ``has_gripper`` 选择模型并发布 TF。

.. code-block:: bash

   roslaunch lebai_driver driver.launch robot_ip:=192.168.1.104 publish_robot_description:=false
   roslaunch lebai_lm3_moveit_config lm3.launch has_gripper:=false launch_driver:=false

默认的 MoveIt 配置使用驱动在 ``/lebai`` 下发布的关节状态话题和控制器 action
的绝对名称。如果在驱动端修改了 action 名称，请同步修改相应控制器的 ``name``
和 ``action_ns``，使拼接后的路径与驱动端一致。带夹爪模式修改
``lebai_lm3_moveit_config/config/controllers.yaml``，仅机械臂模式修改
``lebai_lm3_moveit_config/config/controllers_arm_only.yaml``。

RViz 中的操作
-------------

在 RViz 的 ``MotionPlanning`` 面板中选择 ``manipulator``，设置目标姿态后点击
``Plan``。确认规划轨迹后，按 :doc:`quickstart` 调用
``/lebai/start_stop/start_sys`` 使能机器人，再点击 ``Execute``。
带夹爪模式还可以选择 ``gripper`` 规划组。

检查连接
--------

查看驱动是否发布关节状态和轨迹控制器的 action 状态。

.. code-block:: bash

   rostopic echo -n 1 /lebai/status/joint_states
   rostopic info /lebai_trajectory_controller/status

带夹爪模式还可查看 ``/lebai/model/joint_states``。各话题的查询命令见
:doc:`interfaces/topics`，Python 示例见 :doc:`examples`。

直接调用控制器
--------------

默认 action 名称见 :ref:`node-launch-parameters`。

* 机械臂使用 ``control_msgs/FollowJointTrajectoryAction``。请求中的六个关节名
  必须与驱动配置的顺序一致，并至少提供两个轨迹点。每个轨迹点分别包含六个位置、
  速度和加速度值，``time_from_start`` 必须严格递增。第一个点的时间作为计算
  后续轨迹段时长的起点。
* 内置夹爪使用 ``control_msgs/GripperCommandAction``。关节目标位置从 0 到
  π/3 弧度，对应 0% 到 100% 的开合幅度。``max_effort`` 小于或等于 0 时，
  使用默认力值 100。

驱动可并行处理直接提交的 action 目标，取消轨迹会调用控制器的 ``stop_move``，
可能影响其他运动。请在客户端协调 action、MoveIt 和运动服务，确保同一时刻只有
一个来源发出机械臂运动指令。
