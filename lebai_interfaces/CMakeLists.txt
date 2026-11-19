cmake_minimum_required(VERSION 3.0.2)
project(lebai_interfaces)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  std_msgs
)

add_message_files(FILES
  CartesianPose.msg
  ClawState.msg
  ControllerInfo.msg
  GripperState.msg
  IOState.msg
  JointMotion.msg
  MotionParams.msg
  MotionTarget.msg
  Result.msg
  RobotState.msg
)

add_service_files(FILES
  Command.srv
  GetAnalogInput.srv
  GetAnalogInputs.srv
  GetAnalogOutput.srv
  GetAnalogOutputs.srv
  GetClaw.srv
  GetDigitalInput.srv
  GetDigitalInputs.srv
  GetDigitalOutput.srv
  GetDigitalOutputs.srv
  GetDioMode.srv
  GetMotionState.srv
  GetRunningMotion.srv
  GetSignals.srv
  LoadResourceList.srv
  MoveCircular.srv
  MoveJoint.srv
  MoveLinear.srv
  MovePvat.srv
  ResolveControllers.srv
  SetAnalogOutput.srv
  SetAnalogOutputs.srv
  SetClaw.srv
  SetDigitalOutput.srv
  SetDigitalOutputs.srv
  SetDioMode.srv
  SetGripperForce.srv
  SetGripperPosition.srv
  SetGripperVelocity.srv
  SetLed.srv
  SetSignals.srv
  SpeedJoint.srv
  SpeedLinear.srv
  WaitMove.srv
)

generate_messages(DEPENDENCIES std_msgs)

catkin_package(CATKIN_DEPENDS message_runtime std_msgs)
