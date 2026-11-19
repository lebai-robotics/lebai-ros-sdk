服务
====

下列路径使用默认的 ``/lebai`` 命名空间，服务类型均来自 ``lebai_interfaces``。
每个响应包含 ``result``，其中有 ``success``、``code`` 和 ``message`` 三个字段。
结果码 ``0`` 表示成功，``1`` 表示 SDK 错误。运动服务在已安装的 SDK 缺少
所请求的方法时返回 ``2``。使用返回数据前请先检查 ``result.success``。

可通过正在运行的服务查看其请求和响应字段。

.. code-block:: bash

   rosservice type /lebai/motion/movej
   rossrv show lebai_interfaces/MoveJoint

启停与系统管理
--------------

``/lebai/start_stop/`` 下的服务类型均为 ``Command``，请求为空。

* ``start_sys``、``stop_sys``、``powerdown``、``stop``、``estop`` 和 ``reboot``
* ``start_teach_mode`` 和 ``end_teach_mode``
* ``pause_move`` 和 ``resume_move``

运动
----

运动服务使用 ``/lebai/motion/`` 前缀。

.. list-table::
   :header-rows: 1

   * - 服务
     - 类型
   * - ``movej``
     - ``MoveJoint``
   * - ``movel``
     - ``MoveLinear``
   * - ``movec``
     - ``MoveCircular``
   * - ``speedj``
     - ``SpeedJoint``
   * - ``speedl``
     - ``SpeedLinear``
   * - ``move_pvat``
     - ``MovePvat``
   * - ``wait_move``
     - ``WaitMove``
   * - ``stop_move``, ``skip_move``
     - ``Command``
   * - ``get_running_motion``
     - ``GetRunningMotion``
   * - ``get_motion_state``
     - ``GetMotionState``

``movej``、``movel``、``movec``、``speedj``、``speedl`` 和
``get_running_motion`` 返回无符号的 ``motion_id``。
``movec`` 要求 ``via`` 和 ``target`` 同时使用关节坐标，或同时使用笛卡尔坐标。
混用两种坐标时，驱动在调用 SDK 运动方法前返回错误码 ``1``。
``get_motion_state`` 接收运动 ID 并返回状态字符串。

``wait_move`` 在 SDK 中阻塞等待指定运动完成。等待期间，其他驱动服务（包括
``stop_move``）也会等待，状态话题会跳过更新。ROS 服务端未设置等待超时。
如果需要持续读取状态或调用其他服务，可以轮询 ``get_motion_state``。

I/O
---

``/lebai/io/`` 下的每个请求都指定设备 ``device`` 和起始引脚 ``pin``。
批量读取时用 ``num`` 指定引脚数量，批量写入时提供 ``values`` 数组。

.. list-table::
   :header-rows: 1

   * - 服务
     - 类型
   * - ``get_di``, ``get_do``, ``set_do``
     - ``GetDigitalInput``, ``GetDigitalOutput``, ``SetDigitalOutput``
   * - ``get_dis``, ``get_dos``, ``set_dos``
     - ``GetDigitalInputs``, ``GetDigitalOutputs``, ``SetDigitalOutputs``
   * - ``get_ai``, ``get_ao``, ``set_ao``
     - ``GetAnalogInput``, ``GetAnalogOutput``, ``SetAnalogOutput``
   * - ``get_ais``, ``get_aos``, ``set_aos``
     - ``GetAnalogInputs``, ``GetAnalogOutputs``, ``SetAnalogOutputs``
   * - ``get_dio_mode``, ``set_dio_mode``
     - ``GetDioMode``, ``SetDioMode``

LED 和信号
----------

* ``/lebai/led/set_led`` （``SetLed``）接收模式、速度和颜色。
* ``/lebai/signal/get_signals`` （``GetSignals``）从指定索引开始读取一定数量的
  信号值。
* ``/lebai/signal/set_signals`` （``SetSignals``）从指定索引开始写入信号值。

资源
----

``/lebai/resource/`` 下的 ``load_tcp_list``、``load_pose_list``、
``load_frame_list`` 和 ``load_trajectory_list`` 都使用 ``LoadResourceList``。
传入目录 ``directory``，从响应的 ``names`` 数组读取名称。

内置夹爪
--------

* ``/lebai/claw/init_claw`` （``Command``）初始化夹爪。
* ``/lebai/claw/set_claw`` （``SetClaw``）接收夹持力 ``force`` 和开合幅度
  ``amplitude``。
* ``/lebai/claw/get_claw`` （``GetClaw``）返回 ``ClawState`` 类型的 ``state``。

串口夹爪
--------

串口夹爪节点在 ``/lebai/gripper/`` 下提供以下服务。

* ``set_position`` （``SetGripperPosition``）设置位置。
* ``set_force`` （``SetGripperForce``）设置夹持力。
* ``set_velocity`` （``SetGripperVelocity``）接收速度 ``velocity`` 和持久化标志
  ``persistent``。
* ``do_calibration``、``turn_on_auto_calibration`` 和
  ``turn_off_auto_calibration`` 的类型均为 ``Command``。

发现控制器
----------

发现节点提供 ``/lebai/discovery/resolve`` （``ResolveControllers``）。
请求为空，返回的 ``controllers`` 数组以 ``ControllerInfo`` 记录发现的控制器。
