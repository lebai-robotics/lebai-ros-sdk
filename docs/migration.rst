Migration
=========

This refactor is intentionally a breaking ROS API change.

What Changed
------------

- ROS1 support is not part of active branches.
- C++ runtime driver code has been removed from the active driver path.
- Runtime controller access now uses released ``pylebai``.
- Old service and topic names are not preserved.
- Motion actions are deferred; phase 1 uses services.
- MoveIt configuration remains present but is deferred for redesign.

Old Package Concepts
--------------------

The old runtime split used categories such as ``robot_state``, ``io_service``,
``system_service``, and ``motion``. The new API follows the SDK categories
instead:

.. list-table::
   :header-rows: 1

   * - Old concept
     - New category
   * - ``system_service``
     - ``start_stop``
   * - ``motion``
     - ``motion``
   * - ``robot_state``
     - ``status``
   * - ``io_service``
     - ``io`` and ``claw``
   * - standalone gripper package
     - ``gripper`` through ``pylebai``

Migration Checklist
-------------------

1. Replace old service names with the new ``/lebai/<sdk-category>/...`` paths.
2. Replace old message and service types with the phase-1
   ``lebai_interfaces`` types.
3. Replace action clients with service calls for phase 1.
4. Use ``CartesianPose`` fields ``x``, ``y``, ``z``, ``rx``, ``ry``, ``rz``
   instead of ``geometry_msgs/Pose`` for SDK-style Cartesian data.
5. Move direct gripper serial code to the standalone gripper node where
   supported by released ``pylebai``.
