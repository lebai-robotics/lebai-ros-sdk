cmake_minimum_required(VERSION 2.8.3)
project(lebai_driver)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  industrial_msgs
  lebai_msgs
  grpc
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES driver
  CATKIN_DEPENDS grpc roscpp control_msgs industrial_msgs sensor_msgs std_msgs trajectory_msgs urdf
  # LIBRARIES
#  DEPENDS system_lib
)

generate_proto(lebai_proto GRPC SRC_BASE "lebai-proto"
  FILES lebai-proto/robot_controller.proto lebai-proto/messages.proto
)


include_directories(
  ${catkin_INCLUDE_DIRS}
  include
  include/lebai_driver
)



# robot_state node
add_executable(${PROJECT_NAME}_robot_state
  src/robot_state/robot_state_node.cpp
  src/robot_state/robot_state_interface.cpp
  src/robot_state/joint_feedback_handler.cpp
  src/robot_state/io_status_handler.cpp
  src/robot_state/gripper_status_handler.cpp
  src/robot_state/robot_state_handler.cpp
)
target_link_libraries(${PROJECT_NAME}_robot_state
  ${catkin_LIBRARIES}
  lebai_proto
)
 
set_target_properties(${PROJECT_NAME}_robot_state
 PROPERTIES OUTPUT_NAME robot_state
 PREFIX "")
add_dependencies(${PROJECT_NAME}_robot_state lebai_msgs_generate_messages_cpp)

# io_service node
add_executable(${PROJECT_NAME}_io_service
  src/io_service/io_service_node.cpp
  src/io_service/io_service.cpp
)
target_link_libraries(${PROJECT_NAME}_io_service
  lebai_proto
  ${catkin_LIBRARIES}
)
set_target_properties(${PROJECT_NAME}_io_service
PROPERTIES OUTPUT_NAME io_service
PREFIX "")
add_dependencies(${PROJECT_NAME}_io_service lebai_msgs_generate_messages_cpp)


# system_service node
add_executable(${PROJECT_NAME}_system_service
  src/system_service/system_service_node.cpp
  src/system_service/system_service.cpp
)
target_link_libraries(${PROJECT_NAME}_system_service
  ${catkin_LIBRARIES}
  lebai_proto
)
set_target_properties(${PROJECT_NAME}_system_service
PROPERTIES OUTPUT_NAME system_service
PREFIX "")
add_dependencies(${PROJECT_NAME}_system_service lebai_msgs_generate_messages_cpp)

# motion_service node
add_executable(${PROJECT_NAME}_motion_service
  src/motion_service/motion_service_node.cpp
  src/motion_service/joint_trajectory_manager.cpp
  #  src/motion_service/joint_trajectory_pt_full_streamer.cpp
  src/motion_service/trajectory_move.cpp
)
target_link_libraries(${PROJECT_NAME}_motion_service
  lebai_proto
  ${catkin_LIBRARIES}
)
 set_target_properties(${PROJECT_NAME}_motion_service
 PROPERTIES OUTPUT_NAME motion_service
 PREFIX "")
add_dependencies(${PROJECT_NAME}_motion_service lebai_msgs_generate_messages_cpp)

#
#
#
##############
### Install ##
##############
#
## all install targets should use catkin DESTINATION variables
## See http://ros.org/doc/api/catkin/html/adv_user_guide/variables.html
#
### Mark executable scripts (Python etc.) for installation
### in contrast to setup.py, you can choose the destination
## install(PROGRAMS
##   scripts/my_python_script
##   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
## )
#
### Mark executables for installation
### See http://docs.ros.org/melodic/api/catkin/html/howto/format1/building_executables.html
## install(TARGETS ${PROJECT_NAME}_node
##   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
## )
#
### Mark libraries for installation
### See http://docs.ros.org/melodic/api/catkin/html/howto/format1/building_libraries.html
#
#install(
#    TARGETS ${PROJECT_NAME}_motion_service
#  ${PROJECT_NAME}_io_service
#  ${PROJECT_NAME}_system_service
#  ${PROJECT_NAME}_robot_state
#  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
#
### Mark cpp header files for installation
## install(DIRECTORY include/${PROJECT_NAME}/
##   DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
##   FILES_MATCHING PATTERN "*.h"
##   PATTERN ".svn" EXCLUDE
## )
#
#
### Mark other files for installation (e.g. launch and bag files, etc.)
#install(FILES
#  README.md
#  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
#)
#install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
#
#
#
## catkin_make run_tests
#find_package(rostest REQUIRED)
#
#find_package(rostest REQUIRED)
#add_rostest_gtest(test_system_service
#  test/test_system_service.test
#  test/test_system_service.cpp
#)
#target_link_libraries(test_system_service
#  ${catkin_LIBRARIES}
#)
#
#
#
#
#add_rostest_gtest(test_robot_state
#  test/test_robot_state.test
#  test/test_robot_state.cpp
#)
#target_link_libraries(test_robot_state
#  ${catkin_LIBRARIES}
#)
#
#add_rostest_gtest(test_io_service
#  test/test_io_service.test
#  test/test_io_service.cpp
#)
#target_link_libraries(test_io_service
#  ${catkin_LIBRARIES}
#)
#
#add_rostest_gtest(test_motion_service
#  test/test_motion_service.test
#  test/test_motion_service.cpp
#)
#target_link_libraries(test_motion_service
#  ${catkin_LIBRARIES}
#)



