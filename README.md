# lebai-ros-sdk
Lebai ros sdk for controlling the robot via ROS

# Prerequsite

As a ROS Industrial package, you need firstly install `ROS` && `ROS Industrial`.

**Now we can only work on `Ros Melodic`(`Ubuntu 18.04`) version, runnning on other `ROS` distribution is possible, but we never tested.**

1. Install `ROS` follow official guide.

2. Install `ROS` Industrial.

   ```sudo apt install ros-melodic-industrial-robot-client```

3. If you want to play with `MoveIt`, you need to install `MoveIt` package(optional)

   ```sudo apt install ros-melodic-moveit```

# Install lebai-ros-sdk

Download deb package from the release section

```shell
sudo apt install lebai-ros-sdk-0.1.deb
```

The sdk files will be installed under `/opt/lebai/ros` folder

# Configuration
The configuration is different that depends on what type of shell you use, the following will introduct the common used shells: `bash` and `zsh`.
For the `Bash` and `ZSH` sections, you should choose the correct shell type.

## Bash

```shell
echo "source /opt/lebai/ros/setup.bash" >> ~/.bashrc
```

## ZSH
```shell
echo "source /opt/lebai/ros/setup.zsh" >> ~/.zshrc
```

Then close current terminal and reopen again, then you are ready to go.

# How to run

To connect a real lebai robot, you must have a lebai robot controller running with network access.

## Run driver without gui display (lm3 as an example)

```
roslaunch lebai_lm3_support robot_interface_lm3.launch robot_ip:=<robot_ip>
```

`robot_ip` is the robot's physical IP address.

## Run MoveIt application (lm3 as an example)

First, you need to install `MoveIt`:

```
sudo apt install ros-melodic-moveit
```

Then, run as following:

```
# simulation mode
roslaunch lebai_lm3_moveit_config run.launch
# connection to real robot
roslaunch lebai_lm3_moveit_config run.launch sim:=false robot_ip:=<robot_ip>
```

`sim` set to true will not connect to real robot. otherwise it will only run a moveit simulation

`robot_ip` is the robot's physical IP address, if `sim` set to false, `robot_ip` is required.

## Ros basic
As the common usage of ros commands, you can use `rostopic` or `rosservice` to query the states or control the robot.

## Python support
Currently only support `python 2`.

You can check the python samples under `lib/lebai_tutorials` folder.



