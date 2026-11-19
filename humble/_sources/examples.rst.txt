示例
====

``lebai_tutorials`` 提供可以直接运行的 Python 示例。运行前先构建工作空间：

.. code-block:: bash

   cd ~/lebai/lebai_ws
   source /opt/ros/humble/setup.bash
   colcon build --symlink-install
   source install/setup.bash

基础驱动示例
------------

基础示例需要先启动 ``lebai_driver``：

.. code-block:: bash

   ros2 launch lebai_driver driver.launch.py robot_ip:=127.0.0.1 simulator:=true

运行关节运动和直线运动示例：

.. code-block:: bash

   ros2 run lebai_tutorials move_example.py

运行 IO 示例：

.. code-block:: bash

   ros2 run lebai_tutorials io_example.py

``move_example.py`` 和 ``io_example.py`` 使用固定的 ``/lebai/...`` service
名称，不提供 ``--namespace`` 参数。service 返回的 ``Result.success`` 为
``false`` 时，脚本以非零状态退出；service 尚未出现时，脚本会继续等待。
``io_example.py`` 当前发送 legacy 小写 ``robot``，因此仅适合目标确实为
``ROBOT`` 的兼容场景；自定义 IO 请求应使用大写规范名 ``ROBOT``、
``FLANGE`` 等，避免 SDK 的默认回退。

订阅关节状态：

.. code-block:: bash

   ros2 run lebai_tutorials joint_state_subscriber.py

``joint_state_subscriber.py`` 同样固定订阅
``/lebai/status/joint_states``，不提供 ``--namespace`` 参数；它会持续运行并
打印关节位置，直到用户中断进程。

MoveIt 示例准备
---------------

MoveIt 示例需要先启动 MoveIt 配置。使用 gripper 示例时必须启用 gripper：

.. code-block:: bash

   ros2 launch lebai_lm3_moveit_config lm3.launch.py \
     robot_ip:=127.0.0.1 \
     simulator:=true \
     has_gripper:=true

连接真实控制器时，将 ``robot_ip`` 改成控制器 IP，并省略 ``simulator:=true``。

机械臂 MoveIt 示例
------------------

``moveit_manipulator_example.py`` 通过 MoveIt 的 ``manipulator`` group 发送
关节空间目标。默认会规划并执行轨迹：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_manipulator_example.py

只规划、不执行：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_manipulator_example.py --plan-only

指定 6 个关节目标，单位为弧度：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_manipulator_example.py \
     --joints="-0.35,-1.0,1.2,-1.1,-0.6,0.0"

该脚本默认在 ``lebai`` 命名空间使用相对 action ``move_action``，解析为
``/lebai/move_action``。MoveIt launch 使用其他命名空间时传入相同值：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_manipulator_example.py \
     --namespace robot_1

action server 不可用、goal 被拒绝、等待超时或 MoveIt 返回错误时，脚本都以
非零状态退出。

gripper MoveIt 示例
-------------------

``moveit_gripper_amplitude_example.py`` 使用 MoveIt gripper 控制器 action，并用
claw 幅度百分比设置 gripper。幅度范围是 ``0`` 到 ``100``：

.. code-block:: bash

   ros2 run lebai_tutorials moveit_gripper_amplitude_example.py --amplitude 50

幅度会映射到 gripper 主动关节 ``gripper_r_joint1``：

.. code-block:: text

   gripper_r_joint1 = amplitude / 100 * pi / 3

因此 ``--amplitude 0`` 对应关闭，``--amplitude 100`` 对应打开。

该脚本默认使用相对 action
``lebai_gripper_controller/gripper_cmd``，在默认命名空间解析为
``/lebai/lebai_gripper_controller/gripper_cmd``。自定义命名空间同样使用
``--namespace robot_1``。action server 不可用、goal 被拒绝、等待超时或
gripper 未到达目标时，脚本以非零状态退出。
