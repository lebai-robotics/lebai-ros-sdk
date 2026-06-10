# Agent Guide

This repository is being refactored into a ROS2-only Lebai driver whose runtime
code is Python and whose controller access goes through released `pylebai`.

## Repository Map

- `lebai_driver/`: active `ament_python` runtime package.
- `lebai_interfaces/`: small `ament_cmake` package for `.msg` and `.srv`
  generation.
- `lebai_tutorials/`: Python examples for the new ROS2 API.
- `lebai_lm3_support/` and `lebai_resources/`: robot model/resource packages.
- `lebai_lm3_moveit_config/`: deferred MoveIt configuration.
- `docs/`: committed user documentation.
- `docs/superpowers/`: local AI planning scratch space; do not commit it.

## Phase 1 Scope

Implement only the released `pylebai` APIs needed for:

- `start_stop`
- `motion`
- `status`
- `io`
- `claw`
- `discovery`
- standalone `gripper`

Actions, MoveIt, config/files/modbus/serial/storage, programs/scenes, robotics,
LED, signal, and other SDK areas are later phases.

## Hard Rules

- Do not use old `lebai.LebaiRobot`.
- Do not use direct `pymodbus` or `pyserial`.
- Do not restore C++ runtime driver code.
- Use released `pylebai`; do not patch `/home/liufang/lebai/lebai-sdk` from this
  repo.
- Keep ROS categories aligned with the SDK category names.
- Keep `docs/superpowers/` and generated `site/` output out of git.

## Branch Workflow

Develop on topic branches and open pull requests into the matching distro
branch. Current active target:

```text
jazzy-dev-refactor -> jazzy-dev
```

Future distro branches should carry distro-specific fixes instead of mixing
Humble, Jazzy, and future ROS releases in one branch.

## Verification

Use ROS Jazzy locally for this branch:

```bash
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

Build documentation with:

```bash
./scripts/build-docs.sh
```

## Documentation

Committed documentation lives under `docs/` and is built with Sphinx into
`site/`. GitHub Pages is deployed from Actions, not by committing generated
HTML.
