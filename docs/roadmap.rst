Roadmap
=======

Phase 1
-------

Current phase-1 scope:

- ``start_stop``
- ``motion`` services
- ``status`` topics
- ``io`` services and state topic
- ``claw`` services and state topic
- ``discovery`` service
- standalone ``gripper`` services and state topic
- Humble CI with unit tests and simulator smoke tests
- versioned GitHub Pages documentation

Later Phases
------------

Planned areas after the core driver stabilizes:

- Motion actions for long-running motion workflows.
- MoveIt configuration redesign.
- Additional SDK categories: ``config``, ``file``, ``modbus``, ``serial``,
  ``storage``, ``program``/``scene``, ``robotics``, ``led``, and ``signal``.
- Jazzy branch support on Ubuntu 24.04.
- Future ROS2 distribution branch for Ubuntu 26.04.

Compatibility Policy
--------------------

Each active ROS2 distribution should have its own branch. Branches may share the
same public API where practical, but distro-specific dependency and packaging
differences should stay isolated.
