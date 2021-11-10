# lebai driver

Driver for robot controller and ros connection.
Connection services are classified into four types:

- **state** provides all the controller internal states, include io state, robot state, joint state, and gripper state.
- **io** provides io control interface and gripper control interface.
- **system** provides some system level interface.(enable, disable, etc.)
- **motion** provides motion control interface

# State

the node is **robot_state**

state send several robot state(joint state, io state, robot state, gripper state) to ROS by publishing.

- `/io_status`, topic type is `lebai_msgs/IOStatus`
- `/robot_status`, topic type is `lebai_msgs/RobotStatus`
- `/joint_states`, topic type is `sensor_msgs/JointState`
- `/gripper_states`, topic type is `lebai_msgs/GripperStatus`

**TODO:**

- `effort` in `joint_states` is not implemented.(gRPC problem)
- `force` in `gripper_states` is not implemented.(gRPC problem)
- `hold_on` in `gripper_status` should be documented more explicit.
- maybe `robot_status` should use some vendor specified dat.(Do not use industrial_msgs's data) 

# io

the node is **io_service**
Currently, io provides following services:

- `/io_service/set_robot_do` type is `lebai_msgs/SetDO`
- `/io_service/set_robot_ao, service`, type is `lebai_msgs/SetAO`
- `/io_service/set_robot_ao_mode` type is `lebai_msgs/SetAMode`
- `/io_service/set_robot_ai_mode` type is `lebai_msgs/SetAMode`
- `/io_service/set_flange_do` type is `lebai_msgs/SetDO`
- `/io_service/set_gripper_position` type is `lebai_msgs/SetGripper`
- `/io_service/set_gripper_force` type is `lebai_msgs/SetGripper`

# system

the node is **system_service**
Currently, system provides following services:

- `/system_service/emergency_stop`
- `/system_service/enable`
- `/system_service/disable`
- `/system_service/entry_teach_mode`
- `/system_service/exit_teach_mode`
- `/system_service/pause_motion`
- `/system_service/abort_motion`
- `/system_service/resume_motion`
- `/system_service/power_off`
- `/system_service/power_on`
- `/system_service/turn_off_robot`

 all the services are typed `std_srvs/Empty`

# motion

the node are **motion_service**
Currently, motion provides following services:

- `/motion_service/move_circle`, service type is `lebai_msgs/MoveCircle`
- `/motion_service/move_joint`, service type is `lebai_msgs/MoveJoint`
- `/motion_service/move_circle`, service type is`lebai_msgs/MoveCircle`

 **TODO:**

- `Until` function in all the `MoveXXX` is not working.

