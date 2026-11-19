cmake_minimum_required(VERSION 2.8.3)
project(lebai_lm3_support)

find_package(catkin REQUIRED)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES lebai_lm3_support
#  CATKIN_DEPENDS other_catkin_pkg
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
# ${catkin_INCLUDE_DIRS}
)

## Declare a C++ library
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/lebai_lm3_support.cpp
# )

install(DIRECTORY config launch urdf  meshes DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

if(CATKIN_ENABLE_TESTING)
  set(gripper_test_result "pytest-gripper-mimic.xml")
  set(gripper_test_path "${CMAKE_CURRENT_SOURCE_DIR}/test/test_gripper_mimic.py")
  set(gripper_test_results_dir "${CATKIN_TEST_RESULTS_DIR}/${PROJECT_NAME}")
  catkin_run_tests_target(pytest gripper_mimic "${gripper_test_result}"
    COMMAND "\"${PYTHON_EXECUTABLE}\" -B -m pytest -q -p no:cacheprovider --junitxml=\"${gripper_test_results_dir}/${gripper_test_result}\" \"${gripper_test_path}\""
  )
endif()
