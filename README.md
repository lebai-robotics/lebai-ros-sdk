# Lebai ROS SDK

This repository hosts ROS drivers, examples, robot descriptions, and
documentation for Lebai robots.

The `main` branch is a landing branch only. Do not build robot driver packages
from `main`; choose the branch that matches your ROS distribution.

## Active ROS2 Branches

| ROS distribution | Ubuntu | Branch | Clone command |
| --- | --- | --- | --- |
| ROS2 Humble | Ubuntu 22.04 | `humble-dev` | `git clone --branch humble-dev https://github.com/lebai-robotics/lebai-ros-sdk.git` |
| ROS2 Jazzy | Ubuntu 24.04 | `jazzy-dev` | `git clone --branch jazzy-dev https://github.com/lebai-robotics/lebai-ros-sdk.git` |
| ROS2 Lyrical | Ubuntu 26.04 | `lyrical-dev` | `git clone --branch lyrical-dev https://github.com/lebai-robotics/lebai-ros-sdk.git` |

## Legacy Branches

These branches are kept for existing users and are not part of current
development:

| ROS distribution | Branch |
| --- | --- |
| ROS Noetic | `noetic-dev` |
| ROS2 Galactic | `galactic-dev` |
| ROS Melodic | `melodic-dev` |

## Documentation

GitHub Pages is orchestrated from this landing branch. The Pages workflow checks
out each active distro branch, builds that branch's Sphinx documentation, and
publishes a combined documentation site to the `gh-pages` branch:

```text
/              branch selector
/humble/       docs built from humble-dev
/jazzy/        docs built from jazzy-dev
/lyrical/      docs built from lyrical-dev
/noetic/       legacy archive, if preserved
/galactic/     legacy archive, if preserved
/melodic/      legacy archive, if preserved
```

Active distro branches run their own CI to validate code, tests, and local docs.
They do not deploy GitHub Pages.
