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

#include "lebai_driver/io_service/io_service.h"
#include <industrial_msgs/ServiceReturnCode.h>

namespace lebai_driver
{
    IOService::IOService()
        : node_("~")
    {
        this->srv_set_robot_do_ = this->node_.advertiseService("set_robot_do", &IOService::setRobotDOCB, this);
        this->srv_set_robot_ao_ = this->node_.advertiseService("set_robot_ao", &IOService::setRobotAOCB, this);
        this->srv_set_robot_ao_mode_ = this->node_.advertiseService("set_robot_ao_mode", &IOService::setRobotAOModeCB, this);
        this->srv_set_robot_ai_mode_ = this->node_.advertiseService("set_robot_ai_mode", &IOService::setRobotAIModeCB, this);
        this->srv_set_flange_do_ = this->node_.advertiseService("set_flange_do", &IOService::setFlangeDOCB, this);
        this->srv_set_gripper_position_ = this->node_.advertiseService("set_gripper_position", &IOService::setGripperPositionCB, this);
        this->srv_set_gripper_force_ = this->node_.advertiseService("set_gripper_force", &IOService::setGripperForceCB, this);
    }
    bool IOService::init()
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

    bool IOService::setRobotDOCB(lebai_msgs::SetDO::Request &req, lebai_msgs::SetDO::Response &res)
    {
        grpc::ClientContext context;
        robotc::DIO grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        
        grpc_req.set_pin(req.pin);
        grpc_req.set_value(req.value);
        status = stubs_.robot_controller_stub_->SetDIO(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
            res.code.val = industrial_msgs::ServiceReturnCode::SUCCESS;
        }
        else
        {
            ROS_ERROR("Failed to call `SetDIO`.");
            return false;
        }
        return true;
    }

    bool IOService::setRobotAOCB(lebai_msgs::SetAO::Request &req, lebai_msgs::SetAO::Response &res)
    {
        grpc::ClientContext context;
        robotc::AIO grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;        
        grpc_req.set_pin(req.pin);
        grpc_req.set_value(req.value);
        status = stubs_.robot_controller_stub_->SetAIO(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
            res.code.val = industrial_msgs::ServiceReturnCode::SUCCESS;
        }
        else
        {
            ROS_ERROR("Failed to call `SetAIO`.");
            return false;
        }
        return true;
    }

    bool IOService::setRobotAOModeCB(lebai_msgs::SetAMode::Request &req, lebai_msgs::SetAMode::Response &res)
    {
        grpc::ClientContext context;
        robotc::AIO grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        
        grpc_req.set_pin(req.pin);
        grpc_req.set_value(req.mode);
        status = stubs_.robot_controller_stub_->SetAOutMode(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
            res.code.val = industrial_msgs::ServiceReturnCode::SUCCESS;
        }
        else
        {
            ROS_ERROR("Failed to call `SetAOutMode`.");
            return false;
        }
        return true;
    }

    bool IOService::setRobotAIModeCB(lebai_msgs::SetAMode::Request &req, lebai_msgs::SetAMode::Response &res)
    {
        grpc::ClientContext context;
        robotc::AIO grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        
        grpc_req.set_pin(req.pin);
        grpc_req.set_value(req.mode);
        status = stubs_.robot_controller_stub_->SetAInMode(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
            res.code.val = industrial_msgs::ServiceReturnCode::SUCCESS;
        }
        else
        {
            ROS_ERROR("Failed to call `SetAInMode`.");
            return false;
        }
        return true;
    }

    bool IOService::setFlangeDOCB(lebai_msgs::SetDO::Request &req, lebai_msgs::SetDO::Response &res)
    {
        grpc::ClientContext context;
        robotc::DIO grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        
        grpc_req.set_pin(req.pin);
        grpc_req.set_value(req.value);
        status = stubs_.robot_controller_stub_->SetTcpDIO(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
            res.code.val = industrial_msgs::ServiceReturnCode::SUCCESS;
        }
        else
        {
            ROS_ERROR("Failed to call `SetTcpDIO`.");
            return false;
        }
        return true;
    }

    bool IOService::setGripperPositionCB(lebai_msgs::SetGripper::Request &req, lebai_msgs::SetGripper::Response &res)
    {
        grpc::ClientContext context;
        robotc::Amplitude grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        
        grpc_req.set_amplitude(req.val);
        status = stubs_.robot_controller_stub_->SetClawAmplitude(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
            res.ret = true;
        }
        else
        {
            ROS_ERROR("Failed to call `SetClawAmplitude`.");
            return false;
        }
        return true;
    }

    bool IOService::setGripperForceCB(lebai_msgs::SetGripper::Request &req, lebai_msgs::SetGripper::Response &res)
    {
        grpc::ClientContext context;
        robotc::Force grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        
        grpc_req.set_force(req.val);
        status = stubs_.robot_controller_stub_->SetClawForce(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
            res.ret = true;
        }
        else
        {
            ROS_ERROR("Failed to call `SetClawForce`.");
            return false;
        }
        return true;  
    }

}