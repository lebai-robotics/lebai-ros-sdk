# TODO

This file tracks future work that is not part of the current active scope.

## Deferred Runtime Areas

The active runtime branches currently prioritize released `pylebai` APIs for
start/stop, motion, status, IO, resource lists, claw, discovery, and standalone
gripper support.

Later phases should cover:

- actions
- MoveIt configuration
  - gripper group semantics are configured.
  - arm trajectory execution is available through the
    `/lebai_trajectory_controller` FollowJointTrajectory action bridge.
  - gripper execution is available through the
    `/lebai_gripper_controller/gripper_cmd` GripperCommand action bridge.
- config/files/modbus/serial/storage APIs
- box device discovery APIs
- programs and scenes
- robotics SDK areas beyond current runtime scope
- other released SDK areas not yet mapped into ROS

## Planned Version System

Do not implement this in the current API expansion branch.

Use a distro-scoped release version model for runtime branches:

- Package versions are tracked per active distro branch.
- Tags use distro prefixes: `humble-vX.Y.Z`, `jazzy-vX.Y.Z`, and
  `lyrical-vX.Y.Z`.
- Keep versions aligned across active distro branches when the same feature or
  fix applies to all of them.
- Allow distro-specific patch releases when only one distro branch needs a fix,
  for example `humble-v0.2.1`.
- `main` does not own the runtime package version; it coordinates docs and
  GitHub Pages orchestration.

## API Expansion Order

Expand APIs one coherent PR at a time instead of putting every deferred API area
into one branch.

No concrete API expansion item is currently queued. Pick the next coherent area
from Deferred Runtime Areas and add it here before implementation.
