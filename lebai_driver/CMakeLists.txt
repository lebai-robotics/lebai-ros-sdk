cmake_minimum_required(VERSION 2.8.3)
project(lebai_driver)

find_package(catkin REQUIRED COMPONENTS
  industrial_robot_client
  lebai_msgs
  grpc
)




generate_proto(lebai_proto GRPC SRC_BASE "lebai-proto"
  FILES lebai-proto/robot_controller.proto lebai-proto/messages.proto
)
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES driver
  CATKIN_DEPENDS grpc industrial_robot_client
  LIBRARIES lebai_proto
#  DEPENDS system_lib
  LIBRARIES ${ALL_GRPC_LIBS} ${ALL_PROTOBUF_LIBS}
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
  src/motion_service/joint_trajectory_pt_full_streamer.cpp
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


install(TARGETS lebai_proto
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
)
      
install(TARGETS 
  ${PROJECT_NAME}_robot_state
  ${PROJECT_NAME}_io_service
  ${PROJECT_NAME}_motion_service
  ${PROJECT_NAME}_system_service  
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})


