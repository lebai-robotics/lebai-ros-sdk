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


#include "lebai_driver/robot_state/robot_state_interface.h"
#include "lebai_driver/robot_state/joint_feedback_handler.h"
#include "lebai_driver/robot_state/io_status_handler.h"
#include "lebai_driver/robot_state/gripper_status_handler.h"
#include "lebai_driver/robot_state/robot_state_handler.h"

using namespace lebai_driver;

int main(int argc, char **argv)
{
    // initialize node
    ros::init(argc, argv, "state_interface");

    // launch the default Robot State Interface connection/handlers
    RobotStateInterface rsi;
    if (!rsi.init())
    {
        return 0;
    }



    std::unique_ptr<JointFeedbackHandler> joint_feedback_handler;
    joint_feedback_handler.reset(new JointFeedbackHandler());
    joint_feedback_handler->init(rsi.getStubs(),rsi.get_joint_names(), rsi.get_gripper_joint_names());
    rsi.add_handler(std::move(joint_feedback_handler));

    std::unique_ptr<IOStatusHandler> io_status_handler;
    io_status_handler.reset(new IOStatusHandler());
    io_status_handler->init(rsi.getStubs());
    rsi.add_handler(std::move(io_status_handler));

    std::unique_ptr<GripperStatusHandler> gripper_status_handler;
    gripper_status_handler.reset(new GripperStatusHandler());
    gripper_status_handler->init(rsi.getStubs());
    rsi.add_handler(std::move(gripper_status_handler));
    
    std::unique_ptr<RobotStateHandler> robot_state_handler;
    robot_state_handler.reset(new RobotStateHandler());
    robot_state_handler->init(rsi.getStubs());
    rsi.add_handler(std::move(robot_state_handler));


    ros::Rate loop_rate(10);

    /**
   * A count of how many messages we have sent. This is used to create
   * a unique string for each message.
   */
    int count = 0;
    while (ros::ok())
    {   
        rsi.run();
        loop_rate.sleep();
        ++count;
    }

    return 0;
}
