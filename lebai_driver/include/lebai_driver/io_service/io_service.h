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

#pragma once

#include <map>
#include <vector>
#include <string>
#include <ros/ros.h>
#include "lebai_driver/stubs.h"

#include "lebai_msgs/SetDO.h"
#include "lebai_msgs/SetAO.h"
#include "lebai_msgs/SetAMode.h"
#include "lebai_msgs/SetGripper.h"

namespace lebai_driver
{
    class IOService
    {

    public:
        IOService();

        bool init();

        virtual ~IOService()
        {
        }

        void run()
        {
            ros::spin();
        }

    protected:

        ros::NodeHandle node_;
        Stubs stubs_;

        ros::ServiceServer srv_set_robot_do_;         // set robot do srv
        ros::ServiceServer srv_set_robot_ao_;         // set robot_ao srv
        ros::ServiceServer srv_set_robot_ao_mode_;    // set robot ao mode srv
        ros::ServiceServer srv_set_robot_ai_mode_;    // set robot ai mode srv
        ros::ServiceServer srv_set_flange_do_;        // set flange do srv
        ros::ServiceServer srv_set_gripper_position_; // set gripper position srv
        ros::ServiceServer srv_set_gripper_force_;    // set gripper force srv

    protected:
        bool setRobotDOCB(lebai_msgs::SetDO::Request &req, lebai_msgs::SetDO::Response &res);
        bool setRobotAOCB(lebai_msgs::SetAO::Request &req, lebai_msgs::SetAO::Response &res);
        bool setRobotAOModeCB(lebai_msgs::SetAMode::Request &req, lebai_msgs::SetAMode::Response &res);
        bool setRobotAIModeCB(lebai_msgs::SetAMode::Request &req, lebai_msgs::SetAMode::Response &res);
        bool setFlangeDOCB(lebai_msgs::SetDO::Request &req, lebai_msgs::SetDO::Response &res);
        bool setGripperPositionCB(lebai_msgs::SetGripper::Request &req, lebai_msgs::SetGripper::Response &res);
        bool setGripperForceCB(lebai_msgs::SetGripper::Request &req, lebai_msgs::SetGripper::Response &res);
        // bool setFlangeDOCB(lebai_msgs::SetDO::Request &req, lebai_msgs::SetDO::Response &res);
    };
} // namespace lebai_driver
