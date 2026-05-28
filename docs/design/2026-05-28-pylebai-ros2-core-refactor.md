# pylebai ROS2 Core Refactor Design

Date: 2026-05-28

## Summary

Refactor `lebai-ros-sdk` into an active ROS2-only driver project whose runtime
code is Python and whose controller access goes through the released `pylebai`
API. The first implementation targets Humble on Ubuntu 22.04 through a PR into
`humble-dev`. Jazzy on Ubuntu 24.04 is the next active distribution branch.

The phase-1 runtime scope is intentionally narrow and follows the public
`lebai-sdk` function categories:

- start_stop
- motion
- status
- io
- claw
- discovery
- standalone gripper

MoveIt, actions, LED/voice/fan, signals, kinematics, tasks, config, files,
modbus, serial, storage, backup/upgrade, and plugins are deferred to later
phases.

## Goals

- Remove C++ runtime/tutorial implementation from active ROS2 driver branches.
- Use `pylebai` as the only robot, controller, discovery, and gripper access
  layer.
- Keep a small `ament_cmake` interface package for `.msg`, `.srv`, and future
  `.action` generation.
- Introduce a breaking, cleaner ROS API instead of preserving old service names.
- Provide typed ROS services and topics, not a generic raw JSON-RPC ROS service.
- Add branch-owned documentation and GitHub Actions Pages deployment.
- Add CI that runs unit tests and simulator-backed smoke tests where the
  simulator supports the behavior.
- Add `AGENTS.md` so AI agents and human contributors share the same workflow
  rules.

## Non-Goals

- Preserve ROS1 support on active branches.
- Preserve old ROS service, topic, package, or node names unless they remain
  useful by coincidence.
- Refactor MoveIt configuration in phase 1.
- Add ROS actions in phase 1.
- Modify `lebai-sdk` or extend `pylebai`.
- Use the old `lebai_gripper_ros2` implementation, `pymodbus`, or `pyserial`
  directly.
- Provide complete `pylebai` coverage in phase 1.

## Branch Strategy

Work starts from `humble-dev` on a dev branch:

```text
dev/refactor-pylebai-ros2-core -> humble-dev
```

Historical branches remain frozen:

```text
melodic-dev
noetic-dev
galactic-dev
```

After the Humble refactor is stable, create or port to:

```text
jazzy-dev
```

Future Ubuntu 26.04 support should use the matching ROS2 distribution branch
when that work starts.

## Package Layout

Phase 1 keeps package boundaries simple:

```text
lebai_driver
  ament_python runtime package
  Python nodes, connection management, service/topic registration, tests

lebai_interfaces
  ament_cmake interface package
  all phase-1 msg/srv definitions
  future action definitions when actions are introduced

lebai_lm3_support
  robot model/resource package
  unchanged in phase 1 except for build compatibility if needed

lebai_resources
  shared xacro resources
  unchanged in phase 1 except for build compatibility if needed
```

`lebai_tutorials` should no longer contain C++ examples in the active ROS2
runtime path. Python examples can be reintroduced after the phase-1 API settles.

`lebai_lm3_moveit_config` remains out of phase-1 scope. It can stay present but
should not drive the core driver architecture.

Keep the package names `lebai_driver` and `lebai_interfaces` for phase 1. The
refactor is already a breaking ROS API change; renaming packages at the same
time would add migration cost without improving the runtime architecture.

`lebai_driver` should declare `pylebai` as its Python runtime dependency. If a
ROS distro package does not provide a rosdep key for `pylebai`, installation
docs and CI should install the released PyPI package explicitly.

## Runtime Architecture

Use one main Python driver node that owns one `pylebai.Robot` instance:

```text
lebai_driver_node
  connection lifecycle
  typed status publishers
  typed start_stop services
  typed motion services
  typed io services
  typed claw services and topics where supported by pylebai.Robot
```

Keep Python internals modular even though they share one ROS node:

```text
lebai_driver/
  connection.py
  errors.py
  status.py
  start_stop_services.py
  motion_services.py
  io_services.py
  claw_services.py
  conversions.py
```

Use separate nodes where the connection semantics differ:

```text
lebai_discovery_node
  uses pylebai discovery APIs

lebai_serial_gripper_node
  optional standalone gripper node
  uses released pylebai gripper APIs only
```

