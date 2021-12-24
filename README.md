**This document describe `lebai-ros-sdk` on ROS Melodic(Ubuntu 18.04)**

If you use `ROS` noetic, please refer [noetic-dev](https://github.com/lebai-robotics/lebai-ros-sdk/tree/noetic-dev) branch.

# Prerequsite

As a ROS package, you need firstly install `ROS` .

1. Install `ROS` follow the official guide(`ros-melodic-desktop-full` is sugguested).
   
2. Also we need some extra `ROS` packages:

   ```
   sudo apt install -y ros-melodic-industrial-robot-client ros-melodic-industrial-robot-simulator ros-melodic-grpc 
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

If you connect your `ROS` device to the `lebai WIFI`, usually the network gateway(`10.20.17.1`)  address is the robot Ip address.

Once the driver started to run, you can get access to the robot controller via `ROS` `pubsub` and `service`. See [lebai_driver](lebai_driver/README.md) for more detailed information.

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

## Connect with MoveIt (lm3 as an example)

Install `MoveIt` firstly.

```
sudo apt install -y ros-melodic-moveit
```

Then, run the following:

```
# simulation mode
roslaunch lebai_lm3_moveit_config run.launch
# connection to real robot
roslaunch lebai_lm3_moveit_config run.launch sim:=false robot_ip:=your_robot_ip
```

`sim` set to true will not connect to real robot. it will only run a simulation

`robot_ip` is the robot's physical IP address, if `sim` set to false, `robot_ip` is required.  

**Note**:

Before using `MoveIt` to move the manipulator, make sure the robot is enabled, there are two methods:

in `ROS`:

```
rosservice call /system_service/enable "{}"
```

in `l-master` web, click the startup(启动) as show in the following fig:

![](lebai_doc/enable_robot_on_website.png)