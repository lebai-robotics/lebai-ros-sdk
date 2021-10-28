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
#include <vector>

#include <ros/ros.h>

#include "lebai_driver/robot_state/handle.h"
#include "lebai_driver/stubs.h"

namespace lebai_driver
{
    class RobotStateInterface
    {

    public:
        RobotStateInterface();
        // Channels & getChannels();
        Stubs * getStubs();
        bool init();
        


        /**
   * \brief Begin processing messages and publishing topics.
   */
        void run();

        //   /**
        //    * \brief get current robot-connection instance.
        //    *
        //    * \return current robot connection object
        //    */
        //   SmplMsgConnection* get_connection()
        //   {
        //     return this->connection_;
        //   }

        //   /**
        //    * \brief get active message-manager object
        //    *
        //    * \return current message-manager object
        //    */
        //   MessageManager* get_manager()
        //   {
        //     return &this->manager_;
        //   }

          std::vector<std::string> get_joint_names()
          {
            return this->joint_names_;
          }


          std::vector<std::string> get_gripper_joint_names()
          {
            return this->gripper_joint_names_;
          }

          void add_handler(std::unique_ptr<Handler> && handler)
          {
            handlers_.push_back(std::move(handler));
          }

        protected:
            Stubs stubs_;
            ros::NodeHandle node_;
            std::vector<std::unique_ptr<Handler>> handlers_;
            std::vector<std::string> joint_names_ = {"joint_1","joint_2","joint_3","joint_4","joint_5","joint_6"};
            std::vector<std::string> gripper_joint_names_;
        //   TcpClient default_tcp_connection_;
        //   JointRelayHandler default_joint_handler_;
        //   RobotStatusRelayHandler default_robot_status_handler_;

        //   SmplMsgConnection* connection_;
        //   MessageManager manager_;
          

    }; //class RobotStateInterface

} //lebai
