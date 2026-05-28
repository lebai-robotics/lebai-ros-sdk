# lebai_driver

ROS2 Python runtime package for Lebai controllers, backed by released
`pylebai`.

Phase 1 provides typed ROS services and topics for:

- `start_stop`
- `motion`
- `status`
- `io`
- `claw`
- `discovery`
- standalone `gripper`

Launch files:

- `driver.launch.py`
- `discovery.launch.py`
- `serial_gripper.launch.py`

The old ROS1/C++ runtime, old service names, and action surface are removed
from the active ROS2 driver path.
