cmake_minimum_required(VERSION 3.1.3)
project(lebai_lm3_moveit_config)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN "setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)
  set(mode_test_result "pytest-moveit-modes.xml")
  set(mode_test_results_dir "${CATKIN_TEST_RESULTS_DIR}/${PROJECT_NAME}")
  catkin_run_tests_target(pytest moveit_modes "${mode_test_result}"
    COMMAND "\"${PYTHON_EXECUTABLE}\" -B -m pytest -q -p no:cacheprovider --junitxml=\"${mode_test_results_dir}/${mode_test_result}\" \"${CMAKE_CURRENT_SOURCE_DIR}/test/test_moveit_modes.py\""
  )
  add_rostest(test/lm3_arm_only.test)
  add_rostest(test/lm3_with_gripper.test)
endif()
