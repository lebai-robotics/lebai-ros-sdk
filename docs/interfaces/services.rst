Services
========

The examples below assume the default ``/lebai`` namespace. All command-style
responses include ``lebai_interfaces/msg/Result``.

Start Stop
----------

.. list-table::
   :header-rows: 1

   * - Service
     - Type
   * - ``/lebai/start_stop/start_sys``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/stop_sys``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/powerdown``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/stop``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/estop``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/start_teach_mode``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/end_teach_mode``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/pause_move``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/resume_move``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/start_stop/reboot``
     - ``lebai_interfaces/srv/Command``

Motion
------

.. list-table::
   :header-rows: 1

   * - Service
     - Type
   * - ``/lebai/motion/movej``
     - ``lebai_interfaces/srv/MoveJoint``
   * - ``/lebai/motion/movel``
     - ``lebai_interfaces/srv/MoveLinear``
   * - ``/lebai/motion/movec``
     - ``lebai_interfaces/srv/MoveCircular``
   * - ``/lebai/motion/speedj``
     - ``lebai_interfaces/srv/SpeedJoint``
   * - ``/lebai/motion/speedl``
     - ``lebai_interfaces/srv/SpeedLinear``
   * - ``/lebai/motion/move_pvat``
     - ``lebai_interfaces/srv/MovePvat``
   * - ``/lebai/motion/wait_move``
     - ``lebai_interfaces/srv/WaitMove``
   * - ``/lebai/motion/stop_move``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/motion/skip_move``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/motion/get_running_motion``
     - ``lebai_interfaces/srv/GetRunningMotion``
   * - ``/lebai/motion/get_motion_state``
     - ``lebai_interfaces/srv/GetMotionState``

IO
--

.. list-table::
   :header-rows: 1

   * - Service
     - Type
   * - ``/lebai/io/set_do``
     - ``lebai_interfaces/srv/SetDigitalOutput``
   * - ``/lebai/io/get_di``
     - ``lebai_interfaces/srv/GetDigitalInput``
   * - ``/lebai/io/get_do``
     - ``lebai_interfaces/srv/GetDigitalOutput``
   * - ``/lebai/io/set_ao``
     - ``lebai_interfaces/srv/SetAnalogOutput``
   * - ``/lebai/io/get_ai``
     - ``lebai_interfaces/srv/GetAnalogInput``
   * - ``/lebai/io/get_ao``
     - ``lebai_interfaces/srv/GetAnalogOutput``
   * - ``/lebai/io/set_dio_mode``
     - ``lebai_interfaces/srv/SetDioMode``
   * - ``/lebai/io/get_dio_mode``
     - ``lebai_interfaces/srv/GetDioMode``

Claw
----

.. list-table::
   :header-rows: 1

   * - Service
     - Type
   * - ``/lebai/claw/init_claw``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/claw/set_claw``
     - ``lebai_interfaces/srv/SetClaw``
   * - ``/lebai/claw/get_claw``
     - ``lebai_interfaces/srv/GetClaw``

Discovery
---------

.. list-table::
   :header-rows: 1

   * - Service
     - Type
   * - ``/lebai/discovery/resolve``
     - ``lebai_interfaces/srv/ResolveControllers``

Standalone Gripper
------------------

.. list-table::
   :header-rows: 1

   * - Service
     - Type
   * - ``/lebai/gripper/set_position``
     - ``lebai_interfaces/srv/SetGripperPosition``
   * - ``/lebai/gripper/set_force``
     - ``lebai_interfaces/srv/SetGripperForce``
   * - ``/lebai/gripper/set_velocity``
     - ``lebai_interfaces/srv/SetGripperVelocity``
   * - ``/lebai/gripper/do_calibration``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/gripper/turn_on_auto_calibration``
     - ``lebai_interfaces/srv/Command``
   * - ``/lebai/gripper/turn_off_auto_calibration``
     - ``lebai_interfaces/srv/Command``
