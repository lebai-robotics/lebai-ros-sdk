旧版本用户迁移
==============

如果你使用过旧版 ``lebai-ros-sdk``，升级后主要需要修改启动命令、topic 名称、
service 名称和接口类型。

启动方式
--------

使用新的主驱动 launch：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_ip:=192.168.1.100

旧的分散 launch 文件不再作为推荐入口使用。状态、运动、IO 和 claw 服务都由
主驱动节点提供。

命名空间
--------

默认命名空间是 ``/lebai``。如果你以前在代码里写死了旧 topic 或 service
路径，需要改成新的路径：

.. code-block:: text

   /lebai/<category>/<name>

例如：

.. code-block:: text

   /lebai/status/robot
   /lebai/motion/movej
   /lebai/io/set_do
   /lebai/claw/set_claw

常用名称替换
------------

.. list-table::
   :header-rows: 1

   * - 旧概念
     - 新用法
   * - ``system_service``
     - 使用 ``/lebai/start_stop/...`` 服务。
   * - ``robot_state``
     - 订阅 ``/lebai/status/...`` topic。
   * - ``io_service``
     - 使用 ``/lebai/io/...`` 和 ``/lebai/claw/...`` 服务。
   * - 旧 gripper 包
     - 使用 ``serial_gripper.launch.py`` 和 ``/lebai/gripper/...`` 服务。

运动接口
--------

Phase 1 使用 service 调用运动接口。典型调用：

.. code-block:: bash

   ros2 service call /lebai/motion/movej lebai_interfaces/srv/MoveJoint "{
     target: {
       is_joint_pose: true,
       joint_positions: [0.0, -0.5, 0.5, 0.0, 0.5, 0.0]
     },
     params: {
       acceleration: 0.5,
       velocity: 0.5,
       time: 0.0,
       blend_radius: 0.0
     }
   }"

如果你的旧程序使用 action client，需要先改成 service client。

笛卡尔数据
----------

SDK 风格的笛卡尔数据使用 ``lebai_interfaces/msg/CartesianPose``：

.. code-block:: text

   x
   y
   z
   rx
   ry
   rz

不要在新的运动 service 中直接传 ``geometry_msgs/Pose``。

模型和 TF
---------

启动驱动后默认发布机器人模型和 TF：

.. code-block:: bash

   ros2 topic echo /lebai/model/joint_states
   ros2 topic echo /tf

如果旧工程单独启动 ``robot_state_publisher``，请确认不要重复发布相同模型。
