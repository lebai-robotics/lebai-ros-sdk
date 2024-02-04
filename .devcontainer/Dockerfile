FROM ros:melodic
RUN echo "\. \"/opt/ros/$ROS_DISTRO/setup.bash\"" >> "${HOME}/.bashrc" && \
    echo "\. /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> "${HOME}/.bashrc"
RUN apt-get update && apt install -y ros-melodic-srdfdom ros-melodic-moveit ros-melodic-urdf ros-melodic-tf ros-melodic-xacro ros-melodic-robot-state-publisher ros-melodic-control-msgs rviz ros-melodic-rviz ros-melodic-fcl ros-melodic-industrial-robot-client ros-melodic-grpc
