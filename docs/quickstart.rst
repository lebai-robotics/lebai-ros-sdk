Quickstart
==========

Driver
------

Source the workspace environment and launch the driver. Replace
``192.168.1.104`` with your controller's IP address.

.. code-block:: bash

   roslaunch lebai_driver driver.launch robot_ip:=192.168.1.104

Set ``simulator:=true`` to connect to a running simulator controller. Use the
simulator host's reachable address. This example uses a local simulator.

.. code-block:: bash

   roslaunch lebai_driver driver.launch robot_ip:=127.0.0.1 simulator:=true

From a second terminal, read the connection and joint state.

.. code-block:: bash

   rostopic echo -n 1 /lebai/status/robot
   rostopic echo -n 1 /lebai/status/joint_states

When ready to enable the robot for motion, call ``start_sys`` and check
``result.success``.

.. code-block:: bash

   rosservice call /lebai/start_stop/start_sys '{}'

Driver launch arguments
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Argument
     - Default
     - Purpose
   * - ``robot_ip``
     - ``127.0.0.1``
     - Robot or simulator controller host.
   * - ``simulator``
     - ``false``
     - Select simulator mode in the Python SDK.
   * - ``namespace``
     - ``lebai``
     - Namespace for relative topics, services, and nodes.
   * - ``joint_names``
     - ``[joint_1, joint_2, joint_3, joint_4, joint_5, joint_6]``
     - Six arm joint names in controller order.
   * - ``trajectory_action_name``
     - ``/lebai_trajectory_controller``
     - Arm action name.
   * - ``gripper_action_name``
     - ``/lebai_gripper_controller/gripper_cmd``
     - Integrated claw action name.
   * - ``joint_state_publish_rate``, ``joint_motion_publish_rate``
     - ``20.0`` Hz each
     - Arm and model joint states, and joint motion status.
   * - ``robot_state_publish_rate``, ``io_state_publish_rate``, ``gripper_state_publish_rate``
     - ``10.0`` Hz each
     - Robot status, I/O state, and integrated claw state and joint state.
   * - ``gripper_joint_name``
     - ``gripper_r_joint1``
     - Active joint used by the integrated claw's model.
   * - ``io_state_device``
     - ``robot``
     - Device read by the I/O status publisher.
   * - ``io_state_digital_input_count``, ``io_state_digital_output_count``,
       ``io_state_analog_input_count``, ``io_state_analog_output_count``,
       ``io_state_dio_count``
     - ``0`` each
     - Number of pins to read per I/O group, starting at pin 0. A zero count
       leaves the corresponding status array empty.
   * - ``publish_robot_description``
     - ``true``
     - Load the model in the driver namespace and launch its state publisher.
   * - ``robot_model``
     - ``lm3_with_gripper.xacro``
     - Model file from ``lebai_lm3_support/urdf``.

Publish rates must be positive. See :doc:`architecture` for action name
overrides and concurrency behavior.

Discovery
---------

The discovery node can run independently of the robot driver. Its
``namespace`` argument defaults to ``lebai``.

.. code-block:: bash

   roslaunch lebai_driver discovery.launch
   # In another sourced terminal
   rosservice call /lebai/discovery/resolve '{}'

Serial gripper
--------------

Launch the serial gripper node with the device path for the attached gripper.
Its ``port_name`` defaults to ``/dev/ttyUSB0``, ``namespace`` to ``lebai``,
and ``gripper_state_publish_rate`` to ``10.0`` Hz.

.. code-block:: bash

   roslaunch lebai_driver serial_gripper.launch port_name:=/dev/ttyUSB0
   # In another sourced terminal
   rostopic echo -n 1 /lebai/gripper/state

The serial node exposes its own ``gripper/*`` interfaces. The robot driver's
``claw/*`` interfaces address the claw integrated with the robot controller.
