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

#include "ros/ros.h"
#include <lebai_msgs/MoveJoint.h>
#include <lebai_msgs/MoveLine.h>
#include <lebai_msgs/MoveCircle.h>
#include <lebai_msgs/SpeedJoint.h>
#include <lebai_msgs/SpeedLine.h>
#include <lebai_msgs/UntilInfo.h>
#include "lebai_driver/stubs.h"
#include <robot_controller.grpc.pb.h>
#include <motion.pb.h>

namespace lebai_driver
{

    class TrajectoryMove
    {

    public:
        TrajectoryMove();
        ~TrajectoryMove();
        bool init(Stubs * stubs);
        bool moveJoint(lebai_msgs::MoveJoint::Request &req, lebai_msgs::MoveJoint::Response &res);
        bool moveLine(lebai_msgs::MoveLine::Request &req, lebai_msgs::MoveLine::Response &res);
        bool moveCircle(lebai_msgs::MoveCircle::Request &req, lebai_msgs::MoveCircle::Response &res);
        bool speedJoint(lebai_msgs::SpeedJoint::Request &req, lebai_msgs::SpeedJoint::Response &res);
        bool speedLine(lebai_msgs::SpeedLine::Request &req, lebai_msgs::SpeedLine::Response &res);

        bool sendMoveJointToRobot(robotc::MoveJRequest & grpc_req);
        bool sendMoveLineToRobot(robotc::MoveLRequest & grpc_req);
        bool sendMoveCircleToRobot(robotc::MoveCRequest & grpc_req);
        bool sendSpeedJointToRobot(robotc::SpeedJRequest & grpc_req);
        bool sendSpeedLineToRobot(robotc::SpeedLRequest & grpc_req);

        // void robotStatusCB(const industrial_msgs::RobotStatusConstPtr &msg);

        // bool stopMotionCB(industrial_msgs::StopMotion::Request &req,
        //                   industrial_msgs::StopMotion::Response &res) final;

    protected:
        // bool untilInfoToSimpleMsg(const lebai_msgs::UntilInfo &, UntilInfo &);
        ros::NodeHandle node_;
        Stubs * stubs_;

        ros::ServiceServer move_joint_service_;
        ros::ServiceServer move_line_service_;
        ros::ServiceServer move_circle_service_;
        ros::ServiceServer speed_joint_service_;
        ros::ServiceServer speed_line_service_;
    };

} // namespace lebai_driver
