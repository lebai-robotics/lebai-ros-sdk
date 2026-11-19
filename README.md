# Lebai ROS SDK for Noetic

Driver 2.0.0 is a breaking release for ROS Noetic on Ubuntu 20.04 with Python 3.8 and `pylebai>=2.0.8,<3`. Python 2 is unsupported. The driver exposes services and status using `lebai_interfaces` and supports MoveIt 1 for the LM3 arm with or without its integrated gripper.

- [Install the SDK and build the Catkin workspace](docs/install.rst)
- [Launch the driver, discovery, or serial gripper](docs/quickstart.rst)
- [Review the migration table and driver behavior](docs/architecture.rst)
- [Run the Python tutorials](docs/examples.rst)
- [Configure LM3 for MoveIt 1](docs/moveit.rst)

Build the HTML documentation from the repository root.

```bash
python3 -m pip install --user -r docs/requirements.txt
./scripts/build-docs.sh
```

Open `site/index.html` after the build.
