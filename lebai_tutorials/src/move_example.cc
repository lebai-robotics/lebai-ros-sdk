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