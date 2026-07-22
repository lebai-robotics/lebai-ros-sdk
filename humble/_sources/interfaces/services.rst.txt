服务 Services
=============

以下表格是当前 runtime 的完整 service 清单，使用默认 ``/lebai`` 命名空间。
名称在 node 中是相对名称；修改对应 launch 的 ``namespace`` 参数后，前缀会
随之变化。每个响应都包含 ``lebai_interfaces/msg/Result``：

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
   ros2 service call /lebai/start_stop/stop_sys lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/powerdown lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/stop lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/estop lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/start_teach_mode lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/end_teach_mode lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/pause_move lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/resume_move lebai_interfaces/srv/Command
   ros2 service call /lebai/start_stop/reboot lebai_interfaces/srv/Command

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

``WaitMove.motion_id`` 必须大于 0；ID 0 的“等待整个运动缓冲区”语义不能用
非阻塞状态查询等价实现，因此会被拒绝。``timeout_sec`` 为 0 时无限等待，
大于 0 时使用单调时钟限制最长等待秒数。驱动每 0.05 秒查询一次运动状态，
不会调用阻塞式 SDK ``wait_move``，因此等待期间仍可处理 ``stop_move`` 和
急停请求。同一驱动实例仅允许一个活动的等待请求，并发等待会立即返回失败，
避免耗尽执行器线程。超时、无效参数、未知状态或后端错误都会返回失败结果。

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

圆弧、速度和 PVAT 运动示例：

.. code-block:: bash

   ros2 service call /lebai/motion/movec lebai_interfaces/srv/MoveCircular "{via: {is_joint_pose: true, joint_positions: [0.0, -0.4, 0.4, 0.0, 0.4, 0.0]}, target: {is_joint_pose: true, joint_positions: [0.0, -0.5, 0.5, 0.0, 0.5, 0.0]}, rad: 1.5708, params: {acceleration: 0.5, velocity: 0.2, time: 0.0, blend_radius: 0.0}}"
   ros2 service call /lebai/motion/speedj lebai_interfaces/srv/SpeedJoint "{acceleration: 0.5, velocities: [0.1, 0.0, 0.0, 0.0, 0.0, 0.0], time: 1.0}"
   ros2 service call /lebai/motion/speedl lebai_interfaces/srv/SpeedLinear "{acceleration: 0.5, velocity: {linear: {x: 0.01, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}, time: 1.0, reference: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}"
   ros2 service call /lebai/motion/move_pvat lebai_interfaces/srv/MovePvat "{positions: [0.0, -0.5, 0.5, 0.0, 0.5, 0.0], velocities: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], accelerations: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], duration: 0.1}"

运动控制和状态查询示例（将 ``motion_id`` 替换为运动 service 返回的 ID）：

.. code-block:: bash

   ros2 service call /lebai/motion/wait_move lebai_interfaces/srv/WaitMove "{motion_id: 1, timeout_sec: 5.0}"
   ros2 service call /lebai/motion/stop_move lebai_interfaces/srv/Command
   ros2 service call /lebai/motion/skip_move lebai_interfaces/srv/Command
   ros2 service call /lebai/motion/get_running_motion lebai_interfaces/srv/GetRunningMotion
   ros2 service call /lebai/motion/get_motion_state lebai_interfaces/srv/GetMotionState "{motion_id: 1}"

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
``MODE_FLASH``，对应数值范围 0 至 6。``SetLed.speed`` 使用
``SPEED_UNSPECIFIED``、``SPEED_FAST``、``SPEED_NORMAL`` 和 ``SPEED_SLOW``，
对应数值范围 0 至 3；数值 0 表示控制器/protobuf 的未指定速度，不是快速、
正常或慢速，数值 1、2、3 分别表示快速、正常、慢速。``color`` 可含 0 至 4
个数值为 0 至 15 的调色板索引。

