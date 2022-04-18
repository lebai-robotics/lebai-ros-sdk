cmake_minimum_required(VERSION 2.8.3)
project(lebai_msgs)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  genmsg
  industrial_msgs
  message_generation
  message_runtime
  std_msgs
  trajectory_msgs
  geometry_msgs
)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  # ExecuteMode.msg
  IOStatus.msg 
  GripperStatus.msg 
  IOConditionalExpress.msg
  UntilInfo.msg  
  MoveCommon.msg
  #MoveLine.msg
  #MoveJoint.msg  
  #MoveCircle.msg
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  SetDO.srv
  SetAO.srv
  SetAMode.srv
  MoveJoint.srv
  MoveLine.srv
  MoveCircle.srv
  SetGripper.srv
)

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  industrial_msgs
  trajectory_msgs
  std_msgs
  geometry_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES lebai_msgs
  CATKIN_DEPENDS industrial_msgs std_msgs trajectory_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)

