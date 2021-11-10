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

#include "lebai_driver/system_service/system_service.h"

namespace lebai_driver
{
    SystemService::SystemService()
    : node_("~")
    {
        this->srv_emergency_stop_ = this->node_.advertiseService("emergency_stop", &SystemService::emergencyStop, this);
        this->srv_power_on_ = this->node_.advertiseService("power_on", &SystemService::powerOn, this);
        this->srv_power_off_ = this->node_.advertiseService("power_off", &SystemService::powerOff, this);
        this->srv_enable_ = this->node_.advertiseService("enable", &SystemService::enable, this);
        this->srv_disable_ = this->node_.advertiseService("disable", &SystemService::disable, this);
        this->srv_pause_motion_ = this->node_.advertiseService("pause_motion", &SystemService::pauseMotion, this);
        this->srv_resume_motion_ = this->node_.advertiseService("resume_motion", &SystemService::resumeMotion, this);
        this->srv_abort_motion_ = this->node_.advertiseService("abort_motion", &SystemService::abortMotion, this);
        this->srv_entry_teach_mode_ = this->node_.advertiseService("entry_teach_mode", &SystemService::entryTeacMode, this);
        this->srv_exit_teach_mode_ = this->node_.advertiseService("exit_teach_mode", &SystemService::exitTeacMode, this);
        this->srv_turn_off_robot_ = this->node_.advertiseService("turn_off_robot", &SystemService::turnOffRobot, this);
    }

    bool SystemService::init()
    {
        grpc_init();
        std::string default_ip = "";
        std::string ip;

        int default_rcs_port = 5181;
        int rcs_port;

        // override IP/port with ROS params, if available
        ros::param::param<std::string>("robot_ip_address", ip, default_ip);
        ros::param::param<int>("~rcs_port", rcs_port, default_rcs_port);

        // check for valid parameter values
        if (ip.empty())
        {
            ROS_ERROR("No valid robot IP address found.  Please set ROS 'robot_ip_address' param");
            return false;
        }

        if (rcs_port <= 0)
        {
            ROS_ERROR("No valid robot IP rcs port found.  Please set ROS '~rcs_port' param");
            return false;
        }

        std::string rcs_target = ip + ":" + std::to_string(rcs_port);
        ROS_DEBUG("rcs_target: %s\n", rcs_target.c_str());
        stubs_.robot_controller_stub_ = robotc::RobotController::NewStub(grpc::CreateChannel(rcs_target, grpc::InsecureChannelCredentials()));

        return true;
    }

    bool SystemService::emergencyStop(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->EStop(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `EStop`.");
            return false;
        }
        return true;
    }
    bool SystemService::powerOn(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->StartSys(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `StartSys`.");
            return false;
        }
        return true;
    }
    bool SystemService::powerOff(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->StopSys(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `StopSys`.");
            return false;
        }
        return true;
    }
    bool SystemService::enable(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->StartSys(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `StartSys`.");
            return false;
        }
        return true;
    }
    bool SystemService::disable(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->StopSys(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `StopSys`.");
            return false;
        }
        return true;
    }
    bool SystemService::pauseMotion(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->Pause(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `Pause`.");
            return false;
        }
        return true;
    }
    bool SystemService::resumeMotion(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->Resume(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `Resume`.");
            return false;
        }
        return true;
    }
    bool SystemService::abortMotion(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->Stop(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `Stop`.");
            return false;
        }
        return true;
    }
    bool SystemService::entryTeacMode(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->TeachMode(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `TeachMode`.");
            return false;
        }
        return true;
    }
    bool SystemService::exitTeacMode(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->EndTeachMode(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `EndTeachMode`.");
            return false;
        }
        return true;
    }
    bool SystemService::turnOffRobot(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res)
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_.robot_controller_stub_->StopSys(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `StopSys`.");
            return false;
        }
        return true;
    }


}
