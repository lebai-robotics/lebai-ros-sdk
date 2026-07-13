# lebai_driver

ROS2 Python runtime package for Lebai controllers, backed by released
`pylebai`.

The runtime provides typed ROS services, topics, and actions for:

- `start_stop`
- `motion`
- `status`
- `io`
- `led`
- `signal`
- `config`
- `claw`
- `discovery`
- standalone `gripper`

Launch files:

- `driver.launch.py`
- `discovery.launch.py`
- `serial_gripper.launch.py`

Configuration list services use the SDK-aligned `/lebai/config/load_*`
taxonomy. The old ROS1/C++ runtime and legacy service names are removed from
the active ROS2 driver path.