No phase-1 node may instantiate old `lebai.LebaiRobot` or directly use
`pymodbus`/`pyserial`.

## ROS API Principles

- Use a configurable namespace, with examples documented under `/lebai`.
- Use topics for continuously useful state.
- Use services for phase-1 commands and request/response queries.
- Do not use actions in phase 1.
- Do not expose a generic raw JSON-RPC ROS service as public API.
- Include success/error fields in service responses.
- Include motion IDs or state strings in motion responses where `pylebai`
  provides them so actions can be introduced later without rethinking the
  command model.

Function categories must follow the SDK public API groups. ROS paths use
lowercase names:

| SDK surface | ROS category |
| --- | --- |
| `Robot` STARTSTOP | `start_stop` |
| `Robot` MOTION | `motion` |
| `Robot` STATUS | `status` |
| `Robot` IO | `io` |
| `Robot` CLAW | `claw` |
| `Discovery` | `discovery` |
| `Gripper` | `gripper` |

Deferred SDK categories keep their SDK names in the roadmap: `config`, `led`,
`signal`, `program`/`scene`, `robotics`, `file`, `modbus`, `serial`, and
`storage`.

Example namespace shape:

```text
/lebai/status/robot
/lebai/status/joint_motion
/lebai/io/state
/lebai/start_stop/start_sys
/lebai/start_stop/stop_sys
/lebai/motion/movej
/lebai/motion/movel
/lebai/io/set_do
/lebai/claw/set_claw
/lebai/discovery/resolve
```

The final names should follow the released `pylebai` API and SDK function
categories rather than old ROS package categories.

## Phase-1 Interface Draft

The exact IDL can be refined during implementation for ROS2 syntax details, but
the phase-1 interface set should start from this concrete shape.

### Common Messages

```text
msg/Result.msg
  bool success
  int32 code
  string message

msg/CartesianPose.msg
  float64 x
  float64 y
  float64 z
  float64 rx
  float64 ry
  float64 rz
```

Use `CartesianPose` for SDK-style Cartesian data instead of
`geometry_msgs/Pose`, because released `pylebai` uses `x`, `y`, `z`, `rx`,
`ry`, and `rz`.

### State Messages And Topics

```text
msg/RobotState.msg
  std_msgs/Header header
  bool connected
  int32 state
  int32 estop_reason
  bool is_disconnected
  bool is_down
  string message

msg/JointMotion.msg
  std_msgs/Header header
  bool connected
  float64[] actual_joint_positions
  float64[] target_joint_positions
  float64[] actual_joint_speed
  float64[] target_joint_speed
  float64[] actual_joint_torques
  float64[] target_joint_torques
  lebai_interfaces/CartesianPose actual_tcp_pose
  lebai_interfaces/CartesianPose target_tcp_pose
  lebai_interfaces/CartesianPose actual_flange_pose
  string message

msg/IOState.msg
  std_msgs/Header header
  bool connected
  string device
  bool[] digital_inputs
  bool[] digital_outputs
  float64[] analog_inputs
  float64[] analog_outputs
  bool[] dio_modes
  string message

msg/ClawState.msg
  std_msgs/Header header
  bool connected
  float64 force
  float64 amplitude
  bool hold_on
  string message

msg/GripperState.msg
  std_msgs/Header header
  bool connected
  float64 position
  float64 force
  float64 velocity
  bool calibrated
  string message
```

Initial topics:

```text
/lebai/status/joint_states     sensor_msgs/msg/JointState
/lebai/status/robot            lebai_interfaces/msg/RobotState
/lebai/status/joint_motion     lebai_interfaces/msg/JointMotion
/lebai/io/state                lebai_interfaces/msg/IOState
/lebai/claw/state              lebai_interfaces/msg/ClawState
/lebai/gripper/state           lebai_interfaces/msg/GripperState
```

Default publish rates should be parameters:

```text
joint_state_publish_rate: 20.0
robot_state_publish_rate: 10.0
joint_motion_publish_rate: 10.0
io_state_publish_rate: 5.0
gripper_state_publish_rate: 10.0
```

Use bounded queue depths. Start with depth `10` for state topics and make QoS
profiles configurable only if real users need it.

### StartStop Services

Use one reusable command service type:

```text
srv/Command.srv
  ---
  lebai_interfaces/Result result
```

Initial services:

