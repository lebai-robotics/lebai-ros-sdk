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

#include "lebai_driver/robot_state/robot_state_handler.h"
#include "lebai_driver/robot_state/robot_state_interface.h"
#include <industrial_msgs/RobotStatus.h>
#include <industrial_msgs/RobotMode.h>

namespace lebai_driver
{
  bool RobotStateHandler::init(Stubs * stubs)
  {
    stubs_ = stubs;
    this->pub_robot_state_ = this->node_.advertise<industrial_msgs::RobotStatus>("robot_status", 1);
    return true;
  }


  void RobotStateHandler::run()
  {
    grpc::ClientContext context;
    google::protobuf::Empty req;
    robotc::RobotMode res;
    grpc::Status status;
    status = stubs_->robot_controller_stub_->GetRobotMode(&context, req, &res);
    if (status.ok())
    {
      industrial_msgs::RobotStatus robot_status;
      robot_status.header.stamp = ros::Time().now();

      if(res.mode() == 7)
      {
        robot_status.motion_possible.val = 0;
        robot_status.in_motion.val = 1;
        robot_status.e_stopped.val = 0;
        robot_status.drives_powered.val = 1;
        // robot_status.mode.val = industrial_msgs::RobotMode::AUTO;
      }
      else if(res.mode() == 5)
      {
        robot_status.motion_possible.val = 1;
        robot_status.in_motion.val = 0;
        robot_status.e_stopped.val = 0;
        robot_status.drives_powered.val = 1;
        // robot_status.mode.val = industrial_msgs::RobotMode::AUTO;
      }
      else if(res.mode() == 11)
      {
        robot_status.motion_possible.val = 0;
        robot_status.in_motion.val = 0;
        robot_status.e_stopped.val = 0;
        robot_status.drives_powered.val = 1;
        // robot_status.mode.val = industrial_msgs::RobotMode::MANUAL;
      }
      else if(res.mode() == 1)
      {
        robot_status.motion_possible.val = 0;
        robot_status.in_motion.val = 0;
        robot_status.e_stopped.val = 1;
        robot_status.drives_powered.val = 0;
      }
      else
      {
          robot_status.motion_possible.val = 0;
          robot_status.in_motion.val = 0;
          robot_status.e_stopped.val = 0;
          robot_status.drives_powered.val = 0;
          robot_status.mode.val = industrial_msgs::RobotMode::UNKNOWN;
      }
      this->pub_robot_state_.publish(robot_status);
    }
    else
    {
      ROS_ERROR("Failed to call `GetRobotMode`.");
      return;
    }
   
    return;
  }


} // namespace lebai_driver
