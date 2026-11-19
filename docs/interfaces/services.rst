Services
========

All paths use the default ``/lebai`` namespace. Service types below belong
to ``lebai_interfaces``. Each response includes ``result`` with
``success``, ``code``, and ``message`` fields. Code ``0`` indicates
success, ``1`` indicates an SDK error, and motion services return ``2``
when the installed SDK lacks the requested method. Check ``result.success``
before using any returned data.

Inspect a live service to see its generated request and response fields.

.. code-block:: bash

   rosservice type /lebai/motion/movej
   rossrv show lebai_interfaces/MoveJoint

Robot lifecycle
---------------

Under ``/lebai/start_stop/``, every service has type ``Command`` with an
empty request.

* ``start_sys``, ``stop_sys``, ``powerdown``, ``stop``, ``estop``,
  and ``reboot``
* ``start_teach_mode`` and ``end_teach_mode``
* ``pause_move`` and ``resume_move``

Motion
------

The motion services use the ``/lebai/motion/`` prefix.

.. list-table::
   :header-rows: 1

   * - Service
     - Type
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

``movej``, ``movel``, ``movec``, ``speedj``, ``speedl``, and
``get_running_motion`` return an unsigned ``motion_id``.
``get_motion_state`` accepts a motion ID and returns a state string.
``wait_move`` waits in the SDK for the supplied motion ID and blocks other
driver services during that wait. See :doc:`../architecture`.

I/O
---

Under ``/lebai/io/``, each request identifies a ``device`` and starting
``pin``. Batch reads specify ``num`` pins, and batch writes provide a
``values`` array.

.. list-table::
   :header-rows: 1

   * - Service
     - Type
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

LED and signals
---------------

* ``/lebai/led/set_led`` (``SetLed``) takes mode, speed, and color.
* ``/lebai/signal/get_signals`` (``GetSignals``) reads a length of signal
  values starting at an index.
* ``/lebai/signal/set_signals`` (``SetSignals``) writes values starting at
  an index.

Resources
---------

Under ``/lebai/resource/``, ``load_tcp_list``, ``load_pose_list``,
``load_frame_list``, and ``load_trajectory_list`` use ``LoadResourceList``.
Pass a ``directory`` and read the returned ``names`` array.

Integrated claw
---------------

* ``/lebai/claw/init_claw`` (``Command``)
* ``/lebai/claw/set_claw`` (``SetClaw``) takes ``force`` and ``amplitude``.
* ``/lebai/claw/get_claw`` (``GetClaw``) returns ``state`` of type
  ``ClawState``.

Serial gripper
--------------

The serial gripper node provides the following services under
``/lebai/gripper/``.

* ``set_position`` (``SetGripperPosition``)
* ``set_force`` (``SetGripperForce``)
* ``set_velocity`` (``SetGripperVelocity``) takes ``velocity`` and
  ``persistent``.
* ``do_calibration``, ``turn_on_auto_calibration``, and
  ``turn_off_auto_calibration`` have type ``Command``.

Discovery
---------

The discovery node provides ``/lebai/discovery/resolve``
(``ResolveControllers``). It takes an empty request and returns a
``controllers`` array of ``ControllerInfo`` records for the discovered
controllers.
