cmake_minimum_required(VERSION 3.8)
project(lebai_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(trajectory_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

set(msg_files
  # "msg/ExecuteMode.msg"
  "msg/GripperStatus.msg"
  "msg/IOConditionalExpress.msg"
  "msg/UntilInfo.msg"
  "msg/MoveCommon.msg"
  "msg/TrajectoryMoveCircle.msg"
  "msg/TrajectoryMoveJoint.msg"
  "msg/TrajectoryMoveLine.msg"
  "msg/IOStatus.msg"
# from ros industrial
  "msg/DebugLevel.msg"
  "msg/DeviceInfo.msg"
  "msg/TriState.msg"
  "msg/RobotStatus.msg"
  "msg/RobotMode.msg"
)

set(srv_files
  "srv/MoveCircle.srv"
  "srv/MoveJoint.srv"
  "srv/MoveLine.srv"
  "srv/SetAMode.srv"
  "srv/SetAO.srv"
  "srv/SetDO.srv"
  "srv/SetGripper.srv"
)
rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES builtin_interfaces geometry_msgs std_msgs
)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
