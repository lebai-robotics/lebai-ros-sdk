安装
====

环境要求
--------

当前文档面向 Ubuntu 24.04 和 ROS2 Jazzy：

.. code-block:: text

   Ubuntu 24.04
   ROS2 Jazzy
   Python 3

安装 ROS2 后，先加载 ROS 环境：

.. code-block:: bash

   source /opt/ros/jazzy/setup.bash

创建工作空间
------------

.. code-block:: bash

   mkdir -p ~/lebai_ws/src
   cd ~/lebai_ws/src
   git clone --branch jazzy-dev https://github.com/lebai-robotics/lebai-ros-sdk.git
   cd ~/lebai_ws

安装依赖
--------

Ubuntu 24.04 的系统 Python 由 apt 管理，不建议直接用 ``pip`` 写入系统
Python 环境。先创建一个可以读取 ROS apt 包的虚拟环境，再安装
``pylebai``：

.. code-block:: bash

   python3 -m venv .venv --system-site-packages
   source .venv/bin/activate
   python3 -m pip install "pylebai>=2.0.0,<3.0.0"

安装 ROS 包依赖：

.. code-block:: bash

   rosdep update
   rosdep install --from-paths src --ignore-src --rosdistro jazzy -y --skip-keys pylebai

构建
----

.. code-block:: bash

   source .venv/bin/activate
   colcon build --symlink-install
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
