cmake_minimum_required(VERSION 3.0.2)
project(lebai_tutorials)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  control_msgs
  lebai_interfaces
  moveit_commander
  rospy
  sensor_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/io_example.py
  scripts/joint_state_subscriber.py
  scripts/move_example.py
  scripts/moveit_gripper_amplitude_example.py
  scripts/moveit_manipulator_example.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Keep the importable helper next to the scripts in both Catkin spaces.
configure_file(
  scripts/lebai_tutorials_common.py
  "${CATKIN_DEVEL_PREFIX}/${CATKIN_PACKAGE_BIN_DESTINATION}/lebai_tutorials_common.py"
  COPYONLY
)
install(FILES scripts/lebai_tutorials_common.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
