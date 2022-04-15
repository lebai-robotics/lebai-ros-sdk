cmake_minimum_required(VERSION 3.0.2)
project(lebai_tutorials)

find_package(catkin REQUIRED COMPONENTS
  lebai_msgs
  rospy
  roscpp
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES lebai_tutorials
#  CATKIN_DEPENDS lebai_msgs rospy
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

# move_example node
add_executable(move_example
  src/move_example
)
target_link_libraries(move_example
  ${catkin_LIBRARIES}
)
#set_target_properties(move_example
#  PROPERTIES OUTPUT_NAME move_example
#  PREFIX "")
add_dependencies(move_example lebai_msgs_generate_messages_cpp)


#############
## Install ##
#############

install(TARGETS move_example
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS scripts/io_example.py scripts/move_example.py scripts/robot_state.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
  