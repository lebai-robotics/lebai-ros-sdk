Topics
======

The examples below assume the default ``/lebai`` namespace.

Driver Topics
-------------

.. list-table::
   :header-rows: 1

   * - Topic
     - Type
     - Purpose
   * - ``/lebai/status/joint_states``
     - ``sensor_msgs/msg/JointState``
     - Current joint positions, velocity, and effort.
   * - ``/lebai/status/robot``
     - ``lebai_interfaces/msg/RobotState``
     - Controller state, estop reason, and connection flags.
   * - ``/lebai/status/joint_motion``
     - ``lebai_interfaces/msg/JointMotion``
     - Actual and target joint/TCP motion data.
   * - ``/lebai/io/state``
     - ``lebai_interfaces/msg/IOState``
     - Configured IO snapshot for one device.
   * - ``/lebai/claw/state``
     - ``lebai_interfaces/msg/ClawState``
     - Robot claw force, amplitude, and hold state.

Standalone Gripper Topics
-------------------------

.. list-table::
   :header-rows: 1

   * - Topic
     - Type
     - Purpose
   * - ``/lebai/gripper/state``
     - ``lebai_interfaces/msg/GripperState``
     - Standalone serial gripper position, force, velocity, and calibration.

Status Parameters
-----------------

The driver exposes publish-rate parameters for each state stream:

.. code-block:: text

   joint_state_publish_rate
   robot_state_publish_rate
   joint_motion_publish_rate
   io_state_publish_rate
   gripper_state_publish_rate

IO state also uses count parameters so users can choose which pins are polled.
