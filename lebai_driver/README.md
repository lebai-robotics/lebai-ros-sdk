# lebai driver

Driver for robot controller and ros connection.
There are  four connection nodes:

- **robot_state** provides all the controller internal states, include io state, robot state, joint state, and gripper state.
- **io_service** provides io control interface and gripper control interface.
- **system_service** provides some system level interface.(enable, disable, etc.)
- **motion** provides motion control interface

# robot_state

## Published Topics

* **`robot_status`** (`lebai_interfaces/msg/RobotStatus`)
* **`joint_states`** (`sensor_msgs/msg/JointState`)
* **`io_status`** (`lebai_interfaces/msg/IOStatus`)

# io_service

## service servers

- **`/io_service/set_extend_ao`** (`lebai_interfaces/srv/SetAO`)
- **`/io_service/set_extend_do`** (`lebai_interfaces/srv/SetDO`)
- **`/io_service/set_flange_do`** (`lebai_interfaces/srv/SetDO`)
- **`/io_service/set_robot_ai_mode`** (`lebai_interfaces/srv/SetAMode`)
- **`/io_service/set_robot_ao`** (`lebai_interfaces/srv/SetAO`)
- **`/io_service/set_robot_ao_mode`** (`lebai_interfaces/srv/SetAMode`)
- **`/io_service/set_robot_do`** (`lebai_interfaces/srv/SetDO`)

# system_service

## service servers

- **`/io_service/set_extend_ao`** (`lebai_interfaces/srv/SetAO`)

- **`/system_service/abort_motion`** (`std_srvs/srv/Empty`)
- **`/system_service/emergency_stop`** (`std_srvs/srv/Empty`)
- **`/system_service/enable`** (`std_srvs/srv/Empty`)
- **`system_service/entry_teach_mode`** (`std_srvs/srv/Empty`)
- **`/system_service/exit_teach_mode`**(`std_srvs/srv/Empty`)
- **`/system_service/pause_motion`**(`std_srvs/srv/Empty`)
- **`/system_service/power_off`** (`std_srvs/srv/Empty`)
- **`/system_service/power_on`** (`std_srvs/srv/Empty`)
- **`/system_service/resume_motion`** (`std_srvs/srv/Empty`)
- **`/system_service/turn_off_robot`** (`std_srvs/srv/Empty`)

# motion

## service servers

- **`/motion_service/move_joint`** (`lebai_interfaces/srv/MoveJoint`)
- **`/motion_service/move_line`** (`lebai_interfaces/srv/MoveLine`)

## action servers

- **`/lebai_trajectory_controller`** (`control_msgs/action/FollowJointTrajectory`)

