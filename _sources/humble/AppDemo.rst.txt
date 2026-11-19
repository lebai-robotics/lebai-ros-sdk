.. _humble_app_demo:

应用编程示例
============

以下给出构建一个简单应用的基本步骤。

.. note:: 
   完整源代码可在 ``lebai-ros-sdk`` 源代码中 `lebai_tutorials <https://github.com/lebai-robotics/lebai-ros-sdk/tree/galactic-dev/lebai_tutorials>`_ 目录中查看。


.. contents:: 目录
   :depth: 2
   :local:

创建 ``ROS 2`` 程序包
-----------------------------
.. code-block:: bash
   
   ros2 pkg create lebai_tutorials --build-type ament_cmake --dependencies rclpy rclcpp lebai_interfaces

在 ``package.xml`` 文件中自行设置 ``description``， ``maintainer``， ``license`` 等内容。


``c++`` 部分
-----------------------------

在 ``src`` 目录下，添加 ``move_example.cc`` 文件。

.. code-block:: bash

   touch src/move_example.cc

复制如下内容到 ``move_example.cc`` 文件中:

.. code-block:: cpp
  
  #include <rclcpp/rclcpp.hpp>
  #include <lebai_interfaces/srv/move_joint.hpp>
  #include <lebai_interfaces/srv/move_line.hpp>
  int main(int argc, char **argv)
  {
    rclcpp::init(argc, argv);
    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("move_example");
    // Create move joint service client.
    rclcpp::Client<lebai_interfaces::srv::MoveJoint>::SharedPtr move_joint_client =
        node->create_client<lebai_interfaces::srv::MoveJoint>("/motion_service/move_joint");
    // Wait for service.
    move_joint_client->wait_for_service();
    RCLCPP_INFO(node->get_logger(), "Move joint service exist.");
    // generate a move joint srv data.
    auto move_joint_req = std::make_shared<lebai_interfaces::srv::MoveJoint::Request>();
    move_joint_req->joint_pose = {-0.515705166127304, -1.383938292070577, 0.9317015810420413, -1.0843326694366626, -0.8334309368181174, -0.7919175817459623};
    move_joint_req->is_joint_pose = 1;
    move_joint_req->common.vel = 0.2;
    move_joint_req->common.acc = 1.0;
    // Call service.
    auto move_joint_result = move_joint_client->async_send_request(move_joint_req);
    if (rclcpp::spin_until_future_complete(node, move_joint_result) ==
        rclcpp::FutureReturnCode::SUCCESS)
    {
      RCLCPP_INFO(node->get_logger(), "Successed to call move joint");
    }
    else
    {
      RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call move joint");
    }
    // Create move line service client.
    rclcpp::Client<lebai_interfaces::srv::MoveLine>::SharedPtr move_line_client =
        node->create_client<lebai_interfaces::srv::MoveLine>("/motion_service/move_line");
    // Wait for service.
    move_line_client->wait_for_service();
    RCLCPP_INFO(node->get_logger(), "Move line service exist.");
    // generate a move line srv data.
    auto move_line_req = std::make_shared<lebai_interfaces::srv::MoveLine::Request>();
    move_line_req->joint_pose = {-1.9979141024218048, -1.1726324385393299, 0.9936360553529241, -1.0942076707586763, -0.849345987492431, -0.8172282647460754};;
    move_line_req->is_joint_pose = 1;
    move_line_req->common.vel = 0.2;
    move_line_req->common.acc = 1.0;
    // Call service.
    auto move_line_result = move_line_client->async_send_request(move_line_req);
    if (rclcpp::spin_until_future_complete(node, move_line_result) ==
        rclcpp::FutureReturnCode::SUCCESS)
    {
      RCLCPP_INFO(node->get_logger(), "Successed to call move line");
    }
    else
    {
      RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call move line");
    }
    rclcpp::shutdown();
    return 0;
  }


在 ``CMakeLists.txt`` 中添加如下内容：

.. code-block:: cmake

   ## after find_package...
   add_executable(move_example src/move_example.cc)
   ament_target_dependencies(move_example
   rclcpp lebai_interfaces)

   install(TARGETS
      move_example
      DESTINATION lib/${PROJECT_NAME}
   )

您可以尝试编译并运行

.. code-block:: bash
   
   # change to your own workspace.
   cd lebai_ws 
   colcon build

   # remember you need to run:
   # source lebai_ws/install/setup.bash.
   # you must run lebai-ros-sdk launch first:
   # ros2 launch lebai_lm3_support robot_interface_lm3.launch.py robot_ip:=xxx.xxx.xxx.xxx
   ros2 run lebai_tutorials move_example

``python`` 部分
-----------------------------

在 ``src`` 目录下，添加 ``python`` 模块目录和相应的文件。

.. code-block:: bash

   cd lebai_tutorials
   mkdir scripts
   touch scripts/move_example.py
   touch scripts/io_example.py
   touch scripts/joint_state_subscriber.py
   
``move_example.py`` 内容如下：

