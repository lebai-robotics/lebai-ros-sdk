**This document describe `lebai-ros-sdk` on ROS Noetic(Ubuntu 20.04)**

# Prerequsite

As a ROS package, you need firstly install `ROS` .

1. Install `ROS` follow official guide(ros-noetic-desktop-full is sugguested).

2. Now the communication to real robot in `lebai-ros-sdk `  is written in python, based on the [`lebai-python-sdk`](https://github.com/lebai-robotics/lebai-python-sdk), So we need install it.

   ```
   pip3 install lebai
   ```

3. The `lebai-ros-sdk` depends on `ROS Industrial`, Currently `ROS industrial` doesn't have debian package(Due to some dependencies are broken). So we need install it from source code as folow:

   ```
   cd ~/catkin_ws/src
   git clone https://github.com/ros-industrial/industrial_core.git 
   cd industrial_core
   # broken dependencies
   rm -rf industrial_trajectory_filters
   # try to run cakint_make to build it. It should success.
   cd ~/catkin_ws
   catkin_make
   ```

4. If you want to play with `MoveIt`, you need to install `MoveIt` package(optional)

   ```sudo apt install ros-noetic-moveit```



# Get the `lebai-ros-sdk`

checkout out package and run `catkin_make`

```bash
cd ~/catkin_ws/src
## TODO replace with github url
git clone git@github.com:lebai-robotics/lebai-ros-sdk.git -b noetic-dev
cd ~/catkin_ws
catkin_make
```

# Unit Test

All the python driver code is in package `lebai_driver`, it contains an unit test.

To run this unit test, you need to have a simulation rc-master running.

**You can use a real robot to run this test, but the test will cause the real robot moving, you must guarantee the move do not cause any damage yourself.**

Before you run the test, you need to set the robot ip of the simulation rc-master:

```
roscd lebai_driver/test
### edit the file test_lebai_driver.launch
### modify the robot_ip according  to real scene.
###
### <arg name="robot_ip" value="192.168.1.104" /> ###
###
```

Then, you can run the test

```
cd ~/catkin_ws/
catkin_make run_tests_lebai_driver
```

# How to run

To connect a real lebai robot, you must have a lebai robot controller running with network access.

## Run driver without gui display (lm3 as an example)

```
roslaunch lebai_lm3_support robot_interface_lm3.launch robot_ip:=your_robot_ip
```

`robot_ip` is the robot's physical IP address.

## Run dual robots

```
roslaunch lebai_lm3_support robot_interface_two_lm3.launch robot1_ip:=first_robot_ip robot2_ip:=second_robot_ip
```
