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

#include "lebai_driver/motion_service/joint_trajectory_pt_full_streamer.h"
#include <industrial_utils/param_utils.h>

namespace lebai_driver
{
    JointTrajectoryPtFullStreamer::~JointTrajectoryPtFullStreamer()
    {
        if(streaming_thread_ && streaming_thread_->joinable())
        {
            streaming_thread_->join();            
        }
        delete this->streaming_thread_;
    }
    bool JointTrajectoryPtFullStreamer::init(Stubs *stubs, const std::vector<std::string> &joint_names,
                                             const std::map<std::string, double> &velocity_limits)
    {
        ROS_INFO("JointTrajectoryPtFullStreamer: init");
        stubs_ = stubs;
        all_joint_names_ = joint_names;
        joint_vel_limits_ = velocity_limits;

        sub_robot_status_ = node_.subscribe("/robot_status", 1, &JointTrajectoryPtFullStreamer::robotStatusCB, this);

        this->sub_cur_pos_ = this->node_.subscribe("/joint_states", 1, &JointTrajectoryPtFullStreamer ::jointStateCB, this);

        if (joint_vel_limits_.empty() && !industrial_utils::param::getJointVelocityLimits("robot_description", joint_vel_limits_))
            ROS_WARN("Unable to read velocity limits from 'robot_description' param.  Velocity validation disabled.");

        this->srv_stop_motion_ = this->node_.advertiseService("stop_motion", &JointTrajectoryPtFullStreamer::stopMotionCB, this);
        // this->srv_joint_trajectory_ = this->node_.advertiseService("joint_path_command", &JointTrajectoryPtFullStreamer::jointTrajectoryCB, this);
        this->sub_joint_trajectory_ = this->node_.subscribe("/joint_path_command", 0, &JointTrajectoryPtFullStreamer::jointTrajectoryCB, this);

        // rtn &= JointTrajectoryInterface::init(connection, joint_names, velocity_limits);
        //  this->srv_stop_motion_ = this->node_.advertiseService("stop_motion", &JointTrajectoryPtFullStreamer::stopMotionCB, this);
        // this->mutex_.lock();

        boost::mutex::scoped_lock lock(this->mutex_);

        this->current_point_ = 0;
        this->state_ = TransferStates::IDLE;
        this->streaming_thread_ =
            new boost::thread(boost::bind(&JointTrajectoryPtFullStreamer::streamingThread, this));
        //  ROS_INFO("Unlocking mutex");
        // this->mutex_.unlock();

        return true;
    }
    bool JointTrajectoryPtFullStreamer::select(int seq, const std::vector<std::string> &ros_joint_names, const trajectory_msgs::JointTrajectoryPoint &ros_pt,
                                               const std::vector<std::string> &rbt_joint_names, robotc::PVATRequest &grpc_pt)
    {
        ROS_ASSERT(ros_joint_names.size() == ros_pt.positions.size());

        
        for (size_t rbt_idx = 0; rbt_idx < rbt_joint_names.size(); ++rbt_idx)
        {
            bool is_empty = rbt_joint_names[rbt_idx].empty();

            // find matching ROS element
            size_t ros_idx = std::find(ros_joint_names.begin(), ros_joint_names.end(), rbt_joint_names[rbt_idx]) - ros_joint_names.begin();
            bool is_found = ros_idx < ros_joint_names.size();

            // error-chk: required robot joint not found in ROS joint-list
            if (!is_empty && !is_found)
            {
                ROS_ERROR("Expected joint (%s) not found in JointTrajectory.  Aborting command.", rbt_joint_names[rbt_idx].c_str());
                return false;
            }

            if (is_empty)
            {
                if (!ros_pt.positions.empty())
                {
                    grpc_pt.add_q(0.0);
                }
                if (!ros_pt.velocities.empty())
                {
                    grpc_pt.add_v(0.0);
                }
                if (!ros_pt.accelerations.empty())
                {
                    grpc_pt.add_acc(0.0);
                }
            }
            else
            {
                if (!ros_pt.positions.empty())
                {
                    grpc_pt.add_q(ros_pt.positions[ros_idx]);
                }
                if (!ros_pt.velocities.empty())
                {
                    grpc_pt.add_v(ros_pt.velocities[ros_idx]);
                }
                if (!ros_pt.accelerations.empty())
                {
                    grpc_pt.add_acc(ros_pt.accelerations[ros_idx]);
                }
            }

            // robot_id, sequence, fields, time, pos, vel, acc
        }
        return true;
    }

