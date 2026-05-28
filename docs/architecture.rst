Architecture
============

Package Boundary
----------------

``lebai_driver`` is the only active runtime package. It is an ``ament_python``
package and contains no C++ driver implementation. It owns ROS nodes, parameter
declarations, service registration, status publishers, and conversion helpers.

``lebai_interfaces`` is intentionally small and remains ``ament_cmake`` because
ROS2 message and service generation is normally handled by CMake packages.

Runtime Nodes
-------------

``driver``
   Creates one ``pylebai.Robot`` connection and registers status publishers plus
   ``start_stop``, ``motion``, ``io``, and ``claw`` services.

``discovery``
   Uses ``pylebai.zeroconf.Discovery`` and exposes controller discovery as a
   typed ROS service.

``serial_gripper``
   Uses the released ``pylebai.gripper.Gripper`` API for standalone serial
   grippers.

The main driver node keeps one connection wrapper and delegates category
registration to focused modules:

.. code-block:: text

   connection.py
   start_stop_services.py
   motion_services.py
   io_services.py
   claw_services.py
   status.py
   discovery_node.py
   serial_gripper_node.py
   conversions.py

Error Contract
--------------

Service responses include ``lebai_interfaces/msg/Result``:

.. code-block:: text

   bool success
   int32 code
   string message

SDK exceptions are mapped to ``success=false`` with the exception message.
Unsupported methods are reported with a non-zero code.

State Model
-----------

Continuously useful state is published as topics. Commands and request/response
queries are services. ROS actions are deferred until a later motion-control
phase.
