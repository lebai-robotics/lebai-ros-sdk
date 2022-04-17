.. _noetic_interface:


``ROS`` 接口说明
========================================

.. contents:: Table of Contents
   :depth: 2
   :local:


Node
~~~~~~~~~~~~~~~~~

 * ``io_service`` ``IO`` 服务。
 * ``trajectory_action_server`` 关节轨迹运动 ``Action Server`` ，用来向机械臂发送轨迹。
 * ``motion_service`` 运动指令服务， ``movel`` 、 ``movej`` 等。
 * ``system_service`` 系统服务，例如上下使能，进入、退出视角模式等。
 * ``robot_state`` 获取机械臂的各种状态并发布。

Published Topics
~~~~~~~~~~~~~~~~~
* **/joint_states** (``sensor_msgs/msg/JointState``)

  发布机械臂的关节数据信息（位置、速度等）。

* **/gripper_status** (``lebai_interfaces/msg/GripperStatus``)

  发布机械臂夹爪数据。

* **/io_status** (``lebai_interfaces/msg/IOStatus``)

  发布机械臂 ``IO`` 数据。

Services
~~~~~~~~~~
* **/system_service/enable** (``std_srvs/srv/Empty``)

  机械臂上使能。

  脚本示例::

    ros2 service call /system_service/enable std_srvs/srv/Empty "{}"

* **/system_service/disable** (``std_srvs/srv/Empty``)

  机械臂下使能。

  脚本示例::

    ros2 service call /system_service/disable std_srvs/srv/Empty "{}"

* **/system_service/power_on** (``std_srvs/srv/Empty``)

  机械臂上电（目前等同于机械臂上使能）。

  脚本示例::

    ros2 service call /system_service/power_on std_srvs/srv/Empty "{}"

* **/system_service/power_off** (``std_srvs/srv/Empty``)

  机械臂上电（目前等同于机械臂下使能）。

  脚本示例::

    ros2 service call /system_service/power_off std_srvs/srv/Empty "{}"

* **/system_service/emergency_stop** (``std_srvs/srv/Empty``)

  机械臂急停。

  脚本示例::

    ros2 service call /system_service/emergency_stop std_srvs/srv/Empty "{}"

* **/system_service/turn_off_robot** (``std_srvs/srv/Empty``)

  机械臂关机。

  脚本示例::

    ros2 service call /system_service/turn_off_robot std_srvs/srv/Empty "{}"

* **/system_service/entry_teach_mode** (``std_srvs/srv/Empty``)

  机械臂进入拖动示教模式。

  脚本示例::

    ros2 service call /system_service/entry_teach_mode std_srvs/srv/Empty "{}"

* **/system_service/exit_teach_mode** (``std_srvs/srv/Empty``)

  机械臂退出拖动示教模式。

  脚本示例::

    ros2 service call /system_service/exit_teach_mode std_srvs/srv/Empty "{}"

* **/system_service/abort_motion** (``std_srvs/srv/Empty``)

  机械臂停止正在执行的运动。

  脚本示例::

    ros2 service call /system_service/abort_motion std_srvs/srv/Empty "{}"

* **/system_service/pause_motion** (``std_srvs/srv/Empty``)

  机械臂暂停正在执行的运动。

  脚本示例::

    ros2 service call /system_service/pause_motion std_srvs/srv/Empty "{}"

* **/system_service/resume_motion** (``std_srvs/srv/Empty``)

  机械臂恢复暂停的运动。

  脚本示例::

    ros2 service call /system_service/resume_motion std_srvs/srv/Empty "{}"

* **motion_service/move_joint** (``lebai_interfaces/srv/MoveJoint``)

  机械臂关节移动。
  
  该服务仅向机械臂控制器发送移动请求，机械臂缓存该移动请求，该服务返回并不代表机械臂移动到终点位置。

  脚本示例::

    ros2 service call /motion_service/move_joint lebai_interfaces/srv/MoveJoint "{is_joint_pose: 1, joint_pose: [3.1,-1.57,-2.2,-1.03,1.67,1.62], common: {vel: 0.5, acc: 1.0, time: 0.0, radius: 0.0}}"

* **motion_service/move_line** (``lebai_msgs/SetAO``)

  机械臂直线移动。该服务仅向机械臂控制器发送移动请求，机械臂缓存该移动请求，该服务返回并不代表机械臂移动到终点位置。

  脚本示例::

    ros2 service call /motion_service/move_line lebai_interfaces/srv/MoveLine "{is_joint_pose: 0, cartesian_pose: {position: {x: -0.3,y: 0.125,z: 0.4077}, orientation: {x: 0.99669, y: -0.047447,z: 0.043886, w: 0.049333}}, common: {vel: 0.2, acc: 1.0, time: 0.0, radius: 0.0}}"

* **/io_service/set_robot_do** (``lebai_interfaces/srv/SetDO``)

  设置控制柜模拟量量输出。

  脚本示例::

    ros2 service call /io_service/set_robot_do lebai_interfaces/srv/SetDO "{pin: 0, value: true}"

* **/io_service/set_flange_do** (``lebai_interfaces/srv/SetDO``)

  设置法兰数字量输出。

  脚本示例::

    ros2 service call /io_service/set_flange_do lebai_interfaces/srv/SetDO "{pin: 0, value: true}"

* **io_service/set_extend_do** (``lebai_interfaces/srv/SetDO``)

  设置扩展数字量输出。

  脚本示例::

    ros2 service call /io_service/set_extend_do lebai_interfaces/srv/SetDO "{pin: 0, value: true}"

* **/io_service/set_robot_ao** (``lebai_interfaces/srv/SetAO``)

  设置控制柜模拟量输出。

  脚本示例::

    ros2 service call /io_service/set_robot_ao lebai_interfaces/srv/SetAO "{pin: 0, value: 2.0}"

* **/io_service/set_ext_ao** (``lebai_interfaces/srv/SetAO``)

  设置扩展模拟量输出。

  脚本示例::

    ros2 service call /io_service/set_ext_ao lebai_interfaces/srv/SetAO "{pin: 0, value: 2.0}"

* **/io_service/set_robot_ao_mode** (``lebai_interfaces/srv/SetAMode``)

  设置控制柜模拟量输出模式。

  脚本示例::

    ros2 service call /io_service/set_robot_ao_mode lebai_interfaces/srv/SetAMode "{pin: 0, mode: 1}"

* **/io_service/set_robot_ai_mode** (``lebai_interfaces/srv/SetAMode``)

  设置控制柜模拟量输入模式。

  脚本示例::

    ros2 service call /io_service/set_robot_ai_mode lebai_interfaces/srv/SetAMode "{pin: 0, mode: 1}"

* **/io_service/set_gripper_force** (``lebai_interfaces/srv/SetGripper``)

  设置夹爪力。

  脚本示例::

    ros2 service call /io_service/set_gripper_force lebai_interfaces/srv/SetGripper "{val: 0.3}"

* **/io_service/set_gripper_position** (``lebai_interfaces/srv/SetGripper``)

  设置夹爪位置。

  脚本示例::

    ros2 service call /io_service/set_gripper_position lebai_interfaces/srv/SetGripper "{val: 0.3}"
