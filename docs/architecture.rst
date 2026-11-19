Driver architecture and migration
=================================

The driver uses a shared ``pylebai.Robot`` connection for driver services,
status topics, and controller actions. Controller discovery and the serial
gripper run as separate nodes. With the default launch namespace, relative
topics and services appear under ``/lebai``. See :doc:`interfaces/topics`
and :doc:`interfaces/services` for the ROS graph.

Actions
-------

The robot driver hosts two ROS 1 action servers.

.. list-table::
   :header-rows: 1

   * - Default action name
     - Type
     - Driver launch argument
   * - ``/lebai_trajectory_controller``
     - ``control_msgs/FollowJointTrajectoryAction``
     - ``trajectory_action_name``
   * - ``/lebai_gripper_controller/gripper_cmd``
     - ``control_msgs/GripperCommandAction``
     - ``gripper_action_name``

The defaults are absolute. To run multiple drivers on one ROS master, give
each a distinct namespace and distinct absolute action names. Configure each
action client to use the corresponding action name.

.. code-block:: bash

   roslaunch lebai_driver driver.launch namespace:=arm_a robot_ip:=192.168.1.104 \
     trajectory_action_name:=/arm_a/trajectory \
     gripper_action_name:=/arm_a/gripper_cmd

The trajectory action expects the six configured arm joint names in order
and at least two points. Every point supplies six positions, velocities, and
accelerations, with strictly increasing ``time_from_start``. The first
point supplies the initial time for the segment durations. The gripper
action maps a commanded joint position from ``0`` to ``pi/3`` radians to
claw amplitude from ``0`` to ``100`` percent. A nonpositive
``max_effort`` selects a force value of ``100``.

Concurrency limits
------------------

Direct action goals use independent workers. Goals can overlap with other
goals, service calls, and status reads on the same SDK connection. Sending a
new direct goal does not preempt an earlier one. A trajectory cancellation
calls the controller's ``stop_move`` and can affect other active motion.
Coordinate direct actions, MoveIt execution, and motion services at the
client level so that only one source commands arm motion at a time.

The ``/lebai/motion/wait_move`` service holds the shared service/status gate
until the blocking SDK call returns. Other driver services, including
``/lebai/motion/stop_move``, wait for the gate, and status publishers skip
updates during this time. The ROS service has no server-side timeout for the
SDK wait. Use short ``/lebai/motion/get_motion_state`` queries when clients
need status updates or other driver services to remain responsive.

Migrating existing Noetic clients
---------------------------------

This is a breaking release. Update message imports, ROS names, and request
and response handling together.

.. BEGIN LEGACY MIGRATION

.. list-table::
   :header-rows: 1

   * - Previous interface
     - Noetic replacement
   * - ``lebai_driver/robot_interface.launch``
     - ``lebai_driver/driver.launch``.
   * - ``lebai_msgs`` messages and services
     - Use ``lebai_interfaces`` with the new definitions. Check each response's
       ``result`` for success, code, and message.
   * - ``/joint_states``, ``/robot_status``, ``/io_status``, ``/gripper_status``
     - ``/lebai/status/joint_states``, ``/lebai/status/robot``,
       ``/lebai/io/state``, and ``/lebai/claw/state``, respectively.
   * - ``/system_service/enable`` and ``/system_service/disable`` using
       ``std_srvs/Empty``
     - ``/lebai/start_stop/start_sys`` and ``/lebai/start_stop/stop_sys``
       using ``lebai_interfaces/Command``.
   * - ``/motion_service/move_joint`` and ``/motion_service/move_line``
     - ``/lebai/motion/movej`` and ``/lebai/motion/movel``, respectively.
       Send the new motion target and parameter fields.
   * - ``/io_service/set_robot_do``, ``/io_service/set_flange_do``, or
       ``/io_service/set_robot_ao``
     - Call ``/lebai/io/set_do`` or ``/lebai/io/set_ao`` with an explicit
       ``device`` and ``pin``.
   * - ``/io_service/set_gripper_position`` and ``/io_service/set_gripper_force``
     - For the integrated claw, send both ``force`` and ``amplitude`` to
       ``/lebai/claw/set_claw``.
   * - ``lebai_lm3_moveit_config/real_robot.launch``
     - ``lebai_lm3_moveit_config/lm3.launch`` with the appropriate
       ``has_gripper`` value.
   * - ``/joint_trajectory_action``
     - ``/lebai_trajectory_controller`` uses
       ``control_msgs/FollowJointTrajectoryAction``.

.. END LEGACY MIGRATION