LED 参数不满足上述范围时，驱动不会调用 SDK，并在 ``Result`` 中返回失败；
设置成功时响应只包含成功的 ``Result``。

``GetSignals.index`` 是连续读取的起始 signal 索引，``length`` 是读取数量，
响应的 ``values`` 是 ``int32`` 数组。``SetSignals.index`` 是连续写入的起始
索引，``values`` 中的 ``int32`` 值按顺序写入。索引和读取数量是 ``uint32``；
驱动不增加额外范围限制，而由控制器检查实际 signal 范围。设置响应只包含
``Result``，后端调用失败时返回失败。

示例：

.. code-block:: bash

   ros2 service call /lebai/led/set_led lebai_interfaces/srv/SetLed "{mode: 2, speed: 0, color: [3]}"
   ros2 service call /lebai/signal/get_signals lebai_interfaces/srv/GetSignals "{index: 0, length: 2}"
   ros2 service call /lebai/signal/set_signals lebai_interfaces/srv/SetSignals "{index: 0, values: [100, -100]}"

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
   * - ``/lebai/io/set_dos``
     - ``lebai_interfaces/srv/SetDigitalOutputs``
     - 连续设置多个数字输出。
   * - ``/lebai/io/get_dis``
     - ``lebai_interfaces/srv/GetDigitalInputs``
     - 连续读取多个数字输入。
   * - ``/lebai/io/get_dos``
     - ``lebai_interfaces/srv/GetDigitalOutputs``
     - 连续读取多个数字输出。
   * - ``/lebai/io/set_ao``
     - ``lebai_interfaces/srv/SetAnalogOutput``
     - 设置模拟输出。
   * - ``/lebai/io/get_ai``
     - ``lebai_interfaces/srv/GetAnalogInput``
     - 读取模拟输入。
   * - ``/lebai/io/get_ao``
     - ``lebai_interfaces/srv/GetAnalogOutput``
     - 读取模拟输出。
   * - ``/lebai/io/set_aos``
     - ``lebai_interfaces/srv/SetAnalogOutputs``
     - 连续设置多个模拟输出。
   * - ``/lebai/io/get_ais``
     - ``lebai_interfaces/srv/GetAnalogInputs``
     - 连续读取多个模拟输入。
   * - ``/lebai/io/get_aos``
     - ``lebai_interfaces/srv/GetAnalogOutputs``
     - 连续读取多个模拟输出。
   * - ``/lebai/io/set_dio_mode``
     - ``lebai_interfaces/srv/SetDioMode``
     - 设置 DIO 模式。
   * - ``/lebai/io/get_dio_mode``
     - ``lebai_interfaces/srv/GetDioMode``
     - 读取 DIO 模式。

批量 IO 请求使用 ``device`` 和 ``pin`` 指定设备与连续范围的起始引脚。
``SetDigitalOutputs.values`` 和 ``SetAnalogOutputs.values`` 按引脚顺序写入；
``GetDigitalInputs``、``GetDigitalOutputs``、``GetAnalogInputs`` 和
``GetAnalogOutputs`` 使用 ``num`` 指定读取数量，并分别在 ``values`` 中返回
``bool`` 或 ``float64`` 数组。``pin`` 和 ``num`` 是 ``uint32``。ROS 驱动将
``device`` 字符串原样传给 SDK；released lebai-sdk 使用大写规范名
``ROBOT``、``FLANGE``、``EXTRA``、``ROBOT_BTN``、``SHOULDER`` 和
``FLANGE_BTN``。其他任何拼写（包括小写和拼写错误）都会映射到 ``ROBOT``，
而不是返回错误，因此调用方应始终使用大写规范名。驱动不增加 device 名称
校验；控制器继续检查有效引脚范围。设置响应只包含 ``Result``，后端调用失败
时返回失败。

示例：

