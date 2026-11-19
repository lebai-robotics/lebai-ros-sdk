Python tutorials
================

Source the workspace and launch the nodes from :doc:`quickstart` or
:doc:`moveit`. The examples below use the driver defaults. ROS name remapping
can point the service and topic examples at another namespace.

Read arm joint state
--------------------

``joint_state_subscriber.py`` subscribes to ``/lebai/status/joint_states``
with ``rospy.Subscriber`` and logs the joint names and positions.

.. code-block:: bash

   rosrun lebai_tutorials joint_state_subscriber.py

Set an output
-------------

``io_example.py`` calls ``/lebai/io/set_do`` or ``/lebai/io/set_ao`` through
``rospy.ServiceProxy`` and checks the service response. Choose the device,
pin, and output value for your controller. These examples write pin 0.

.. code-block:: bash

   rosrun lebai_tutorials io_example.py --device robot --pin 0 --digital 1
   rosrun lebai_tutorials io_example.py --device robot --pin 0 --analog 3.0

Send a direct motion request
----------------------------

``move_example.py`` uses ``/lebai/motion/movej`` for six joint positions in
radians or ``/lebai/motion/movel`` for a Cartesian pose in
``x,y,z,rx,ry,rz`` order. Supply a target appropriate for your robot and
workspace. This example sends a motion command without MoveIt planning.

.. code-block:: bash

   rosrun lebai_tutorials move_example.py --joints=-0.35,-1.0,1.2,-1.1,-0.6,0.0

The script prints the returned motion ID. Pass ``--wait`` to call the
blocking ``wait_move`` service. See :doc:`architecture` for its effect on
other driver operations.

Use MoveIt and the gripper controller
-------------------------------------

``moveit_manipulator_example.py`` uses the LM3 ``manipulator`` group through
``moveit_commander`` in either gripper mode. It plans by default. Add
``--execute`` to execute the planned trajectory.

.. code-block:: bash

   rosrun lebai_tutorials moveit_manipulator_example.py

``moveit_gripper_amplitude_example.py`` requires ``has_gripper:=true``.
It converts an amplitude percentage to the active gripper joint angle and
sends a goal directly to the gripper controller using
``actionlib.SimpleActionClient``. The command below moves the claw to 50
percent amplitude.

.. code-block:: bash

   rosrun lebai_tutorials moveit_gripper_amplitude_example.py --amplitude 50
