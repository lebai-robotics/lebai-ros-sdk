Lebai ROS2 SDK
===============

``lebai-ros-sdk`` is being refactored into a ROS2-only driver project. Runtime
nodes are Python, controller access goes through released ``pylebai``, and the
ROS interface definitions stay in a small ``ament_cmake`` package.

Phase 1 covers the core SDK categories: ``start_stop``, ``motion``, ``status``,
``io``, ``claw``, ``discovery``, and standalone ``gripper``.

.. toctree::
   :maxdepth: 2

   install
   quickstart
   architecture
   interfaces/topics
   interfaces/services
   migration
   roadmap
   agent-guide
