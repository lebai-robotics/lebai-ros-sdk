cmake_minimum_required(VERSION 3.8)
project(lebai_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

set(msg_files
  "msg/Result.msg"
  "msg/CartesianPose.msg"
  "msg/RobotState.msg"
  "msg/JointMotion.msg"
  "msg/IOState.msg"
  "msg/ClawState.msg"
  "msg/GripperState.msg"
  "msg/MotionParams.msg"
  "msg/MotionTarget.msg"
  "msg/ControllerInfo.msg"
)

set(srv_files
  "srv/Command.srv"
  "srv/MoveJoint.srv"
  "srv/MoveLinear.srv"
  "srv/MoveCircular.srv"
  "srv/SpeedJoint.srv"
  "srv/SpeedLinear.srv"
  "srv/MovePvat.srv"
  "srv/WaitMove.srv"
  "srv/GetMotionState.srv"
  "srv/GetRunningMotion.srv"
  "srv/SetDigitalOutput.srv"
  "srv/GetDigitalInput.srv"
  "srv/GetDigitalOutput.srv"
  "srv/SetDigitalOutputs.srv"
  "srv/GetDigitalInputs.srv"
  "srv/GetDigitalOutputs.srv"
  "srv/SetAnalogOutput.srv"
  "srv/GetAnalogInput.srv"
  "srv/GetAnalogOutput.srv"
  "srv/SetAnalogOutputs.srv"
  "srv/GetAnalogInputs.srv"
  "srv/GetAnalogOutputs.srv"
  "srv/SetDioMode.srv"
  "srv/GetDioMode.srv"
  "srv/SetLed.srv"
  "srv/GetSignals.srv"
  "srv/SetSignals.srv"
  "srv/LoadResourceList.srv"
  "srv/SetClaw.srv"
  "srv/GetClaw.srv"
  "srv/SetGripperPosition.srv"
  "srv/SetGripperForce.srv"
  "srv/SetGripperVelocity.srv"
  "srv/ResolveControllers.srv"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES std_msgs
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
