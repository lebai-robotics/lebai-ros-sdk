Install
=======

Supported Branches
------------------

The active refactor target is ROS2 Humble on Ubuntu 22.04:

.. code-block:: text

   humble-dev

ROS2 Jazzy on Ubuntu 24.04 is planned as a separate distro branch. ROS1 and the
old 20.04 ROS2 branch are kept as historical code and are not part of the new
runtime refactor.

Workspace Setup
---------------

Install ROS2 Humble, create a workspace, and clone this repository into
``src``:

.. code-block:: bash

   mkdir -p ~/lebai_ws/src
   cd ~/lebai_ws/src
   git clone https://github.com/lebai-robotics/lebai-ros-sdk.git
   cd ~/lebai_ws

Install Python and ROS dependencies:

.. code-block:: bash

   source /opt/ros/humble/setup.bash
   python3 -m pip install pylebai
   rosdep update
   rosdep install --from-paths src --ignore-src --rosdistro humble -y --skip-keys pylebai

Build the active packages:

.. code-block:: bash

   colcon build --packages-select lebai_interfaces lebai_driver lebai_tutorials --symlink-install
   source install/setup.bash

Package Roles
-------------

``lebai_interfaces``
   Generates phase-1 messages and services.

``lebai_driver``
   Provides Python ROS2 nodes backed by ``pylebai``.

``lebai_tutorials``
   Provides Python examples for the new API.
