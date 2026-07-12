cmake_minimum_required(VERSION 3.10.2)
project(lebai_lm3_moveit_config)
find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(Python3 REQUIRED COMPONENTS Interpreter)

  add_test(
    NAME test_gripper_group
    COMMAND ${Python3_EXECUTABLE} -m pytest test/test_gripper_group.py -q
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_model_startup
    COMMAND ${Python3_EXECUTABLE} -m pytest test/test_model_startup.py -q
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_launch_inventory
    COMMAND ${Python3_EXECUTABLE} -m pytest test/test_launch_inventory.py -q
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_package_dependencies
    COMMAND ${Python3_EXECUTABLE} -m pytest test/test_package_dependencies.py -q
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_planning_limits
    COMMAND ${Python3_EXECUTABLE} -m pytest test/test_planning_limits.py -q
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
  add_test(
    NAME test_planning_limits_launch
    COMMAND ${Python3_EXECUTABLE} -m pytest test/test_planning_limits_launch.py -q
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
endif()

ament_package()

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(FILES .setup_assistant DESTINATION share/${PROJECT_NAME})