    bool JointTrajectoryPtFullStreamer::trajectory_to_reqs(const trajectory_msgs::JointTrajectoryConstPtr &traj, std::vector<robotc::PVATRequest> *reqs)
    {
        reqs->clear();

        // check for valid trajectory
        if (!is_valid(*traj))
            return false;

        for (size_t i = 0; i < traj->points.size(); ++i)
        {
            robotc::PVATRequest pvat_req;
            if (!select(i, traj->joint_names, traj->points[i], this->all_joint_names_, pvat_req))
            {
                return false;
            }
            double t0 = i != 0 ? traj->points[i - 1].time_from_start.toSec() : 0.0;
            double t1 = traj->points[i].time_from_start.toSec();
            pvat_req.set_duration(t1 - t0);
                    

            // reduce velocity to a single scalar, for robot command
            //    if (!calc_speed(xform_pt, &vel, &duration))
            //      return false;

            //    JointTrajPtFullMessage msg = create_message(i, xform_pt_full);

            // JointTrajPtFullMessage msg;
            // msg.init(xform_pt_full);
            // msgs->push_back(msg);
            reqs->push_back(pvat_req);
        }

        if (!reqs->empty() && (reqs->size() < (size_t)min_buffer_size_))
        {
            ROS_DEBUG("Padding trajectory: current(%d) => minimum(%d)", (int)reqs->size(), min_buffer_size_);
            while (reqs->size() < (size_t)min_buffer_size_)
                reqs->push_back(reqs->back());
        }

        return true;
    }

    void JointTrajectoryPtFullStreamer::jointTrajectoryCB(const trajectory_msgs::JointTrajectoryConstPtr &msg)
    {

        ROS_INFO("Receiving joint trajectory message");

        // read current state value (should be atomic)
        int state = this->state_;

        ROS_DEBUG("Current state is: %d", state);
        if (TransferStates::IDLE != state)
        {
            if (msg->points.empty())
                ROS_INFO("Empty trajectory received, canceling current trajectory");
            else
                ROS_ERROR("Trajectory splicing not yet implemented, stopping current motion.");

            //  this->mutex_.lock();
            boost::mutex::scoped_lock lock(this->mutex_);
            trajectoryStop();
            //  this->mutex_.unlock();
            return;
        }

        if (msg->points.empty())
        {
            //empty points request controller to stop.
            if (robot_status_ && robot_status_->in_motion.val == industrial_msgs::TriState::TRUE)
            {
                boost::mutex::scoped_lock lock(this->mutex_);
                ROS_INFO("Empty trajectory received, canceling current trajectory");
                trajectoryStop();
            }
            ROS_INFO("Empty trajectory received while in IDLE state, nothing is done");
            return;
        }
        //check motion possible
        if (!robot_status_)
        {
            ROS_INFO("Can't send trajectory, no robot status");
            return;
        }
        else
        {
            if (robot_status_->motion_possible.val == industrial_msgs::TriState::FALSE)
            {
                ROS_INFO("Can't send trajectory, motion not possible");
                return;
            }
        }

        // calc new trajectory
        std::vector<robotc::PVATRequest> new_traj_reqs;
        if (!trajectory_to_reqs(msg, &new_traj_reqs))
            return;
        std::cerr<<"new_traj_reqs "<<new_traj_reqs.size()<<"\n";

        // send command messages to robot
        send_to_robot(std::move(new_traj_reqs));
    }

    bool JointTrajectoryPtFullStreamer::send_to_robot(std::vector<robotc::PVATRequest> &&reqs)
    {
        ROS_INFO("Loading trajectory, setting state to streaming");

        boost::mutex::scoped_lock lock(this->mutex_);

        ROS_INFO("Executing trajectory of size: %d", (int)reqs.size());
        this->current_traj_reqs_ = std::move(reqs);
        this->current_point_ = 0;
        this->state_ = TransferStates::STREAMING;
        this->streaming_start_ = ros::Time::now();

        return true;
    }

