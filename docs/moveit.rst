MoveIt 1 for LM3
================

This release provides MoveIt 1 configuration for LM3. Choose the launch
mode that matches the arm's tooling. Replace the example IP with the robot
controller address.

.. code-block:: bash

   roslaunch lebai_lm3_moveit_config lm3.launch has_gripper:=true robot_ip:=192.168.1.104
   roslaunch lebai_lm3_moveit_config lm3.launch has_gripper:=false robot_ip:=192.168.1.104

``has_gripper:=true`` is the default. It loads the arm and gripper model,
configures the ``manipulator`` and ``gripper`` groups, and consumes
``/lebai/model/joint_states``. The gripper group commands
``gripper_r_joint1`` and the URDF derives its mimic joints. The arm-only
mode loads the ``manipulator`` group and consumes
``/lebai/status/joint_states``.

``lm3.launch`` starts the driver and RViz by default. Set
``use_rviz:=false`` for a headless run. To connect to a running simulator,
pass ``simulator:=true`` and use the simulator controller address as
``robot_ip`` (default ``127.0.0.1``).

If a driver is already running, set ``launch_driver:=false``. The default
MoveIt configuration expects the driver's ``/lebai`` joint state paths and
absolute controller action names. If you override an action name on the
driver, update the corresponding controller's ``name`` and ``action_ns`` in
``lebai_lm3_moveit_config/config/controllers.yaml`` for gripper mode or
``lebai_lm3_moveit_config/config/controllers_arm_only.yaml`` for arm-only mode
so their combined path matches the override.

Enable the robot for execution with ``/lebai/start_stop/start_sys``. The
arm tutorial supports both modes, and the gripper amplitude tutorial
requires ``has_gripper:=true``. See :doc:`examples` for the commands.
