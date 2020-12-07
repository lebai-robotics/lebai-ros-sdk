# lebai driver

Driver for robot controller and ros connection.
Connection services are classified into four types:

- **motion** provides motion control interface
- **io** provides io control interface and gripper control interface.
- **system** provides some system level interface.(enable, disable, etc.)
- **state** provides all the controller internal states, include io state, robot state, joint state, and gripper state.

# motion

the node are **motion_service**
Currently, motion provides following services:

- `/motion_service/move_circle`, service type is `lebai_msgs/MoveCircle`
- `/motion_service/move_joint`, service type is `lebai_msgs/MoveJoint`
- `/motion_service/move_circle`, service type is`lebai_msgs/MoveCircle`
- `/stop_motion`, service type is `industrial_msgs/StopMotion`

Motion subscribes a topic `/joint_path_command`,message type is `trajectory_msgs/JointTrajectory`

Motion contains a action server `/joint_trajectory_action`

# io

the node is **io_service**
Currently, io provides following services.

- `/io_service/set_robot_do` type is `lebai_msgs/SetDO`
- `/io_service/set_robot_ao, service`, type is `lebai_msgs/SetAO`
- `/io_service/set_robot_ao_mode` type is `lebai_msgs/SetAMode`
- `/io_service/set_robot_ai_mode` type is `lebai_msgs/SetAMode`
- `/io_service/set_flange_do` type is `lebai_msgs/SetDO`
- `/gripper_service/set_gripper_position` type is `lebai_msgs/SetGripper`
- `/gripper_service/set_gripper_force` type is `lebai_msgs/SetGripper`



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

# State

the node is **robot_state**

state send several robot state(joint state, io state, robot state) to ROS by publishing.

- `/io_status`, topic type is `lebai_msgs/IOStatus`
- `/robot_status`, topic type is `lebai_msgs/RobotStatus`
- `/joint_states`, topic type is `sensor_msgs/JointState`
- `/gripper_states`, topic type is `lebai_msgs/GripperStatus`

 









