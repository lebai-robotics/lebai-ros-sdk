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
#include <ros/ros.h>
#include <boost/thread/thread.hpp>

// #include <industrial_robot_client/joint_trajectory_interface.h>
#include <industrial_msgs/RobotStatus.h>
#include <industrial_msgs/StopMotion.h>
#include <trajectory_msgs/JointTrajectory.h>
#include <sensor_msgs/JointState.h>

#include "lebai_driver/stubs.h"

// typedef trajectory_msgs::JointTrajectoryPoint Industrial_JointTrajPoint;

namespace lebai_driver
{

  // using namespace industrial::joint_traj_pt_full;
  // using industrial::joint_traj_pt_full_message::JointTrajPtFullMessage;
  // using industrial::joint_traj_pt_message::JointTrajPtMessage;
  // using industrial::simple_message::SimpleMessage;
  // using industrial::smpl_msg_connection::SmplMsgConnection;
  // using industrial_robot_client::joint_trajectory_interface::JointTrajectoryInterface;

  namespace TransferStates
  {
    enum TransferState
    {
      IDLE = 0,
      STREAMING = 1 //,STARTING, //, STOPPING
    };
  }
  typedef TransferStates::TransferState TransferState;

  class JointTrajectoryPtFullStreamer
  {

  public:
    // using JointTrajectoryInterface::init;
    JointTrajectoryPtFullStreamer(int min_buffer_size = 1) : min_buffer_size_(min_buffer_size){};
    ~JointTrajectoryPtFullStreamer();
    bool init(Stubs *stubs, const std::vector<std::string> &joint_names,
              const std::map<std::string, double> &velocity_limits = std::map<std::string, double>());

    void jointTrajectoryCB(const trajectory_msgs::JointTrajectoryConstPtr &msg);

    // JointTrajPtFullMessage create_message(int seq, Industrial_JointTrajPtPull &pt_full);

    bool select(int seq, const std::vector<std::string> &ros_joint_names, const trajectory_msgs::JointTrajectoryPoint &ros_pt,
                                               const std::vector<std::string> &rbt_joint_names, robotc::PVATRequest &grpc_pt);

    // //  virtual bool trajectory_to_msgs(const trajectory_msgs::JointTrajectoryConstPtr &traj, std::vector<JointTrajPtMessage>* msgs);
    bool trajectory_to_reqs(const trajectory_msgs::JointTrajectoryConstPtr &traj,
                            std::vector<robotc::PVATRequest> * reqs);

    void streamingThread();

    bool send_to_robot(std::vector<robotc::PVATRequest> && reqs);


    void robotStatusCB(const industrial_msgs::RobotStatusConstPtr &msg);
    
    void jointStateCB(const sensor_msgs::JointStateConstPtr &msg);

    bool stopMotionCB(industrial_msgs::StopMotion::Request &req,
                      industrial_msgs::StopMotion::Response &res);
    


  protected:
    void trajectoryStop();
    bool is_valid(const trajectory_msgs::JointTrajectory &traj);

    // Stubs * stubs_;

    boost::thread *streaming_thread_;
    boost::mutex mutex_;

    TransferState state_;
    int current_point_;
    std::vector<robotc::PVATRequest> current_traj_reqs_;
    ros::Time streaming_start_;
    // std::unique_ptr<::grpc::ClientReaderWriter<::robotc::RobotDataCmd, ::robotc::IO>> stream = stubs_->robot_controller_stub_->GetRobotIOData(&context);

    
    int min_buffer_size_;

    ros::Subscriber sub_robot_status_;
    industrial_msgs::RobotStatusConstPtr robot_status_;

    ros::NodeHandle node_;
    Stubs *stubs_;

    std::vector<std::string> all_joint_names_;
    std::map<std::string, double> joint_vel_limits_;

    ros::Subscriber sub_cur_pos_;             // handle for joint-state topic subscription
     sensor_msgs::JointState cur_joint_pos_;

    ros::Subscriber sub_joint_trajectory_;    // handle for joint-trajectory topic subscription
    // ros::ServiceServer srv_joint_trajectory_; // handle for joint-trajectory service
    ros::ServiceServer srv_stop_motion_;      // handle for stop_motion service
  };

} // namespace lebai_driver
