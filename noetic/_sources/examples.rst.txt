示例
====

加载工作空间环境后，在终端运行以下 Python 示例。示例使用驱动的默认配置，可
通过 ROS 名称重映射将服务和话题指向其他命名空间。

基础驱动示例
------------

先按 :doc:`quickstart` 启动驱动。

读取机械臂关节状态
~~~~~~~~~~~~~~~~~~

``joint_state_subscriber.py`` 通过 ``rospy.Subscriber`` 订阅
``/lebai/status/joint_states``，并记录关节名称和位置。

.. code-block:: bash

   rosrun lebai_tutorials joint_state_subscriber.py

设置 I/O 输出
~~~~~~~~~~~~~

``io_example.py`` 通过 ``rospy.ServiceProxy`` 调用 ``/lebai/io/set_do`` 或
``/lebai/io/set_ao``，并检查服务响应。请根据控制器选择设备、引脚和输出值。
下方示例写入 0 号引脚。

.. code-block:: bash

   rosrun lebai_tutorials io_example.py --device robot --pin 0 --digital 1
   rosrun lebai_tutorials io_example.py --device robot --pin 0 --analog 3.0

直接发送运动请求
~~~~~~~~~~~~~~~~

``move_example.py`` 可以通过 ``/lebai/motion/movej`` 发送六个关节位置（单位为
弧度），也可以通过 ``/lebai/motion/movel`` 发送按 ``x,y,z,rx,ry,rz`` 排列的
笛卡尔位姿。请根据机器人和工作空间选择合适的目标。此示例直接发送运动命令，
无 MoveIt 规划步骤。

.. code-block:: bash

   rosrun lebai_tutorials move_example.py --joints=-0.35,-1.0,1.2,-1.1,-0.6,0.0

脚本会打印返回的运动 ID。传入 ``--wait`` 时，脚本会调用阻塞式
``wait_move`` 服务。等待期间的调用限制见 :doc:`interfaces/services`。

MoveIt 示例准备
---------------

先按 :doc:`moveit` 启动 LM3。机械臂示例支持两种模式，夹爪示例需要
``has_gripper:=true``。

机械臂 MoveIt 示例
------------------

``moveit_manipulator_example.py`` 通过 ``moveit_commander`` 使用 LM3 的
``manipulator`` 规划组，支持带夹爪和仅机械臂两种模式。默认只做规划，传入
``--execute`` 可执行规划出的轨迹。

.. code-block:: bash

   rosrun lebai_tutorials moveit_manipulator_example.py

夹爪 MoveIt 示例
----------------

``moveit_gripper_amplitude_example.py`` 将开合幅度的百分比换算为夹爪主动关节
的角度，再通过 ``actionlib.SimpleActionClient`` 直接向夹爪控制器发送目标。
下方命令将夹爪移动到 50% 的开合幅度。

.. code-block:: bash

   rosrun lebai_tutorials moveit_gripper_amplitude_example.py --amplitude 50
