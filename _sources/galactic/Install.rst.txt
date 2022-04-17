.. _galactic_install:

编译编译安装
============

.. contents:: 目录
   :depth: 2
   :local:

为了编译运行 ``lebai-ros-sdk``，你需要先安装一些依赖。

安装 ``ROS 2``
---------------------------------

您可以参考  `ROS 2官方文档 <https://docs.ros.org/en/galactic/Installation.html>`_ 安装 ``ROS 2`` 。
在一个标准的 ``Ubuntu`` 桌面系统通过 ``Debian package`` 的安装步骤通常如下：

设置 ``ROS 2`` 软件包安装源
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sudo apt update && sudo apt install curl gnupg lsb-release
   # https://ghproxy.com is for chinese network.
   curl -sSL https://ghproxy.com/https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

通过 ``apt`` 安装 ``ROS 2``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sudo apt update
   sudo apt install ros-galactic-desktop # use desktop full， this will take some time.

设置 ``ROS 2`` 环境
^^^^^^^^^^^^^^^^^^^^^^^^^

您需要在 **bash** 终端中运行如下脚本来设置 ``ROS 2`` 环境。

.. code-block:: bash

   source /opt/ros/galactic/setup.bash

如果您不希望每次打开终端都需要运行上述脚本，你可以通过将上述脚本内容写入对应的 ``rc`` 配置文件中来简化。

**bash**

.. code-block:: bash

   echo "source /opt/ros/galactic/setup.bash" >> ~/.bashrc
   source ~/.bashrc

如果您使用 ``zsh``，则相应的脚本如下。

**zsh**

.. code-block:: bash

   echo "source /opt/ros/galactic/setup.zsh" >> ~/.zshrc
   source ~/.zshrc

注意，如果您的设备装有多个不同的 ``ROS`` 发行版，您可以通过不同的脚本文件来选择使用不同的发行版。
当您切换时，请重新打开一个新的 ``Shell`` 。


安装 ``ROS 2`` 依赖包
---------------------------------
运行如下脚本，安装一些 ``lebai-ros-sdk`` 所需要的依赖包。

.. code-block:: bash

   sudo apt install ros-galactic-control-msgs ros-galactic-moveit

安装 ``python`` 依赖包
---------------------------------
``lebai-ros-sdk`` 依赖于如下 ``python`` 包:
   * `lebai-python-sdk <https://pypi.org/project/lebai/>`_

通过 ``pip`` 可以进行安装

.. code-block:: bash

   sudo apt install python3-pip # If pip is not install.
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple lebai

编译 ``lebai-ros-sdk`` 开发包
---------------------------------

您现在可以开始从github克隆 ``lebai-ros-sdk`` 的源代码，并且尝试编译。

运行如下脚本：

.. code-block:: bash

   mkdir -p  ~/lebai_ws/src
   cd  ~/lebai_ws/src
   # choose one you prefer:
   # ssh
   git clone git@github.com:lebai-robotics/lebai-ros-sdk.git -b galactic-dev
   # https
   git clone https://github.com/lebai-robotics/lebai-ros-sdk.git -b galactic-dev
   cd ~/lebai_ws
   colcon build

您现在已经完成了 ``lebai-ros-sdk`` 的编译。

.. note::
   记住，当您完成编译后，您需要设置您工作空间的环境以便让 ``ROS 2`` 发现您的包。
   
.. code-block:: bash
   
   # for bash 
   source ~/lebai_ws/install/setup.bash
   # for zsh
   source ~/lebai_ws/install/setup.zsh
   