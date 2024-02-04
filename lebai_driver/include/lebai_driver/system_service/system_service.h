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
#include <std_srvs/Empty.h>
#include "lebai_driver/stubs.h"

namespace lebai_driver
{

    class SystemService
    {

    public:
        SystemService();
        virtual ~SystemService()
        {
        };
        Stubs *getStubs();
        bool init();
        void run()
        {
            ros::spin();
        }

    protected:
        bool emergencyStop(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool powerOn(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool powerOff(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool enable(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool disable(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool pauseMotion(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool resumeMotion(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool abortMotion(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool entryTeacMode(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool exitTeacMode(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);
        bool turnOffRobot(std_srvs::Empty::Request &req, std_srvs::Empty::Response &res);

        Stubs stubs_;
        ros::NodeHandle node_;

        ros::ServiceServer srv_emergency_stop_;
        ros::ServiceServer srv_power_on_;
        ros::ServiceServer srv_power_off_;
        ros::ServiceServer srv_enable_;
        ros::ServiceServer srv_disable_;
        ros::ServiceServer srv_pause_motion_;
        ros::ServiceServer srv_resume_motion_;
        ros::ServiceServer srv_abort_motion_;
        ros::ServiceServer srv_entry_teach_mode_;
        ros::ServiceServer srv_exit_teach_mode_;
        ros::ServiceServer srv_turn_off_robot_;
    };
} // namespace lebai_driver