话题
====

参照 :doc:`../quickstart` 加载工作空间环境并启动驱动。以下示例使用默认
命名空间 ``lebai``。修改启动参数 ``namespace`` 后，请替换命令中的
``/lebai`` 前缀。``/tf`` 和 ``/tf_static`` 使用全局路径。

``rostopic echo -n 1`` 收到一条消息后退出。持续查看时可去掉 ``-n 1``。
带有 ``connected`` 字段的状态消息在 SDK 读取失败时将其设为 ``false``，
错误信息见 ``message`` 字段。驱动状态的发布频率可通过
:ref:`driver-status-rates` 配置。

机器人状态
----------

控制器状态
~~~~~~~~~~

话题 ``/lebai/status/robot`` 使用 ``lebai_interfaces/RobotState``，默认 10 Hz。
它提供控制器状态、急停原因和连接标志。

.. code-block:: bash

   rostopic echo -n 1 /lebai/status/robot

机械臂关节状态
~~~~~~~~~~~~~~

话题 ``/lebai/status/joint_states`` 使用 ``sensor_msgs/JointState``，默认 20 Hz。
它提供机械臂的关节名称及实测位置、速度和力矩。仅有机械臂的 LM3 也使用此话题。

.. code-block:: bash

   rostopic echo -n 1 /lebai/status/joint_states

关节运动状态
~~~~~~~~~~~~

话题 ``/lebai/status/joint_motion`` 使用 ``lebai_interfaces/JointMotion``，
默认 20 Hz。它提供实际和目标关节位置、速度、力矩及 TCP 位姿，以及实际法兰位姿。
TCP 和法兰位姿使用 ``lebai_interfaces/CartesianPose``，字段包括
``x``、``y``、``z``、``rx``、``ry`` 和 ``rz``。

.. code-block:: bash

   rostopic echo -n 1 /lebai/status/joint_motion

机器人模型与 TF
---------------

组合模型关节状态
~~~~~~~~~~~~~~~~

话题 ``/lebai/model/joint_states`` 使用 ``sensor_msgs/JointState``，默认 20 Hz。
它将机械臂与内置夹爪的主动关节状态合为一条消息，供机器人模型使用。

.. code-block:: bash

   rostopic echo -n 1 /lebai/model/joint_states

只要机械臂或夹爪的任一读取失败，驱动就会发布七个关节名、七个零位置以及空的
速度和力矩数组。此时时间戳仍表示发布时间，应把这条消息视为测量数据不可用。
默认的 MoveIt 启动配置仅接收组合模型的完整测量数据。仅凭新的时间戳或其他话题
的 ``connected`` 标志，无法确认机械臂具备执行条件。

动态 TF
~~~~~~~

话题 ``/tf`` 使用 ``tf2_msgs/TFMessage``。默认启动的 ``robot_state_publisher``
根据关节状态发布动态坐标变换。

.. code-block:: bash

   rostopic echo -n 1 /tf

静态 TF
~~~~~~~

话题 ``/tf_static`` 使用 ``tf2_msgs/TFMessage``，用于发布模型中固定关节的
坐标变换。

.. code-block:: bash

   rostopic echo -n 1 /tf_static

URDF 参数
~~~~~~~~~

使用默认的 ``driver.launch`` 时，可以通过 ROS 参数读取 URDF 模型。

.. code-block:: bash

   rosparam get /lebai/robot_description

I/O 状态
--------

话题 ``/lebai/io/state`` 使用 ``lebai_interfaces/IOState``，默认 10 Hz。
它提供所选设备的数字 I/O、模拟 I/O 和 DIO 模式。各组引脚数默认为 0，
此时对应的状态数组为空。可在 :ref:`driver-io-parameters` 中查看设备和
引脚数量参数。

.. code-block:: bash

   rostopic echo -n 1 /lebai/io/state

内置夹爪
--------

夹爪状态
~~~~~~~~

话题 ``/lebai/claw/state`` 使用 ``lebai_interfaces/ClawState``，默认 10 Hz。
它提供内置夹爪的力、开合幅度和夹持标志。

.. code-block:: bash

   rostopic echo -n 1 /lebai/claw/state

夹爪关节状态
~~~~~~~~~~~~

话题 ``/lebai/claw/joint_states`` 使用 ``sensor_msgs/JointState``，默认 10 Hz。
它将内置夹爪的开合幅度转换为模型主动关节的位置。

.. code-block:: bash

   rostopic echo -n 1 /lebai/claw/joint_states

串口夹爪状态
------------

话题 ``/lebai/gripper/state`` 使用 ``lebai_interfaces/GripperState``，默认
10 Hz。它由独立的串口夹爪节点发布，提供位置、力、速度和标定状态。
先按 :doc:`../quickstart` 启动 ``serial_gripper.launch``，再查看状态。

.. code-block:: bash

   rostopic echo -n 1 /lebai/gripper/state
