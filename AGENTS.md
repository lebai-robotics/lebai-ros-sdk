# Agent Guide

This branch contains the ROS2 Jazzy Lebai driver. Runtime code is Python and
controller access goes through released `pylebai`.

## Start Here

- Runtime package: `lebai_driver/`
- Interfaces: `lebai_interfaces/`
- Examples: `lebai_tutorials/`
- Robot models/resources: `lebai_lm3_support/`, `lebai_resources/`
- Deferred MoveIt configuration: `lebai_lm3_moveit_config/`
- User docs: `docs/`
- Future/deferred work list: `TODO.md`

## Development Rules

- Always make changes through pull requests.
- Use conventional commit messages, for example `fix: align gripper frame`.
- Unless a request is explicitly branch-specific, apply concrete feature, fix,
  and process changes to all active runtime branches: `humble-dev`, `jazzy-dev`,
  and `lyrical-dev`.
- Do not modify legacy branches (`noetic-dev`, `galactic-dev`, `melodic-dev`)
  unless explicitly requested.
- Use released `pylebai`; do not use old `lebai.LebaiRobot`, direct
  `pymodbus`, direct `pyserial`, or C++ runtime driver code.
- Keep ROS categories aligned with SDK category names.
- Keep `docs/superpowers/` and generated `site/` output out of git.

## Verification

Run workspace builds and tests from the workspace root, not from this repository
directory:

```bash
cd /path/to/lebai_ws
source /opt/ros/${ROS_DISTRO:-jazzy}/setup.bash
source .venv/bin/activate
colcon build --packages-select lebai_interfaces lebai_driver lebai_tutorials --symlink-install
source install/setup.bash
python3 -m pytest src/lebai-ros-sdk/lebai_driver/test -q -m "not integration and not linter"
```

Run simulator smoke tests only when a controller or simulator is available:

```bash
LEBAI_TEST_ROBOT_IP=127.0.0.1 python3 -m pytest src/lebai-ros-sdk/lebai_driver/test/test_simulator_smoke.py -q -m integration
```

Build documentation from this repository root:

```bash
./scripts/build-docs.sh
```
