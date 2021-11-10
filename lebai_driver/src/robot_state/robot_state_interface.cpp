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

#include <industrial_utils/param_utils.h>
#include "lebai_driver/robot_state/robot_state_interface.h"

namespace lebai_driver
{

    RobotStateInterface::RobotStateInterface()
    {
    }

    Stubs * RobotStateInterface::getStubs()
    {
        return &stubs_;
    }

    bool RobotStateInterface::init()
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

        if (!industrial_utils::param::getJointNames("controller_joint_names", "robot_description", joint_names_))
        {
            ROS_ERROR("Failed to initialize joint_names.  Aborting");
            return false;
        }
        

        std::vector<std::string> default_gripper_joint_names;
        ros::param::param<std::vector<std::string>>("gripper_joint_names", gripper_joint_names_, default_gripper_joint_names);



        std::string rcs_target = ip+":"+std::to_string(rcs_port);
        ROS_DEBUG("rcs_target: %s\n",rcs_target.c_str());
        stubs_.robot_controller_stub_ = robotc::RobotController::NewStub(grpc::CreateChannel(rcs_target, grpc::InsecureChannelCredentials()));
        return true;
    }


    void RobotStateInterface::run()
    {
        // manager_.spin();
        for(auto && s :  handlers_)
        {
            s->run();
        }
    }

} // lebai
