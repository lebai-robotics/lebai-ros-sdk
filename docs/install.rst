Installation
============

Use ROS Noetic on Ubuntu 20.04 with Python 3.8 and
``pylebai>=2.0.8,<3``. Python 2 is unsupported. This is a breaking release.
See :doc:`architecture` when updating existing clients.

With ROS Noetic installed, install the Python SDK into the Python 3.8
environment that will run the ROS nodes. Do this before building the Catkin
workspace.

.. code-block:: bash

   sudo apt install python3-pip
   python3 -m pip install --user 'pylebai>=2.0.8,<3'

Place the checkout of this release in ``~/catkin_ws/src/lebai-ros-sdk``.
Initialize rosdep with ``sudo rosdep init`` if your Noetic installation has
not initialized it yet. Install the remaining dependencies and build from
the workspace root.

.. code-block:: bash

   source /opt/ros/noetic/setup.bash
   cd ~/catkin_ws
   rosdep update --include-eol-distros
   rosdep install --from-paths src --ignore-src --rosdistro noetic --skip-keys pylebai -y
   catkin_make
   source devel/setup.bash

Source ``~/catkin_ws/devel/setup.bash`` in each terminal used to run the
driver, examples, or MoveIt. Continue with :doc:`quickstart`.

Building this guide
-------------------

Install the documentation dependencies and build from the repository root.
The build treats Sphinx warnings as errors and writes the site to
``docs/build/html/``. Open ``docs/build/html/index.html`` in a browser.

.. code-block:: bash

   python3 -m pip install --user -r docs/requirements.txt
   ./scripts/build-docs.sh
