cmake_minimum_required(VERSION 3.8)
project(lebai_lm3_support)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(Python3 REQUIRED COMPONENTS Interpreter)

  add_test(
    NAME test_gripper_mimic
    COMMAND ${Python3_EXECUTABLE} -m pytest
      test/test_gripper_mimic.py -q --no-xvfb
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_display_launch_graph
    COMMAND ${Python3_EXECUTABLE} -m pytest
      test/test_display_launch_graph.py -q
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  set_tests_properties(test_display_launch_graph PROPERTIES TIMEOUT 600)
  add_test(
    NAME test_launch_inventory
    COMMAND ${Python3_EXECUTABLE} -m pytest
      test/test_launch_inventory.py -q --no-xvfb
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_package_dependencies
    COMMAND ${Python3_EXECUTABLE} -m pytest
      test/test_package_dependencies.py -q --no-xvfb
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_rviz_config
    COMMAND ${Python3_EXECUTABLE} -m pytest
      test/test_rviz_config.py -q --no-xvfb
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_robot_models
    COMMAND ${Python3_EXECUTABLE} -m pytest
      test/test_robot_models.py -q --no-xvfb
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
endif()


install(DIRECTORY launch meshes rviz urdf DESTINATION
    share/${PROJECT_NAME}
)

ament_package()
