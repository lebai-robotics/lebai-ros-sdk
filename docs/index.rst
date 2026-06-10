Lebai ROS SDK 文档
==================

本页面用于选择与你的 ROS 发行版匹配的文档和代码分支。

``main`` 分支只作为项目入口和文档发布分支，不用于构建机器人驱动。使用前请
根据你的 Ubuntu 和 ROS 版本选择对应分支。

当前 ROS2 文档
--------------

.. list-table::
   :header-rows: 1

   * - ROS 发行版
     - Ubuntu
     - 代码分支
     - 文档
   * - ROS2 Humble
     - 22.04
     - ``humble-dev``
     - `打开 Humble 文档 <humble/>`__
   * - ROS2 Jazzy
     - 24.04
     - ``jazzy-dev``
     - `打开 Jazzy 文档 <jazzy/>`__
   * - ROS2 Lyrical
     - 26.04
     - ``lyrical-dev``
     - `打开 Lyrical 文档 <lyrical/>`__

获取代码
--------

.. code-block:: bash

   git clone --branch humble-dev https://github.com/lebai-robotics/lebai-ros-sdk.git
   git clone --branch jazzy-dev https://github.com/lebai-robotics/lebai-ros-sdk.git
   git clone --branch lyrical-dev https://github.com/lebai-robotics/lebai-ros-sdk.git

历史文档
--------

以下分支保留给老用户参考，不再作为当前开发目标：

.. list-table::
   :header-rows: 1

   * - ROS 发行版
     - 代码分支
     - 文档
   * - ROS Noetic
     - ``noetic-dev``
     - `打开 Noetic 历史文档 <noetic/>`__
   * - ROS2 Galactic
     - ``galactic-dev``
     - `打开 Galactic 历史文档 <galactic/>`__
   * - ROS Melodic
     - ``melodic-dev``
     - `打开 Melodic 历史文档 <melodic/>`__
