**This document describe `lebai-ros-sdk` on ROS Melodic(Ubuntu 18.04)**

If you use `ROS` noedic, please refer here.

# Prerequsite

As a ROS package, you need firstly install `ROS` .

1. Install `ROS` follow the official guide(`ros-melodic-desktop-full` is sugguested).
   
2. Also we need some extra `ROS` packages:

   ```
   sudo apt install -y ros-melodic-industrial-msgs ros-melodic-grpc
   ```


# Get the `lebai-ros-sdk` from src

checkout out package and run `catkin_make`

```bash
cd ~/catkin_ws/src
git clone git@github.com:lebai-robotics/lebai-ros-sdk.git -b melodic-dev
cd ~/catkin_ws
catkin_make
```

# How to run

To connect a real `lebai` robot, you must have a `lebai` `l-master`  running with network access.

## Run driver without gui display (lm3 as an example)

```
roslaunch lebai_lm3_support robot_interface_lm3.launch robot_ip:=your_robot_ip has_gripper:=0
```

`robot_ip` is the robot's physical IP address.

`has_gripper ` decide whether gripper is mounted on the end.

## Run driver with gui display (lm3 as an example)

```
roslaunch lebai_lm3_support robot_interface_lm3_with_visual.launch robot_ip:=your_robot_ip has_gripper:=0
```

`robot_ip` is the robot's physical IP address.

`has_gripper ` depends on whether gripper is mounted on the end.



## Connect lm3 with MoveIt

Coming soon...