```text
/lebai/start_stop/start_sys
/lebai/start_stop/stop_sys
/lebai/start_stop/powerdown
/lebai/start_stop/stop
/lebai/start_stop/estop
/lebai/start_stop/start_teach_mode
/lebai/start_stop/end_teach_mode
/lebai/start_stop/pause_move
/lebai/start_stop/resume_move
/lebai/start_stop/reboot
```

### Motion Services

```text
msg/MotionParams.msg
  float64 acceleration
  float64 velocity
  float64 time
  float64 blend_radius

msg/MotionTarget.msg
  bool is_joint_pose
  float64[] joint_positions
  lebai_interfaces/CartesianPose cartesian_pose

srv/MoveJoint.srv
  lebai_interfaces/MotionTarget target
  lebai_interfaces/MotionParams params
  ---
  lebai_interfaces/Result result
  uint32 motion_id

srv/MoveLinear.srv
  lebai_interfaces/MotionTarget target
  lebai_interfaces/MotionParams params
  ---
  lebai_interfaces/Result result
  uint32 motion_id

srv/MoveCircular.srv
  lebai_interfaces/MotionTarget via
  lebai_interfaces/MotionTarget target
  float64 rad
  lebai_interfaces/MotionParams params
  ---
  lebai_interfaces/Result result
  uint32 motion_id

srv/SpeedJoint.srv
  float64 acceleration
  float64[] velocities
  float64 time
  ---
  lebai_interfaces/Result result
  uint32 motion_id

srv/SpeedLinear.srv
  float64 acceleration
  lebai_interfaces/CartesianPose velocity
  float64 time
  lebai_interfaces/CartesianPose reference
  ---
  lebai_interfaces/Result result
  uint32 motion_id

srv/MovePvat.srv
  float64[] positions
  float64[] velocities
  float64[] accelerations
  float64 duration
  ---
  lebai_interfaces/Result result

srv/WaitMove.srv
  uint32 motion_id
  ---
  lebai_interfaces/Result result

srv/GetMotionState.srv
  uint32 motion_id
  ---
  lebai_interfaces/Result result
  string state

srv/GetRunningMotion.srv
  ---
  lebai_interfaces/Result result
  uint32 motion_id
```

Initial services:

```text
/lebai/motion/movej
/lebai/motion/movel
/lebai/motion/movec
/lebai/motion/speedj
/lebai/motion/speedl
/lebai/motion/move_pvat
/lebai/motion/wait_move
/lebai/motion/stop_move
/lebai/motion/skip_move
/lebai/motion/get_motion_state
/lebai/motion/get_running_motion
```

`/lebai/motion/stop_move` and `/lebai/motion/skip_move` can use
`srv/Command.srv`.

### IO Services

Use SDK device names directly as strings in phase 1. Expected values include
`ROBOT`, `FLANGE`, `EXTRA`, `SHOULDER`, and `FLANGE_BTN`, but the service layer
should pass through any device string accepted by released `pylebai`.

```text
srv/SetDigitalOutput.srv
  string device
  uint32 pin
  bool value
  ---
  lebai_interfaces/Result result

srv/GetDigitalInput.srv
  string device
  uint32 pin
  ---
  lebai_interfaces/Result result
  bool value

srv/GetDigitalOutput.srv
  string device
  uint32 pin
  ---
  lebai_interfaces/Result result
  bool value

srv/SetAnalogOutput.srv
  string device
  uint32 pin
  float64 value
  ---
  lebai_interfaces/Result result

srv/GetAnalogInput.srv
  string device
  uint32 pin
  ---
  lebai_interfaces/Result result
  float64 value

srv/GetAnalogOutput.srv
  string device
  uint32 pin
  ---
  lebai_interfaces/Result result
  float64 value

srv/SetDioMode.srv
  string device
  uint32 pin
  bool is_output
  ---
  lebai_interfaces/Result result

srv/GetDioMode.srv
  string device
  uint32 pin
  ---
  lebai_interfaces/Result result
  bool is_output
```

Initial services:

```text
/lebai/io/set_do
/lebai/io/get_di
/lebai/io/get_do
/lebai/io/set_ao
/lebai/io/get_ai
/lebai/io/get_ao
/lebai/io/set_dio_mode
/lebai/io/get_dio_mode
```

Vector IO services can be added in a follow-up phase-1 PR if the scalar
services and state topic land cleanly first.

### Claw Services