    void JointTrajectoryPtFullStreamer::robotStatusCB(const industrial_msgs::RobotStatusConstPtr &msg)
    {
        robot_status_ = msg; //caching robot status for later use.
    }

    void JointTrajectoryPtFullStreamer::jointStateCB(const sensor_msgs::JointStateConstPtr &msg)
    {
        this->cur_joint_pos_ = *msg;
    }

    bool JointTrajectoryPtFullStreamer::stopMotionCB(industrial_msgs::StopMotion::Request &req,
                                                     industrial_msgs::StopMotion::Response &res)
    {
        ROS_INFO("Send message to robot controller for stopping trajectory!");
        trajectoryStop();
        // no success/fail result from trajectoryStodp.  Assume success.
        res.code.val = industrial_msgs::ServiceReturnCode::SUCCESS;

        return true; // always return true.  To distinguish between call-failed and service-unavailable.
    }

    void JointTrajectoryPtFullStreamer::streamingThread()
    {
        // JointTrajPtFullMessage jtpMsg;
        // jtpMsg.setSequence(SpecialSeqValues::START_TRAJECTORY_STREAMING);
        int connectRetryCount = 1;

        ROS_INFO("Starting joint trajectory streamer thread");
        while (ros::ok())
        {
            ros::Duration(0.005).sleep();
            boost::mutex::scoped_lock lock(this->mutex_);

            switch (this->state_)
            {
            case TransferStates::IDLE:
                ros::Duration(0.250).sleep(); //  slower loop while waiting for new trajectory
                break;

            case TransferStates::STREAMING:
            {
                grpc::ClientContext context;
                robotc::CmdId res;
                std::unique_ptr<::grpc::ClientWriter<robotc::PVATRequest>> pvat_stream = stubs_->robot_controller_stub_->MovePVATStream(&context, &res);
                // std::unique_ptr<::grpc::ClientReaderWriter<::robotc::RobotDataCmd, ::robotc::IO>> stream = stubs_->robot_controller_stub_->GetRobotIOData(&context);
                for (auto &&req : this->current_traj_reqs_)
                {
                    pvat_stream->Write(req);
                }
                pvat_stream->WritesDone();
                pvat_stream->Finish();

                this->state_ = TransferStates::IDLE;
                break;
            }
            default:
                ROS_ERROR("Joint trajectory streamer: unknown state");
                this->state_ = TransferStates::IDLE;
                break;
            }
        }

        ROS_WARN("Exiting trajectory streamer thread");
    }

    void JointTrajectoryPtFullStreamer::trajectoryStop()
    {
        grpc::ClientContext context;
        google::protobuf::Empty grpc_req;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_->robot_controller_stub_->StopMove(&context, grpc_req, &grpc_res);
        if (status.ok())
        {
        }
        else
        {
            ROS_ERROR("Failed to call `Stop`.");
            return;
        }
        this->state_ = TransferStates::IDLE;
    }

    bool JointTrajectoryPtFullStreamer::is_valid(const trajectory_msgs::JointTrajectory &traj)
    {
        for (int i = 0; i < traj.points.size(); ++i)
        {
            const trajectory_msgs::JointTrajectoryPoint &pt = traj.points[i];

            // check for non-empty positions
            if (pt.positions.empty())
            {
                ROS_ERROR("Validation failed: Missing position data for trajectory pt %d", i);
                return false;
            }

            // check for joint velocity limits
            for (int j = 0; j < pt.velocities.size(); ++j)
            {
                std::map<std::string, double>::iterator max_vel = joint_vel_limits_.find(traj.joint_names[j]);
                if (max_vel == joint_vel_limits_.end())
                    continue; // no velocity-checking if limit not defined

                if (std::abs(pt.velocities[j]) > max_vel->second)
                {
                    ROS_ERROR("Validation failed: Max velocity exceeded for trajectory pt %d, joint '%s'", i, traj.joint_names[j].c_str());
                    return false;
                }
            }

            // check for valid timestamp
            if ((i > 0) && (pt.time_from_start.toSec() == 0))
            {
                ROS_ERROR("Validation failed: Missing valid timestamp data for trajectory pt %d", i);
                return false;
            }
        }

        return true;
    }

} // namespace lebai_driver