cmake_minimum_required(VERSION 3.8)
project(lebai_tutorials)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(lebai_interfaces REQUIRED)

install(PROGRAMS
  scripts/move_example.py
  scripts/io_example.py
  scripts/joint_state_subscriber.py
  scripts/moveit_manipulator_example.py
  scripts/moveit_gripper_amplitude_example.py
  DESTINATION lib/${PROJECT_NAME}
)

install(FILES
  scripts/lebai_tutorials_common.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
