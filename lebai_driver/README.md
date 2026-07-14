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

Endpoints owned by the Lebai driver nodes are relative to their node namespace.
With the default `/lebai` namespace, the main `lebai_driver` node publishes:

- `/lebai/status/robot`
- `/lebai/status/joint_states`
- `/lebai/status/joint_motion`
- `/lebai/model/joint_states`
- `/lebai/io/state`
- `/lebai/claw/state`
- `/lebai/claw/joint_states`

The standalone serial gripper node publishes `/lebai/gripper/state`. By default,
`driver.launch.py` also starts a namespaced `robot_state_publisher`, which
publishes the transient-local `std_msgs/msg/String` description topic
`/lebai/robot_description` and uses the standard global `/tf` and `/tf_static`
transports. The description topic is absent when
`publish_robot_description:=false`. The complete service and topic inventories
are maintained in the user documentation.

The two driver actions are also relative names:

- `lebai_trajectory_controller/follow_joint_trajectory`, resolved by default
  as `/lebai/lebai_trajectory_controller/follow_joint_trajectory`
- `lebai_gripper_controller/gripper_cmd`, resolved by default as
  `/lebai/lebai_gripper_controller/gripper_cmd`

The arm status and trajectory action use the fixed joint names `joint_1`
through `joint_6`; they are not runtime-remappable.

Launch files:

- `driver.launch.py`
- `discovery.launch.py`
- `serial_gripper.launch.py`

Configuration list services use the SDK-aligned `/lebai/config/load_*`
taxonomy. The old ROS1/C++ runtime and legacy service names are removed from
the active ROS2 driver path.

IO requests still use strings because released `pylebai` does not yet expose
the coordinated typed enum. Use canonical uppercase SDK device names such as
`ROBOT` and `FLANGE`; unknown or lowercase values may fall back to `ROBOT` in
the SDK.