Controller claw services:

```text
srv/SetClaw.srv
  float64 force
  float64 amplitude
  ---
  lebai_interfaces/Result result

srv/GetClaw.srv
  ---
  lebai_interfaces/Result result
  lebai_interfaces/ClawState state
```

Initial controller claw services:

```text
/lebai/claw/init_claw
/lebai/claw/set_claw
/lebai/claw/get_claw
```

### Standalone Gripper Services

Standalone gripper services, only where released `pylebai` gripper bindings
support them:

```text
srv/SetGripperPosition.srv
  uint32 position
  ---
  lebai_interfaces/Result result

srv/SetGripperForce.srv
  uint32 force
  ---
  lebai_interfaces/Result result

srv/SetGripperVelocity.srv
  uint32 velocity
  bool persistent
  ---
  lebai_interfaces/Result result
```

Standalone calibration and auto-calibration services can use `srv/Command.srv`
with distinct service names:

```text
/lebai/gripper/do_calibration
/lebai/gripper/turn_on_auto_calibration
/lebai/gripper/turn_off_auto_calibration
```

### Discovery Messages And Services

```text
msg/ControllerInfo.msg
  string hostname
  string ip_address
  string mac_address
  string model
  string ds_version
  string rc_version
  string id

srv/ResolveControllers.srv
  ---
  lebai_interfaces/Result result
  lebai_interfaces/ControllerInfo[] controllers
```

Initial service and topic:

```text
/lebai/discovery/resolve
/lebai/discovery/controllers
```

## Phase-1 Interface Scope

### Status

Publish state that is useful to subscribers:

- `sensor_msgs/msg/JointState` for standard joint state consumers.
- Robot state/status using new `lebai_interfaces` messages.
- Joint motion data if supported by released `pylebai`.
- IO state where polling is practical.
- Controller claw state where supported by released `pylebai`.

Status publishers should tolerate transient SDK exceptions and publish explicit
connection/error status where the message model supports it.

### StartStop

Expose service wrappers for safe lifecycle and motion-control commands from
released `pylebai.Robot`, including:

- start_sys
- stop_sys
- powerdown
- stop
- estop
- start/end teach mode
- pause/resume move
- reboot where safe and explicitly requested by users

Service handlers should map SDK exceptions into structured responses rather
than crashing the node.

### Motion

Expose services, not actions, for phase-1 motion:

- `movej` / move joint
- `movel` / move linear
- `movec` / move circular where released `pylebai` supports it
- `speedj`
- `speedl` where released `pylebai` supports it
- `move_pvat`
- `wait_move`
- `stop_move`
- `skip_move`
- `get_running_motion`
- `get_motion_state`

Motion service docs must state whether a command only submits a buffered motion
or waits for completion.

### IO

Use the current SDK device-name model instead of old hardcoded service names:

- get/set digital output
- get digital input
- get/set analog output
- get analog input
- vector read/write helpers where released `pylebai` supports them
- DIO mode services where released `pylebai` supports them

The interface should represent the device name explicitly, for example robot,
flange, extra, shoulder, or flange button, matching SDK documentation.

### Claw And Standalone Gripper

There are two gripper paths:

- Controller claw support through released `pylebai.Robot` methods in the SDK
  `CLAW` category.
- Optional standalone gripper support through released `pylebai` gripper
  bindings.

The old `lebai_gripper_ros2` package is reference material only. Its concepts
may inform messages and services, but its implementation and dependencies must
not be used.

If released `pylebai` lacks a gripper field or command, phase 1 should omit that
feature and document it as future work.

### Discovery

Provide a separate discovery node and typed service/topic interface using
released `pylebai` discovery APIs. Discovery is separate because it does not
require a connected `pylebai.Robot` instance.

## Later Interface Roadmap

Later phases should add typed services/topics for:

- LED/voice/fan
- signals
- kinematics
- tasks/scenes
- config resources
- files
- modbus
- serial
- storage
- backup/restore/upgrade
- plugins
- ROS actions for long-running/cancellable work
- MoveIt integration

Each phase should add a small coherent interface set instead of dumping every
SDK method into ROS at once.

## Documentation Architecture

Replace the manually maintained `doc` branch plus committed generated
`gh-pages` HTML model.

Use branch-owned Sphinx source and GitHub Actions Pages deployment:

