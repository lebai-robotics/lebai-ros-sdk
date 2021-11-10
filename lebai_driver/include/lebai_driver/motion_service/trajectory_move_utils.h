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
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>

namespace lebai_driver
{
    // bool geometryPoseToFloats(const geometry_msgs::Pose &pose, industrial::shared_types::shared_real *cartesian_pose)
    // {
    //     // using lebai::simple_message::motion::MoveJoint;
    //     *(cartesian_pose + 0) = pose.position.x;
    //     *(cartesian_pose + 1) = pose.position.y;
    //     *(cartesian_pose + 2) = pose.position.z;
    //     *(cartesian_pose + 3) = pose.orientation.x;
    //     *(cartesian_pose + 4) = pose.orientation.y;
    //     *(cartesian_pose + 5) = pose.orientation.z;
    //     *(cartesian_pose + 6) = pose.orientation.w;
    //     return true;
    // }
    bool geometryPoseToRepeatedDouble(const geometry_msgs::Pose &pose, google::protobuf::RepeatedField<double> *p)
    {
        tf2::Quaternion quat_tf;
        // geometry_msgs::Quaternion quat_msg = ...;

        tf2::convert(pose.orientation, quat_tf);
        tf2::Matrix3x3 m(quat_tf);
        double yaw, pitch,roll;
        m.getRPY(roll, pitch, yaw);
        p->Add(pose.position.x);
        p->Add(pose.position.y);
        p->Add(pose.position.z);
        p->Add(yaw);
        p->Add(pitch);
        p->Add(roll);
        return true;
    }

}
