服务 Services
=============

以下 service 使用默认 ``/lebai`` 命名空间。每个响应都包含
``lebai_interfaces/msg/Result``：

.. code-block:: text

   bool success
   int32 code
   string message

``success`` 为 ``true`` 表示调用成功。调用失败时，``message`` 会包含错误信息。

启动停止 start_stop
-------------------

.. list-table::
   :header-rows: 1

   * - Service
     - 类型
     - 用途
   * - ``/lebai/start_stop/start_sys``
     - ``lebai_interfaces/srv/Command``
     - 启动系统。
   * - ``/lebai/start_stop/stop_sys``
     - ``lebai_interfaces/srv/Command``
     - 停止系统。
   * - ``/lebai/start_stop/powerdown``
     - ``lebai_interfaces/srv/Command``
     - 关机。
   * - ``/lebai/start_stop/stop``
     - ``lebai_interfaces/srv/Command``
     - 停止机器人。
   * - ``/lebai/start_stop/estop``
     - ``lebai_interfaces/srv/Command``
     - 急停。
   * - ``/lebai/start_stop/start_teach_mode``
     - ``lebai_interfaces/srv/Command``
     - 进入示教模式。
   * - ``/lebai/start_stop/end_teach_mode``
     - ``lebai_interfaces/srv/Command``
     - 退出示教模式。
   * - ``/lebai/start_stop/pause_move``
     - ``lebai_interfaces/srv/Command``
     - 暂停运动。
   * - ``/lebai/start_stop/resume_move``
     - ``lebai_interfaces/srv/Command``
     - 恢复运动。
   * - ``/lebai/start_stop/reboot``
     - ``lebai_interfaces/srv/Command``
     - 重启控制器。

示例：

.. code-block:: bash

   ros2 service call /lebai/start_stop/start_sys lebai_interfaces/srv/Command

运动 motion
-----------

.. list-table::
   :header-rows: 1

   * - Service
     - 类型
     - 用途
   * - ``/lebai/motion/movej``
     - ``lebai_interfaces/srv/MoveJoint``
     - 关节运动。
   * - ``/lebai/motion/movel``
     - ``lebai_interfaces/srv/MoveLinear``
     - 直线运动。
   * - ``/lebai/motion/movec``
     - ``lebai_interfaces/srv/MoveCircular``
     - 圆弧运动。
   * - ``/lebai/motion/speedj``
     - ``lebai_interfaces/srv/SpeedJoint``
     - 关节速度控制。
   * - ``/lebai/motion/speedl``
     - ``lebai_interfaces/srv/SpeedLinear``
     - TCP 速度控制。
   * - ``/lebai/motion/move_pvat``
     - ``lebai_interfaces/srv/MovePvat``
     - PVAT 运动。
   * - ``/lebai/motion/wait_move``
     - ``lebai_interfaces/srv/WaitMove``
     - 等待指定运动完成。
   * - ``/lebai/motion/stop_move``
     - ``lebai_interfaces/srv/Command``
     - 停止当前运动。
   * - ``/lebai/motion/skip_move``
     - ``lebai_interfaces/srv/Command``
     - 跳过当前运动。
   * - ``/lebai/motion/get_running_motion``
     - ``lebai_interfaces/srv/GetRunningMotion``
     - 获取当前运动 ID。
   * - ``/lebai/motion/get_motion_state``
     - ``lebai_interfaces/srv/GetMotionState``
     - 获取指定运动状态。

``MotionTarget.cartesian_pose`` 和 ``SpeedLinear.reference`` 使用
``geometry_msgs/msg/Pose``。``SpeedLinear.velocity`` 使用
``geometry_msgs/msg/Twist``：``linear`` 对应 TCP 线速度，``angular`` 对应
角速度。所有 ``Pose.orientation`` 都必须是有限的非零四元数；驱动会先
归一化，再按控制器的 Euler ZYX 定义
``Rz(rz) * Ry(ry) * Rx(rx)`` 转换。

``MovePvat`` 的 ``positions``、``velocities`` 和 ``accelerations`` 必须各含
6 个有限数值，``duration`` 必须是大于零的有限秒数。无效请求会在进入
``pylebai`` 前返回失败。

关节运动示例：

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

直线运动示例：

.. code-block:: bash

   ros2 service call /lebai/motion/movel lebai_interfaces/srv/MoveLinear "{
     target: {
       is_joint_pose: false,
       cartesian_pose: {
         position: {x: 0.3, y: 0.0, z: 0.4},
         orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
       }
     },
     params: {
       acceleration: 0.5,
       velocity: 0.2,
       time: 0.0,
       blend_radius: 0.0
     }
   }"

查询当前运动：

.. code-block:: bash

   ros2 service call /lebai/motion/get_running_motion lebai_interfaces/srv/GetRunningMotion

LED 和 signal
-------------

.. list-table::
   :header-rows: 1

   * - Service
     - 类型
     - 用途
   * - ``/lebai/led/set_led``
     - ``lebai_interfaces/srv/SetLed``
     - 设置控制器 LED。
   * - ``/lebai/signal/get_signals``
     - ``lebai_interfaces/srv/GetSignals``
     - 读取连续 signal 值。
   * - ``/lebai/signal/set_signals``
     - ``lebai_interfaces/srv/SetSignals``
     - 写入连续 signal 值。

