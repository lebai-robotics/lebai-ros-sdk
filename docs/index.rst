Lebai ROS2 SDK
==============

本项目提供 Lebai 机器人 ROS2 驱动。用户可以在 ROS2 中连接真实控制器或
本地仿真控制器，读取机器人状态，调用运动、IO、夹爪和发现服务，并在 RViz
中显示机器人模型与 TF。

你可以使用本驱动完成：

- 启动机器人驱动节点。
- 连接真实机器人控制器或本地仿真控制器。
- 读取机器人状态、关节状态、IO 状态、claw 状态和 gripper 状态。
- 调用 ``start_stop``、``motion``、``io``、``claw``、``discovery`` 和
  ``gripper`` 服务。
- 发布机器人模型和 TF，用于 RViz 显示。
- 发现局域网中的 Lebai 控制器。

.. toctree::
   :maxdepth: 2

   install
   quickstart
   moveit
   architecture
   interfaces/topics
   interfaces/services
