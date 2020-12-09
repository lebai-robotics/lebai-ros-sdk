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

## Clean
If you have installed `lebai-ros-sdk` before, please uninstall old version first.
```bash
sudo apt remove lebai-ros-sdk
```

## Installation

```bash
sudo apt install lebai-ros-sdk-0.2.deb
```

The sdk files will be installed under `/opt/lebai/ros` folder

# Configuration
The configuration is different that depends on what type of shell you use, the following will introduct the common used shells: `Bash` and `Zsh`.
For the `Bash` and `Zsh` sections, you should choose the correct shell type.

## Bash

```bash
echo "source /opt/lebai/ros/setup.bash" >> ~/.bashrc
```

## Zsh
```bash
echo "source /opt/lebai/ros/setup.zsh" >> ~/.zshrc
```

Then close current terminal and reopen again, then you are ready to go. 
You can use the following command to check whether it installed success or not.
```bash
rospack profile
```

```bash
Full tree crawl took 0.018217 seconds.
Directories marked with (*) contain no manifest.  You may
want to delete these directories.
To get just of list of directories without manifests,
re-run the profile with --zombie-only
-------------------------------------------------------------
0.016406   /opt/ros/melodic/share
0.001153 * /opt/ros/melodic/share/doc
0.001150   /opt/lebai/ros/share
0.001077 * /opt/ros/melodic/share/doc/eigenpy
0.000667 * /opt/ros/melodic/share/doc/eigenpy/doxygen-html
0.000277 * /opt/lebai/ros/share/common-lisp
0.000247 * /opt/lebai/ros/share/common-lisp/ros
0.000218 * /opt/lebai/ros/share/common-lisp/ros/lebai_msgs
0.000217 * /opt/lebai/ros/share/gennodejs
0.000213 * /opt/lebai/ros/share/roseus
0.000179 * /opt/lebai/ros/share/gennodejs/ros
0.000159 * /opt/lebai/ros/share/roseus/ros
0.000142 * /opt/lebai/ros/share/gennodejs/ros/lebai_msgs
0.000137 * /opt/ros/melodic/share/doc/eigenpy/doxygen-html/search
0.000122 * /opt/lebai/ros/share/roseus/ros/lebai_msgs
0.000042 * /opt/lebai/ros/share/common-lisp/ros/lebai_msgs/srv
0.000041 * /opt/ros/melodic/share/man
0.000030 * /opt/lebai/ros/share/common-lisp/ros/lebai_msgs/msg
0.000024 * /opt/lebai/ros/share/gennodejs/ros/lebai_msgs/srv
0.000021 * /opt/lebai/ros/share/roseus/ros/lebai_msgs/srv
```

If the result has the following line that means the installation was success:
```bash
0.001150   /opt/lebai/ros/share
```

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

The following commands and states are support:
- 
- I/O
  - RobotDI
  - RobotDO
  - RobotAI
  - RobotAO
  - FlangeDO
  - FlangeDI
- Motion
  - MoveJ
  - MoveL
  - MoveC
  - MovePVAT
- States
  - Joint states: pose, vel, torque
  - Robot Status
- Gripper (current support Lebai gripper only)
  - Position
  - Force
- System Cmds
  - PowerOn
  - PowerOff
  - Enable
  - Disable
  - PauseMotion
  - ResumeMotion
  - AbortMotion
  - EntryTeachMode
  - ExitTeachMode
  - TurnOff
  - EmergencyStop

**Notes**: Currently the ros sdk is under development and in preview state, so commands and api maybe change according to our refactor and update, please keep in mind that you know changes will be made in the future updates.

## Python support
Currently only support `python 2`.

You can check the python samples under `lib/lebai_tutorials` folder.



