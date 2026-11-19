# Python tutorials

Build and source the Noetic workspace, then start the driver or LM3 MoveIt stack as described in the [quickstart](../docs/quickstart.rst) and the [MoveIt 1 guide](../docs/moveit.rst).

| Script | Interface |
| --- | --- |
| `joint_state_subscriber.py` | Subscribe to the arm joint states |
| `io_example.py` | Set a digital or analog output |
| `move_example.py` | Send a joint or Cartesian target to the driver |
| `moveit_manipulator_example.py` | Plan for the LM3 arm in either gripper mode and optionally execute |
| `moveit_gripper_amplitude_example.py` | Send a claw amplitude to the LM3 controller action. Requires `has_gripper:=true`. |

See the [tutorial commands and inputs](../docs/examples.rst).
