安装
====

环境要求
--------

当前文档面向 Ubuntu 22.04 和 ROS2 Humble：

.. code-block:: text

   Ubuntu 22.04
   ROS2 Humble
   Python 3

安装 ROS2 后，先加载 ROS 环境：

.. code-block:: bash

   source /opt/ros/humble/setup.bash

创建工作空间
------------

.. code-block:: bash

   mkdir -p ~/lebai_ws/src
   cd ~/lebai_ws/src
   git clone --branch humble-dev https://github.com/lebai-robotics/lebai-ros-sdk.git
   cd ~/lebai_ws

安装依赖
--------

安装 Python SDK：

.. code-block:: bash

   python3 -m pip install pylebai

安装 ROS 包依赖：

.. code-block:: bash

   rosdep update
   rosdep install --from-paths src --ignore-src --rosdistro humble -y --skip-keys pylebai

构建
----

.. code-block:: bash

   colcon build --packages-select lebai_interfaces lebai_driver lebai_tutorials --symlink-install
   source install/setup.bash

检查安装
--------

查看驱动 launch 文件：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py --show-args

查看可用接口：

.. code-block:: bash

   ros2 interface list | grep lebai_interfaces

常用包
------

``lebai_driver``
   启动机器人驱动、控制器发现和独立 gripper 节点。

``lebai_interfaces``
   提供 ROS2 message 和 service 类型。

``lebai_tutorials``
   提供可直接运行的 Python 示例。
