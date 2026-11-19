安装
====

环境要求
--------

使用 Ubuntu 20.04 上的 ROS Noetic，依赖 Python 3.8 和 ``pylebai>=2.0.8,<3``。
本版本不支持 Python 2。驱动 2.0.0 含有不兼容的接口变更，使用前请查看
:doc:`interfaces/topics` 和 :doc:`interfaces/services`。

创建工作空间
------------

将本版本的源码放在 ``~/catkin_ws/src/lebai-ros-sdk``。

安装依赖
--------

安装好 ROS Noetic 后，先在运行 ROS 节点的 Python 3.8 环境中安装 Python SDK，
再构建 Catkin 工作空间。Ubuntu 20.04 自带 pip 20.0.2。下方命令会升级到
pip 25.0.1，该版本支持 Python 3.8，并能识别 SDK 的 Linux wheel 标签。

.. code-block:: bash

   sudo apt install python3-pip
   python3 -m pip install --user 'pip==25.0.1'
   python3 -m pip install --user 'pylebai>=2.0.8,<3'

如果尚未初始化 rosdep，先执行 ``sudo rosdep init``。然后在工作空间根目录安装
其余依赖。

.. code-block:: bash

   source /opt/ros/noetic/setup.bash
   cd ~/catkin_ws
   rosdep update --include-eol-distros
   rosdep install --from-paths src --ignore-src --rosdistro noetic --skip-keys pylebai -y

构建
----

在工作空间根目录构建并加载环境。

.. code-block:: bash

   catkin_make
   source devel/setup.bash

在运行驱动、示例或 MoveIt 的每个终端中，先执行
``source ~/catkin_ws/devel/setup.bash`` 加载工作空间环境。

检查安装
--------

确认当前环境能找到驱动包并读取接口定义。

.. code-block:: bash

   rospack find lebai_driver
   rosmsg show lebai_interfaces/RobotState

接下来参阅 :doc:`quickstart`。

构建本文档
----------

在仓库根目录安装文档依赖并构建。构建遇到 Sphinx 警告时会报错，成功后将页面
输出到 ``site/``。在浏览器中打开 ``site/index.html`` 查看。

.. code-block:: bash

   python3 -m pip install --user -r docs/requirements.txt
   ./scripts/build-docs.sh
