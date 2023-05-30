.. _melodic_interface:


``ROS`` 接口说明
========================================

.. contents:: Table of Contents
   :depth: 2
   :local:


Node
~~~~~~~~~~~~~~~~~

 * ``io_service`` ``IO`` 服务。
 * ``joint_trajectory_action`` 关节轨迹运动 ``Action Server`` ，用来向机械臂发送轨迹。
 * ``motion_service`` 运动指令服务， ``movel`` 、 ``movej`` 等。
 * ``system_service`` 系统服务，例如上下使能，进入、退出视角模式等。
 * ``robot_state`` 获取机械臂的各种状态并发布。

Published Topics
~~~~~~~~~~~~~~~~~
* **/feedback_states** (``control_msgs/FollowJointTrajectoryFeedback``)

  发布 ``FollowJointTrajectoryAction`` 反馈信息。

* **/joint_states** (``sensor_msgs/msg/JointState``)

  发布机械臂的关节数据信息（位置、速度等）。

* **/gripper_status** (``lebai_msgs/GripperStatus``)

  发布机械臂夹爪数据。

* **/io_status** (``lebai_msgs/IOStatus``)

  发布机械臂 ``IO`` 数据。


Services
~~~~~~~~~~
* **/system_service/enable** (``std_srvs/Empty``)

  机械臂上使能。

  脚本示例::

    rosservice call /system_service/enable "{}"

* **/system_service/disable** (``std_srvs/Empty``)

  机械臂下使能。

  脚本示例::

    rosservice call /system_service/disable "{}"

* **/system_service/power_on** (``std_srvs/Empty``)

  机械臂上电（目前等同于机械臂上使能）。

  脚本示例::

    rosservice call /system_service/power_on "{}"

* **/system_service/power_off** (``std_srvs/Empty``)

  机械臂上电（目前等同于机械臂下使能）。

  脚本示例::

    rosservice call /system_service/power_off "{}"

* **/system_service/emergency_stop** (``std_srvs/Empty``)

  机械臂急停。

  脚本示例::

    rosservice call /system_service/emergency_stop "{}"

* **/system_service/turn_off_robot** (``std_srvs/Empty``)

  机械臂关机。

  脚本示例::

    rosservice call /system_service/turn_off_robot "{}"

* **/system_service/entry_teach_mode** (``std_srvs/Empty``)

  机械臂进入拖动示教模式。

  脚本示例::

    rosservice call /system_service/entry_teach_mode "{}"

* **/system_service/exit_teach_mode** (``std_srvs/Empty``)

  机械臂退出拖动示教模式。

  脚本示例::

    rosservice call /system_service/exit_teach_mode "{}"

* **/system_service/abort_motion** (``std_srvs/Empty``)

  机械臂停止正在执行的运动。

  脚本示例::

    rosservice call /system_service/abort_motion "{}"

* **/system_service/pause_motion** (``std_srvs/Empty``)

  机械臂暂停正在执行的运动。

  脚本示例::

    rosservice call /system_service/pause_motion "{}"

* **/system_service/resume_motion** (``std_srvs/Empty``)

  机械臂恢复暂停的运动。

  脚本示例::

    rosservice call /system_service/resume_motion "{}"

* **motion_service/move_joint** (``lebai_msgs/MoveJoint``)

  机械臂关节移动。
  
  该服务仅向机械臂控制器发送移动请求，机械臂缓存该移动请求，该服务返回并不代表机械臂移动到终点位置。

  脚本示例::

    rosservice call /motion_service/move_joint "{is_joint_pose: 1, joint_pose: [3.1,-1.57,-2.2,-1.03,1.67,1.62], common: {vel: 0.5, acc: 1.0, time: 0.0, radius: 0.0}}"

* **motion_service/move_line** (``lebai_msgs/MoveLine``)

  机械臂直线移动。该服务仅向机械臂控制器发送移动请求，机械臂缓存该移动请求，该服务返回并不代表机械臂移动到终点位置。

  脚本示例::

    rosservice call /motion_service/move_line "{is_joint_pose: 0, cartesian_pose: {position: {x: -0.3,y: 0.125,z: 0.4077}, orientation: {x: 0.99669, y: -0.047447,z: 0.043886, w: 0.049333}}, common: {vel: 0.2, acc: 1.0, time: 0.0, radius: 0.0}}"

* **motion_service/speed_joint** (``lebai_msgs/SpeedJoint``)

  机械臂关节指定速度移动。

  脚本示例::

    rosservice call /motion_service/speed_joint "{joint_vel: [-0.1,0.0,0.0,0.0,0.0,0.0], acc: 1.0, time: 0.0}"

* **motion_service/speed_line** (``lebai_msgs/SpeedLine``)

  机械臂坐标指定方向移动。

  脚本示例::

    rosservice call /motion_service/speed_line "{vel: {linear: {x: 0.0, y: 0.0, z: -0.1}, angular: {x: 0.0, y: 0.0, z: 0.0}}, acc: 1.0, time: 0.0}"

* **motion_service/stop_motion** (``std_srvs/Empty``)

  停止移动。

  脚本示例::

    rosservice call /motion_service/stop_motion "{}"


* **/io_service/set_robot_do** (``lebai_msgs/SetDO``)

  设置控制柜模拟量量输出。

  脚本示例::

    rosservice call /io_service/set_robot_do "{pin: 0,value: false}"

* **/io_service/set_flange_do** (``lebai_msgs/SetDO``)

  设置法兰数字量输出。

  脚本示例::

    rosservice call /io_service/set_flange_do "{pin: 0,value: false}"

* **/io_service/set_robot_ao** (``lebai_msgs/SetAO``)

  设置控制柜模拟量输出。

  脚本示例::

    rosservice call /io_service/set_robot_ao "{pin: 0,value: 0.5}"

* **/io_service/set_robot_ao_mode** (``lebai_msgs/SetAMode``)

  设置控制柜模拟量输出模式。

  脚本示例::

    rosservice call /io_service/set_robot_ao_mode "{pin: 0, mode: 0}" 

* **/io_service/set_robot_ai_mode** (``lebai_msgs/SetAMode``)

  设置控制柜模拟量输入模式。

  脚本示例::

    rosservice call /io_service/set_robot_ai_mode "{pin: 0, mode: 0}" 

* **/io_service/set_gripper_force** (``lebai_msgs/SetGripper``)

  设置夹爪力。

  脚本示例::

    rosservice call /io_service/set_gripper_force "{val: 0.2}"

* **/io_service/set_gripper_position** (``lebai_msgs/SetGripper``)

  设置夹爪位置。

  脚本示例::

    rosservice call /io_service/set_gripper_position "{val: 0.2}"
