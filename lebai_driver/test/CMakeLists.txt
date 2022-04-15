if (CATKIN_ENABLE_TESTING)
catkin_install_python(PROGRAMS
  test_param_utils.py
  test_lebai_driver.py
  motion_service_proxy.py
  robot_state_proxy.py
  system_service_proxy.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
find_package(rostest REQUIRED)
  add_rostest(test_param_utils.launch)
  add_rostest(test_lebai_driver.launch)
endif()
