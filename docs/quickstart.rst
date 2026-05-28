Quickstart
==========

Driver Node
-----------

Start the main robot driver under the default ``/lebai`` namespace:

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_ip:=127.0.0.1 simulator:=true

For a real controller, pass the controller IP and set ``simulator:=false`` or
omit it.

Discovery Node
--------------

Start controller discovery:

.. code-block:: bash

   ros2 launch lebai_driver discovery.launch.py

Resolve controllers:

.. code-block:: bash

   ros2 service call /lebai/discovery/resolve lebai_interfaces/srv/ResolveControllers

Standalone Gripper Node
-----------------------

Start the pylebai serial gripper node:

.. code-block:: bash

   ros2 launch lebai_driver serial_gripper.launch.py port_name:=/dev/ttyUSB0

Examples
--------

After launching the driver, run Python examples:

.. code-block:: bash

   ros2 run lebai_tutorials move_example.py
   ros2 run lebai_tutorials io_example.py
   ros2 run lebai_tutorials joint_state_subscriber.py

Common Topic Checks
-------------------

.. code-block:: bash

   ros2 topic echo /lebai/status/robot
   ros2 topic echo /lebai/status/joint_states
   ros2 topic echo /lebai/io/state

Common Service Checks
---------------------

.. code-block:: bash

   ros2 service call /lebai/motion/get_running_motion lebai_interfaces/srv/GetRunningMotion
   ros2 service call /lebai/start_stop/start_sys lebai_interfaces/srv/Command
