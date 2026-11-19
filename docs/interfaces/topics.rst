Status topics
=============

These are the default topic paths. A different ``namespace`` launch
argument changes the ``/lebai`` prefix.

.. list-table::
   :header-rows: 1

   * - Topic
     - ROS message
     - Default rate
     - Contents
   * - ``/lebai/status/joint_states``
     - ``sensor_msgs/JointState``
     - 20 Hz
     - Arm joint names, measured positions, velocities, and torques.
   * - ``/lebai/status/robot``
     - ``lebai_interfaces/RobotState``
     - 10 Hz
     - Controller state, emergency stop reason, and connection flags.
   * - ``/lebai/status/joint_motion``
     - ``lebai_interfaces/JointMotion``
     - 20 Hz
     - Actual and target arm joint positions, speeds, torques, and TCP
       poses, plus the actual flange pose.
   * - ``/lebai/io/state``
     - ``lebai_interfaces/IOState``
     - 10 Hz
     - Digital and analog I/O and DIO modes for the configured device and
       pin counts.
   * - ``/lebai/claw/state``
     - ``lebai_interfaces/ClawState``
     - 10 Hz
     - Integrated claw force, amplitude, and whether the claw is holding.
   * - ``/lebai/claw/joint_states``
     - ``sensor_msgs/JointState``
     - 10 Hz
     - Integrated claw's active model joint position.
   * - ``/lebai/model/joint_states``
     - ``sensor_msgs/JointState``
     - 20 Hz
     - Combined arm and integrated claw active joint state.
   * - ``/lebai/gripper/state``
     - ``lebai_interfaces/GripperState``
     - 10 Hz
     - Position, force, velocity, and calibration state from the separate
       serial gripper node.

Driver and serial status messages with a ``connected`` field report
``connected: false`` and populate ``message`` when an SDK read fails.
For arm-only LM3, use ``/lebai/status/joint_states`` without the claw data.

See :doc:`../quickstart` to change the publish rates or I/O pin counts.
The controller actions are listed in :doc:`../architecture`.