``SetLed.mode`` 使用 ``MODE_UNCHANGED``、``MODE_OFF``、``MODE_STEADY``、
``MODE_BREATH``、``MODE_ROTATE_SEGMENTED``、``MODE_ROTATE_SOLID`` 和
``MODE_FLASH``。``SetLed.speed`` 使用 ``SPEED_UNSPECIFIED``、``SPEED_FAST``、
``SPEED_NORMAL`` 和 ``SPEED_SLOW``；数值 0 表示控制器/protobuf 的未指定速度，
不是快速、正常或慢速。``color`` 可含 0 至 4 个数值为 0 至 15 的调色板索引。

IO
--

.. list-table::
   :header-rows: 1

   * - Service
     - 类型
     - 用途
   * - ``/lebai/io/set_do``
     - ``lebai_interfaces/srv/SetDigitalOutput``
     - 设置数字输出。
   * - ``/lebai/io/get_di``
     - ``lebai_interfaces/srv/GetDigitalInput``
     - 读取数字输入。
   * - ``/lebai/io/get_do``
     - ``lebai_interfaces/srv/GetDigitalOutput``
     - 读取数字输出。
   * - ``/lebai/io/set_ao``
     - ``lebai_interfaces/srv/SetAnalogOutput``
     - 设置模拟输出。
   * - ``/lebai/io/get_ai``
     - ``lebai_interfaces/srv/GetAnalogInput``
     - 读取模拟输入。
   * - ``/lebai/io/get_ao``
     - ``lebai_interfaces/srv/GetAnalogOutput``
     - 读取模拟输出。
   * - ``/lebai/io/set_dio_mode``
     - ``lebai_interfaces/srv/SetDioMode``
     - 设置 DIO 模式。
   * - ``/lebai/io/get_dio_mode``
     - ``lebai_interfaces/srv/GetDioMode``
     - 读取 DIO 模式。

示例：

.. code-block:: bash

   ros2 service call /lebai/io/set_do lebai_interfaces/srv/SetDigitalOutput "{device: robot, pin: 0, value: true}"
   ros2 service call /lebai/io/get_di lebai_interfaces/srv/GetDigitalInput "{device: robot, pin: 0}"

内置夹爪 claw
-------------

.. list-table::
   :header-rows: 1

   * - Service
     - 类型
     - 用途
   * - ``/lebai/claw/init_claw``
     - ``lebai_interfaces/srv/Command``
     - 初始化内置 claw。
   * - ``/lebai/claw/set_claw``
     - ``lebai_interfaces/srv/SetClaw``
     - 设置 claw 力和开合幅度。
   * - ``/lebai/claw/get_claw``
     - ``lebai_interfaces/srv/GetClaw``
     - 读取 claw 状态。

示例：

.. code-block:: bash

   ros2 service call /lebai/claw/init_claw lebai_interfaces/srv/Command
   ros2 service call /lebai/claw/set_claw lebai_interfaces/srv/SetClaw "{amplitude: 40.0, force: 50.0}"
   ros2 service call /lebai/claw/get_claw lebai_interfaces/srv/GetClaw

发现 discovery
--------------

.. list-table::
   :header-rows: 1

   * - Service
     - 类型
     - 用途
   * - ``/lebai/discovery/resolve``
     - ``lebai_interfaces/srv/ResolveControllers``
     - 发现局域网中的 Lebai 控制器。

示例：

.. code-block:: bash

   ros2 service call /lebai/discovery/resolve lebai_interfaces/srv/ResolveControllers

独立夹爪 gripper
----------------

.. list-table::
   :header-rows: 1

   * - Service
     - 类型
     - 用途
   * - ``/lebai/gripper/set_position``
     - ``lebai_interfaces/srv/SetGripperPosition``
     - 设置 gripper 位置。
   * - ``/lebai/gripper/set_force``
     - ``lebai_interfaces/srv/SetGripperForce``
     - 设置 gripper 力。
   * - ``/lebai/gripper/set_velocity``
     - ``lebai_interfaces/srv/SetGripperVelocity``
     - 设置 gripper 速度。
   * - ``/lebai/gripper/do_calibration``
     - ``lebai_interfaces/srv/Command``
     - 执行标定。
   * - ``/lebai/gripper/turn_on_auto_calibration``
     - ``lebai_interfaces/srv/Command``
     - 开启自动标定。
   * - ``/lebai/gripper/turn_off_auto_calibration``
     - ``lebai_interfaces/srv/Command``
     - 关闭自动标定。

示例：

.. code-block:: bash

   ros2 service call /lebai/gripper/set_position lebai_interfaces/srv/SetGripperPosition "{position: 50}"
   ros2 service call /lebai/gripper/set_force lebai_interfaces/srv/SetGripperForce "{force: 50}"
   ros2 service call /lebai/gripper/set_velocity lebai_interfaces/srv/SetGripperVelocity "{velocity: 50, persistent: false}"
