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

#include "lebai_driver/robot_state/gripper_status_handler.h"
#include "lebai_driver/robot_state/robot_state_interface.h"
#include <lebai_msgs/GripperStatus.h>

namespace lebai_driver
{

  bool GripperStatusHandler::init(Stubs *stubs)
  {
    stubs_ = stubs;
    this->pub_gripper_status_ = this->node_.advertise<lebai_msgs::GripperStatus>("gripper_status", 1);
    return true;
  }

  void GripperStatusHandler::run()
  {
    lebai_msgs::GripperStatus gripper_status;
    grpc::Status status;
    {
      google::protobuf::Empty req;
      robotc::Amplitude res;
      grpc::ClientContext context;
      status = stubs_->robot_controller_stub_->GetClawAmplitude(&context, req, &res);
      if (status.ok())
      {
        gripper_status.position = res.amplitude();
      }
      else
      {
        ROS_ERROR("Failed to call `GetClawAmplitude`.");
        return;
      }
    }

    {
      google::protobuf::Empty req;
      robotc::HoldOn res;
      grpc::ClientContext context;
      status = stubs_->robot_controller_stub_->GetClawHoldOn(&context, req, &res);
      if (status.ok())
      {
        gripper_status.hold_on = res.hold_on();
      }
      else
      {
        ROS_ERROR("Failed to call `GetClawHoldOn`.");
        return;
      }
    }

    this->pub_gripper_status_.publish(gripper_status);
    return;
  }

} // namespace industrial_robot_client