```text
docs/
  index.rst
  install.rst
  quickstart.rst
  architecture.rst
  interfaces/
    topics.rst
    services.rst
  migration.rst
  roadmap.rst
  agent-guide.rst
```

The published site should preserve the old user experience of one page where
users choose a ROS distribution:

```text
/                 distro chooser
/humble/          docs built from humble-dev
/jazzy/           docs built from jazzy-dev later
/legacy/          frozen old docs
```

Use Sphinx initially because the existing content is RST and the current public
site is Sphinx-generated. Add a generated `versions.json` and a lightweight
version/distro switcher.

The GitHub Pages source should be GitHub Actions, not manual pushes of generated
HTML. The workflow should build selected branch docs into subdirectories, copy
the current generated `origin/gh-pages` site under `legacy/` for the first
refactor, upload a Pages artifact, and deploy it with the standard Pages
actions.

Legacy ROS1 and Galactic docs should be frozen under `legacy/` or otherwise
archived. They are not active maintenance targets.

## CI And Tests

CI must run unit tests and simulator-backed smoke tests where possible.

Use the `lebai-sdk` CI simulator pattern as the reference:

```yaml
services:
  lmaster:
    image: registry.cn-shanghai.aliyuncs.com/lebai/l-master:3.1.6
    options: >-
      --health-cmd="curl -f http://localhost:8080 || exit 1"
      --health-interval=10s
      --health-timeout=5s
      --health-retries=5
```

In CI, resolve the simulator service IP:

```bash
LM_IP=$(getent hosts lmaster | awk '{print $1}')
```

For local simulator tests, document the host endpoint as `127.0.0.1`.

Test layers:

- Unit tests use fake `pylebai` clients and cover all phase-1 domains.
- ROS node tests verify parameters, service registration, topic publication, and
  request/response conversion.
- Simulator integration tests run only for simulator-supported behavior.
- Hardware-only behavior, such as standalone gripper paths if unsupported by the
  simulator, gets fake-client coverage and clear documentation.

Simulator integration should skip cleanly when a feature is unavailable rather
than failing unrelated CI. Phase-1 integration should prefer safe smoke paths:

- SDK connection
- robot state
- safe start/stop lifecycle where supported
- non-dangerous IO checks if supported
- safe motion submit/status checks only when verified safe in the simulator

Expected CI surfaces for Humble:

```text
.github/workflows/ros2_humble_ci.yml
  lint and unit tests
  simulator integration smoke tests

.github/workflows/docs.yml
  versioned Sphinx docs build and GitHub Pages deploy
```

Initial simulator smoke tests should cover:

- create a `pylebai.Robot` connection through the ROS node config
- call `/lebai/start_stop/start_sys` and `/lebai/start_stop/stop_sys` if the
  simulator accepts them
- receive one `/lebai/status/robot` message
- receive one `/lebai/status/joint_states` message
- call `/lebai/motion/get_running_motion`

Gripper, discovery, and unsupported IO paths should be unit-tested with fake
clients unless CI gains a simulator or fixture that supports them.

## AGENTS.md

Add root `AGENTS.md` as the short entry point for AI agents and contributors.
It should include:

- repo map
- branch and PR workflow
- phase-1 scope and deferred scope
- rule that runtime implementation is Python
- rule that all runtime controller access uses released `pylebai`
- rule that old `lebai_gripper_ros2` implementation and direct Modbus/serial
  dependencies are not used
- docs workflow
- unit and simulator test commands
- guidance to preserve user changes and avoid destructive git commands

## Risks And Mitigations

- **Released `pylebai` may not expose every old ROS feature.** Omit missing
  features from phase 1 and document them as future work.
- **A single node can become too large.** Keep domain registration in separate
  Python modules with small testable functions.
- **Simulator coverage may be partial.** Use fake-client tests for all domains
  and simulator tests only for supported behavior.
- **Docs migration can disrupt old links.** Preserve legacy generated docs under
  `legacy/` and provide a root distro chooser.
- **Breaking ROS API requires user migration.** Provide a migration guide and
  clear examples for phase-1 services/topics.

## Open Decisions For Implementation Planning

- Exact ROS2 IDL syntax details after validating generated interfaces locally.
- Exact list of released `pylebai` gripper bindings available from the package
  version used in CI.
- Whether vector IO services land in the first implementation PR or immediately
  after scalar IO service coverage.
