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

#include "lebai_driver/robot_state/io_status_handler.h"
#include "lebai_driver/robot_state/robot_state_interface.h"
#include <lebai_msgs/IOStatus.h>

// using namespace lebai::simple_message;

namespace lebai_driver
{
  bool IOStatusHandler::init(Stubs *stubs)
  {
    stubs_ = stubs;
    this->pub_io_status_ = this->node_.advertise<lebai_msgs::IOStatus>("io_status", 1);
  }

  void IOStatusHandler::run()
  {
    lebai_msgs::IOStatus io_msg;

    grpc::ClientContext context;
    std::unique_ptr<::grpc::ClientReaderWriter<::robotc::RobotDataCmd, ::robotc::IO>> stream = stubs_->robot_controller_stub_->GetRobotIOData(&context);
    robotc::IO io_data;
    robotc::RobotDataCmd cmd;
    stream->Write(cmd);
    stream->WritesDone();
    if (!stream->Read(&io_data))
    {
      ROS_ERROR("Failed to call `GetRobotIOData`\n");
      return;
    }
    stream->Finish();
    //robot dio
    for (size_t i = 0; i < io_data.robotdioout_size(); ++i)
    {
      io_msg.robot_dout.push_back(io_data.robotdioout(i).value());
    }
    for (size_t i = 0; i < io_data.robotdioin_size(); ++i)
    {
      io_msg.robot_din.push_back(io_data.robotdioin(i).value());
    }
    //robot aio
    for (size_t i = 0; i < io_data.robotaioout_size(); ++i)
    {
      io_msg.robot_aout.push_back(io_data.robotaioout(i).value());
    }
    for (size_t i = 0; i < io_data.robotaioin_size(); ++i)
    {
      io_msg.robot_ain.push_back(io_data.robotaioin(i).value());
    }
    //robot aio mode
    io_msg.robot_ain_type.resize(io_msg.robot_din.size());
    for (size_t i = 0; i < io_msg.robot_ain_type.size(); ++i)
    {
      robotc::IOPin req;
      req.set_pin(i);
      robotc::AIO res;
      grpc::ClientContext context;
      grpc::Status status;
      status = stubs_->robot_controller_stub_->GetAInMode(&context, req, &res);
      if (status.ok())
      {
        io_msg.robot_ain_type[i] = res.value();
      }
      else
      {
        ROS_ERROR("Failed to call `GetAInMode`.");
      }
    }

    io_msg.robot_aout_type.resize(io_msg.robot_aout.size());
    for (size_t i = 0; i < io_msg.robot_aout_type.size(); ++i)
    {
      robotc::IOPin req;
      req.set_pin(i);
      robotc::AIO res;
      grpc::ClientContext context;
      grpc::Status status;
      status = stubs_->robot_controller_stub_->GetAOutMode(&context, req, &res);
      if (status.ok())
      {
        io_msg.robot_aout_type[i] = res.value();
      }
      else
      {
        ROS_ERROR("Failed to call `GetAOutMode`.");
      }
    }

    //tcp dio
    for (size_t i = 0; i < io_data.tcpdioin_size(); ++i)
    {
      io_msg.flange_din.push_back(io_data.tcpdioin(i).value());
    }
    for (size_t i = 0; i < io_data.tcpdioout_size(); ++i)
    {
      io_msg.flange_dout.push_back(io_data.tcpdioout(i).value());
    }
    this->pub_io_status_.publish(io_msg);
    return;
  }

} // namespace lebai_driver