.. code-block:: bash

   ros2 service call /lebai/io/set_do lebai_interfaces/srv/SetDigitalOutput "{device: ROBOT, pin: 0, value: true}"
   ros2 service call /lebai/io/get_di lebai_interfaces/srv/GetDigitalInput "{device: ROBOT, pin: 0}"
   ros2 service call /lebai/io/get_do lebai_interfaces/srv/GetDigitalOutput "{device: ROBOT, pin: 0}"
   ros2 service call /lebai/io/set_dos lebai_interfaces/srv/SetDigitalOutputs "{device: ROBOT, pin: 0, values: [true, false]}"
   ros2 service call /lebai/io/get_dis lebai_interfaces/srv/GetDigitalInputs "{device: ROBOT, pin: 0, num: 2}"
   ros2 service call /lebai/io/get_dos lebai_interfaces/srv/GetDigitalOutputs "{device: ROBOT, pin: 0, num: 2}"
   ros2 service call /lebai/io/set_ao lebai_interfaces/srv/SetAnalogOutput "{device: ROBOT, pin: 0, value: 1.0}"
   ros2 service call /lebai/io/get_ai lebai_interfaces/srv/GetAnalogInput "{device: ROBOT, pin: 0}"
   ros2 service call /lebai/io/get_ao lebai_interfaces/srv/GetAnalogOutput "{device: ROBOT, pin: 0}"
   ros2 service call /lebai/io/set_aos lebai_interfaces/srv/SetAnalogOutputs "{device: ROBOT, pin: 0, values: [1.0, 2.0]}"
   ros2 service call /lebai/io/get_ais lebai_interfaces/srv/GetAnalogInputs "{device: ROBOT, pin: 0, num: 2}"
   ros2 service call /lebai/io/get_aos lebai_interfaces/srv/GetAnalogOutputs "{device: ROBOT, pin: 0, num: 2}"
   ros2 service call /lebai/io/set_dio_mode lebai_interfaces/srv/SetDioMode "{device: ROBOT, pin: 0, is_output: true}"
   ros2 service call /lebai/io/get_dio_mode lebai_interfaces/srv/GetDioMode "{device: ROBOT, pin: 0}"

配置 config
-----------

.. list-table::
   :header-rows: 1

   * - Service
     - 类型
     - 用途
   * - ``/lebai/config/load_tcp_list``
     - ``lebai_interfaces/srv/LoadResourceList``
     - 读取控制器中的 TCP 名称列表。
   * - ``/lebai/config/load_pose_list``
     - ``lebai_interfaces/srv/LoadResourceList``
     - 读取控制器中的位姿名称列表。
   * - ``/lebai/config/load_frame_list``
     - ``lebai_interfaces/srv/LoadResourceList``
     - 读取控制器中的坐标系名称列表。
   * - ``/lebai/config/load_trajectory_list``
     - ``lebai_interfaces/srv/LoadResourceList``
     - 读取控制器中的轨迹名称列表。

``directory`` 是任意字符串，用于指定控制器上的资源目录；空字符串表示
控制器默认的根目录，驱动不增加路径格式限制。响应的 ``names`` 是该目录下
的名称字符串数组。SDK 调用失败时，响应的 ``Result`` 返回失败。

示例：

.. code-block:: bash

   ros2 service call /lebai/config/load_tcp_list lebai_interfaces/srv/LoadResourceList "{directory: tools}"
   ros2 service call /lebai/config/load_pose_list lebai_interfaces/srv/LoadResourceList "{directory: waypoints}"
   ros2 service call /lebai/config/load_frame_list lebai_interfaces/srv/LoadResourceList "{directory: fixtures}"
   ros2 service call /lebai/config/load_trajectory_list lebai_interfaces/srv/LoadResourceList "{directory: jobs}"

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
   ros2 service call /lebai/gripper/do_calibration lebai_interfaces/srv/Command
   ros2 service call /lebai/gripper/turn_on_auto_calibration lebai_interfaces/srv/Command
   ros2 service call /lebai/gripper/turn_off_auto_calibration lebai_interfaces/srv/Command
