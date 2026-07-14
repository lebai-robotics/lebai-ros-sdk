# Blocked and Deferred Work

This file contains only work that has an accepted direction but cannot be
completed safely in the current runtime. Current services, topics, actions,
launch files, and examples are documented under `docs/`.

## RSDK-001: Execute ROS trajectories without controller pre-positioning

The current controller playback path pre-positions before replaying stored
trajectory data. `FollowJointTrajectory` must eventually validate the requested
start state and use a distinct PVAT path that never inserts that move.

This remains blocked on authorized controller/protocol work, a corresponding
SDK API, and a released `pylebai>=2.1.0,<3.0.0` exposing it. The ROS driver must
not claim or emulate no-preposition execution before those dependencies exist.

## RSDK-005: Replace string IO devices with a typed enum

The released SDK accepts canonical uppercase device names such as `ROBOT` and
`FLANGE`, but an unknown or lowercase string can silently fall back to `ROBOT`.
The ROS interface therefore remains unsafe for misspelled device names.

The accepted fix requires a stable SDK/SWIG `IoDevice` enum, a released
`pylebai` facade exposing it, and a coordinated typed ROS interface. Until that
release is available, callers and new requests should use canonical uppercase
device names. The existing `io_example.py` currently retains legacy lowercase
`robot` as a ROBOT-only compatibility example; do not copy that value
for `FLANGE` or any other device.

## RSDK-014: Support standard trajectory tolerances

`FollowJointTrajectory` currently ignores `path_tolerance`, `goal_tolerance`,
and `goal_time_tolerance`. Empty tolerances retain the current fixed 0.01 rad
goal tolerance and local timeout policy.

Coherent kinematics snapshots are now available, but explicit tolerance
semantics and validation remain deferred to avoid introducing false motion
failures. Any implementation must preserve current behavior for ordinary
MoveIt goals and test supplied path, goal, and time tolerances separately.

## RSDK-027: Provide validated simplified LM3 collision geometry

The LM3 MoveIt model currently uses detailed visual meshes for collision
geometry, which makes model and planning-scene startup expensive. Replacing
them remains deferred until conservative simplified collision assets are
generated and validated against representative robot states. Existing debug
boxes are not suitable production collision geometry.
