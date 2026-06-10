支持范围
========

当前可用功能
------------

当前文档覆盖以下 ROS2 功能：

- 连接真实控制器。
- 连接本地仿真控制器。
- 启动、停止、急停、暂停和恢复运动。
- 调用 ``movej``、``movel``、``movec``、``speedj``、``speedl`` 和
  ``move_pvat``。
- 读取机器人状态、关节状态和运动状态。
- 读写数字 IO、模拟 IO 和 DIO 模式。
- 控制机器人内置 ``claw``。
- 控制独立串口 ``gripper``。
- 发现局域网中的控制器。
- 发布机器人模型和 TF。

当前支持环境
------------

.. list-table::
   :header-rows: 1

   * - ROS2 发行版
     - Ubuntu
     - 分支
     - 状态
   * - Lyrical
     - 26.04
     - ``lyrical-dev``
     - 当前文档对应环境

后续计划
--------

后续版本计划继续补充：

- motion action，用于更适合取消和反馈的长时间运动任务。
- MoveIt 配置和示例。
- 更多 SDK 分类接口，例如 ``config``、``file``、``modbus``、``serial``、
  ``storage``、``program``、``scene``、``robotics``、``led`` 和
  ``signal``。
- 后续 ROS2 发行版分支。

如果你只需要当前机器人控制、状态读取、IO、claw、discovery 和 gripper 功能，
可以直接使用当前接口。
