/**
* Copyright (c) 2021, Lebai Robotic Co., Ltd.
* All rights reserved.
* 
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
* * Redistributions of source code must retain the above copyright
*   notice, this list of conditions and the following disclaimer.
* * Redistributions in binary form must reproduce the above copyright
*   notice, this list of conditions and the following disclaimer in the
*   documentation and/or other materials provided with the distribution.
* * Neither the name of the University of California nor the
*   names of its contributors may be used to endorse or promote products
*   derived from this software without specific prior written permission.
* 
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
* ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE REGENTS OF THE UNIVERSITY OF CALIFORNIA BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
* GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
* HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
* LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
* THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*  
*/

#include "lebai_driver/robot_state/joint_feedback_handler.h"
#include "lebai_driver/robot_state/robot_state_interface.h"
#include <control_msgs/FollowJointTrajectoryFeedback.h>
#include <sensor_msgs/JointState.h>

namespace lebai_driver
{
  bool JointFeedbackHandler::init(Stubs *stubs, const std::vector<std::string> &joint_names, const std::vector<std::string> &gripper_joint_names)
  {
    stubs_ = stubs;
    this->pub_joint_sensor_state_ = this->node_.advertise<sensor_msgs::JointState>("joint_states", 1);
    this->pub_joint_control_state_ =
        this->node_.advertise<control_msgs::FollowJointTrajectoryFeedback>("feedback_states", 1);

    joint_names_ = joint_names;
    gripper_joint_names_ = gripper_joint_names;

    all_joint_names_ = joint_names_;
    if (!gripper_joint_names_.empty())
    {
      all_joint_names_.insert(all_joint_names_.end(), gripper_joint_names_.begin(), gripper_joint_names_.end());
    }
    return true;
  }

  bool JointFeedbackHandler::updateJointState()
  {
    google::protobuf::Empty request;
    robotc::Joint joint_response;
    robotc::CmdId reply;

    std::vector<double> all_joint_pos;
    std::vector<double> all_joint_vel;
    std::vector<double> all_joint_effort;
    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    grpc::ClientContext position_context;
    // ROS_ERROR("BBB");
    grpc::Status status;
    status = stubs_->robot_controller_stub_->GetActualJointPositions(&position_context, request, &joint_response);
    if (status.ok())
    {
      // ROS_ERROR("DDD");
      // ROS_ERROR("joints_size %d\n",joint_response.joints_size());
      for (size_t i = 0; i < joint_response.joints_size(); ++i)
      {
        all_joint_pos.push_back(joint_response.joints(i));
      }
    }
    else
    {
      ROS_ERROR("Failed to call `GetActualJointPositions`.");
      return false;
    }
    grpc::ClientContext vel_context;
    // context2.crea
    status = stubs_->robot_controller_stub_->GetActualJointSpeeds(&vel_context, request, &joint_response);
    if (status.ok())
    {
      for (size_t i = 0; i < joint_response.joints_size(); ++i)
      {
        all_joint_vel.push_back(joint_response.joints(i));
      }
    }
    else
    {
      ROS_ERROR("Failed to call `GetActualJointSpeeds`.");
    }

    //TODO: gRPC not implemented. add this later.
    // grpc::ClientContext torque_context;
    // status = stubs_->robot_controller_stub_->GetJointTorques(&torque_context, request, &joint_response);
    // if (status.ok())
    // {
    //   for(size_t i = 0; i < joint_response.joints_size(); ++i)
    //   {
    //     all_joint_effort.push_back(joint_response.joints(i));
    //   }
    // }
    // else
    // {
    //   ROS_ERROR("Failed to call `GetJointTorques`.");
    // }
    control_msgs::FollowJointTrajectoryFeedback control_state;
    control_state.header.stamp = ros::Time::now();
    control_state.joint_names = joint_names_;
    control_state.actual.positions = all_joint_pos;
    this->pub_joint_control_state_.publish(control_state);

    // std::cout<<"joint_names_ "<<joint_names_.size()<<"\n";

    sensor_msgs::JointState sensor_state;
    sensor_state.header.stamp = ros::Time::now();
    sensor_state.name = all_joint_names_;
    sensor_state.position = all_joint_pos;
    sensor_state.velocity = all_joint_vel;
    sensor_state.effort = all_joint_effort;

    // std::cout<<"all_joint_names_ "<<all_joint_names_.size()<<"\n";

    if (!gripper_joint_names_.empty())
    {
      double gripper_position = 0.0;
      {
        google::protobuf::Empty req;
        robotc::Amplitude res;
        grpc::ClientContext context;
        status = stubs_->robot_controller_stub_->GetClawAmplitude(&context, req, &res);
        if (status.ok())
        {
          gripper_position = 60.0 / 180.0 * M_PI * res.amplitude() / 100.0;
        }
        else
        {
          gripper_position = 0.0;
        }
        std::vector<double> all_gripper_position = {gripper_position, -gripper_position, -gripper_position, gripper_position, -gripper_position, -gripper_position};
        std::vector<double> all_gripper_velocity = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
        std::vector<double> all_gripper_effort = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
        sensor_state.position.insert(sensor_state.position.end(), all_gripper_position.begin(), all_gripper_position.end());
        sensor_state.velocity.insert(sensor_state.velocity.end(), all_gripper_velocity.begin(), all_gripper_velocity.end());
        sensor_state.effort.insert(sensor_state.effort.end(), all_gripper_effort.begin(), all_gripper_effort.end());
      }     
    }
    this->pub_joint_sensor_state_.publish(sensor_state);

    return true;
  }

  void JointFeedbackHandler::run()
  {
    updateJointState();
  }

} // namespace lebai_driver
