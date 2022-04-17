**This document describe `lebai-ros-sdk` on `ROS2 Galactic`**

If you use `ROS melodic`, please refer [melodic-dev](https://github.com/lebai-robotics/lebai-ros-sdk/tree/melodic-dev) branch.

If you use `ROS noetic`, please refer [noetic-dev](https://github.com/lebai-robotics/lebai-ros-sdk/tree/noetic-dev) branch.

# Prerequsite

As a `ROS2` package, you need firstly install `ROS2` .

1. Install `ROS2 galactic`  follow [official guide](https://docs.ros.org/en/galactic/Installation.html).
   
2. Install some `ROS2` dependency packages.

   ```
   sudo apt install ros-galactic-control-msgs ros-galactic-moveit
   ```

3. Now the communication to real `lebai` robot in `lebai-ros-sdk `  is written in python, based on the [`lebai-python-sdk`](https://github.com/lebai-robotics/lebai-python-sdk), So we need install it.

   ```
   ### lebai sdk
   pip install lebai
   
   ### If pip3 is not install, install it by apt
   sudo apt install python3-pip
   ```

4. If you want to play with `MoveIt2`, please install it by following the [official guide](https://moveit.picknik.ai/galactic/doc/tutorials/getting_started/getting_started.html#).


# Get `lebai-ros-sdk`

checkout out package and run `colcon build`

```bash
cd ~/lebai_ws/src
git clone git@github.com:lebai-robotics/lebai-ros-sdk.git -b galactic-dev
cd ~/lebai_ws
colcon build
```

After build the `lebai-ros-sdk`, **do not forget to source the enviroment file.**

```
source ~/lebai_ws/install/setup.bash
```



# Unit Test

# How to run

To connect a real `lebai `robot, you must have a `lebai` robot controller running with network access.

If you connect your `ROS2` device to the `lebai WIFI`, usually the network gateway(`10.20.17.1`) address is the robot's physical IP address.

Once the driver started to run, you can get access to the robot controller via `ROS2` `pub&&sub` , `service`and `action`. See [lebai_driver](lebai_driver/README.md) for elaborated information.

## Run driver(`lm3` as an example)

```
### Do not forget the source before running.
### source ~/lebai_ws/install/setup.bash

ros2 launch lebai_lm3_support robot_interface_lm3.launch.py robot_ip:=your_robot_ip has_gripper:=false rviz2:=false
```

`robot_ip` is the robot's physical IP address.

`has_gripper ` depends on whether gripper is mounted on the end. Default to false.

`rviz2` set to launch a simple `rviz2` display GUI. Default to false.

## Connect `lm3` with `MoveIt2`

```
ros2 launch lebai_lm3_moveit_config lm3.launch.py robot_ip:=your_robot_ip
```

`robot_ip` is the robot's physical IP address.

**Note**: 

Now, we can only control `lm3` manipulator from `MoveIt2`. Gripper control is not implemented yet(coming soon).

Before using `MoveIt2` to move the manipulator, make sure the robot is enabled, there are two methods:

in `ROS2`:

```
ros2 service call /system_service/enable std_srvs/srv/Empty "{}"
```

in `l-master` web, click the startup(启动) as show in  the following fig:

<img src="lebai_doc/enable_robot_on_website.png" alt="enable_robot_on_website" style="zoom: 33%;" />