.. code-block:: python

   #!/usr/bin/env python3
   import rclpy
   from rclpy.node import Node
   from lebai_interfaces.srv import MoveJoint
   from lebai_interfaces.srv import MoveLine
   from geometry_msgs.msg import Point
   from geometry_msgs.msg import Quaternion

   class MoveExample(Node):
      def __init__(self):
         super().__init__('move_example')

      def SendMoveJoint(self):
         move_joint_srv = self.create_client(
               MoveJoint, '/motion_service/move_joint')
         while not move_joint_srv.wait_for_service(timeout_sec=1.0):
               self.get_logger().info('service "move_joint" not available, waiting...')
         req = MoveJoint.Request()
         req.is_joint_pose = True
         req.joint_pose = [-0.516, -1.384, 0.932, -1.084, -0.833, -0.792]
         req.common.vel = 0.1
         req.common.acc = 1.0
         req.common.radius = 0.0
         future = move_joint_srv.call_async(req)
         while rclpy.ok():
               rclpy.spin_once(self)
               if future.done():
                  try:
                     future.result()
                  except Exception as e:
                     self.get_logger().info(
                           'Service "move_joint" call failed %r' % (e,))
                  else:
                     self.get_logger().info(
                           'Service "move_joint" call succeed.')
                  break

      def SendMoveLine(self):
         move_line_srv = self.create_client(
               MoveLine, '/motion_service/move_line')
         while not move_line_srv.wait_for_service(timeout_sec=1.0):
               self.get_logger().info('service "move_line" not available, waiting...')
         req = MoveLine.Request()
         req.is_joint_pose = False
         req.cartesian_pose.position.x = 0.022
         req.cartesian_pose.position.y = 0.473
         req.cartesian_pose.position.z = 0.431
         req.cartesian_pose.orientation.x = 0.918
         req.cartesian_pose.orientation.y = 0.128
         req.cartesian_pose.orientation.z = -0.364
         req.cartesian_pose.orientation.w = -0.091
         req.common.vel = 0.1
         req.common.acc = 1.0
         req.common.radius = 0.0
         future = move_line_srv.call_async(req)
         while rclpy.ok():
               rclpy.spin_once(self)
               if future.done():
                  try:
                     future.result()
                  except Exception as e:
                     self.get_logger().info(
                           'Service "move_line" call failed %r' % (e,))
                  else:
                     self.get_logger().info(
                           'Service "move_line" call succeed.')
                  break


   def Run():
      move_example = MoveExample()
      move_example.SendMoveJoint()
      move_example.SendMoveLine()
      return


   def main():
      rclpy.init()
      Run()
      rclpy.shutdown()


   if __name__ == '__main__':
      main()

``io_example.py`` 内容如下：

.. code-block:: python

   #!/usr/bin/env python3

   import rclpy
   from rclpy.node import Node
   from lebai_interfaces.srv import SetDO
   from lebai_interfaces.srv import SetAO


   class IOExample(Node):
      def __init__(self):
         super().__init__('io_example')

      def SetDO(self):
         srv = self.create_client(
               SetDO, '/io_service/set_robot_do')
         while not srv.wait_for_service(timeout_sec=1.0):
               self.get_logger().info('service "set_robot_do" not available, waiting...')
         req = SetDO.Request()
         req.pin = 0
         req.value = True
         future = srv.call_async(req)
         while rclpy.ok():
               rclpy.spin_once(self)
               if future.done():
                  try:
                     future.result()
                  except Exception as e:
                     self.get_logger().info(
                           'Service "set_robot_do" call failed %r' % (e,))
                  else:
                     self.get_logger().info(
                           'Service "set_robot_do" call succeed.')
                  break

      def SetAO(self):
         srv = self.create_client(
               SetAO, '/io_service/set_robot_ao')
         while not srv.wait_for_service(timeout_sec=1.0):
               self.get_logger().info('service "set_robot_ao" not available, waiting...')
         req = SetAO.Request()
         req.pin = 0
         req.value = 3.0
         future = srv.call_async(req)
         while rclpy.ok():
               rclpy.spin_once(self)
               if future.done():
                  try:
                     future.result()
                  except Exception as e:
                     self.get_logger().info(
                           'Service "set_robot_ao" call failed %r' % (e,))
                  else:
                     self.get_logger().info(
                           'Service "set_robot_ao" call succeed.')
                  break


   def Run():
      io_example = IOExample()
      io_example.SetDO()
      io_example.SetAO()
      # SendMoveCircle()
      return


   def main():
      rclpy.init()
      Run()
      rclpy.shutdown()


   if __name__ == '__main__':
      main()

``joint_state_subscriber.py`` 内容如下：

.. code-block:: python

   #!/usr/bin/env python3

   import rclpy
   from rclpy.node import Node
   from sensor_msgs.msg import JointState


   class JointStateSubscriber(Node):

      def __init__(self):
         super().__init__('joint_state_subscriber')
         self.subscription = self.create_subscription(
               JointState,
               'joint_states',
               self.joint_state_callback,
               10)
         self.subscription  # prevent unused variable warning

      def joint_state_callback(self, msg: JointState):
         self.get_logger().info('Joint position: "%s"' % msg.position)


   def main(args=None):
      rclpy.init(args=args)
      joint_state_subscriber = JointStateSubscriber()
      rclpy.spin(joint_state_subscriber)
      joint_state_subscriber.destroy_node()
      rclpy.shutdown()


   if __name__ == '__main__':
      main()


在 ``CMakeLists.txt`` 中添加如下内容：

.. code-block:: cmake

   ## after find_package...
   install(PROGRAMS
      scripts/move_example.py
      scripts/io_example.py
      scripts/joint_state_subscriber.py
      DESTINATION lib/${PROJECT_NAME}
   )

您可以尝试编译并运行

.. code-block:: bash
   
   # change to your own workspace.
   cd lebai_ws 
   colcon build

   # remember you need to run:
   # source lebai_ws/install/setup.bash.
   # you must run lebai-ros-sdk launch first:
   # ros2 launch lebai_lm3_support robot_interface_lm3.launch.py robot_ip:=xxx.xxx.xxx.xxx
   ros2 run lebai_tutorials move_example.py
   ros2 run lebai_tutorials io_example.py
   ros2 run lebai_tutorials joint_state_subscriber.py
