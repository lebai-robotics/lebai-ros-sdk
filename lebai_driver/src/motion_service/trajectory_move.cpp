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

// #include <tf2/convert.h>
#include "lebai_driver/motion_service/trajectory_move.h"
#include "lebai_driver/motion_service/trajectory_move_utils.h"

namespace lebai_driver
{

    TrajectoryMove::TrajectoryMove()
    :node_("~")
    {
    }

    TrajectoryMove::~TrajectoryMove()
    {
    }

    bool TrajectoryMove::init(Stubs * stubs)
    {
        stubs_ = stubs;
        ROS_DEBUG("TrajectoryMove: init");
        move_joint_service_ = node_.advertiseService("move_joint", &TrajectoryMove::moveJoint, this);
        move_line_service_ = node_.advertiseService("move_line", &TrajectoryMove::moveLine, this);
        move_circle_service_ = node_.advertiseService("move_circle", &TrajectoryMove::moveCircle, this);
        return true;
    }
    bool TrajectoryMove::sendMoveJointToRobot(robotc::MoveJRequest & grpc_req)
    {
        grpc::ClientContext context;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_->robot_controller_stub_->MoveJ(&context, grpc_req, &grpc_res);
        if (status.ok())
        {

        }
        else
        {
            ROS_ERROR("Failed to call `MoveJ`.");
            return false;
        }
        return true;
    }

    bool TrajectoryMove::sendMoveLineToRobot(robotc::MoveLRequest & grpc_req)
    {
        grpc::ClientContext context;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_->robot_controller_stub_->MoveL(&context, grpc_req, &grpc_res);
        if (status.ok())
        {

        }
        else
        {
            ROS_ERROR("Failed to call `MoveL`.");
            return false;
        }
        return true;
    }

    bool TrajectoryMove::sendMoveCircleToRobot(robotc::MoveCRequest & grpc_req)
    {
        grpc::ClientContext context;
        robotc::CmdId grpc_res;
        grpc::Status status;
        status = stubs_->robot_controller_stub_->MoveC(&context, grpc_req, &grpc_res);
        if (status.ok())
        {

        }
        else
        {
            ROS_ERROR("Failed to call `MoveC`.");
            return false;
        }
        return true;
    }

    bool TrajectoryMove::moveJoint(lebai_msgs::MoveJoint::Request &req, lebai_msgs::MoveJoint::Response &res)
    {
        // req.cartesian_pose.orientation;
        robotc::MoveJRequest grpc_req;
        grpc_req.set_pose_is_joint_angle(req.is_joint_pose);
        if (grpc_req.pose_is_joint_angle())
        {
            for (size_t i = 0; i < req.joint_pose.size(); ++i)
            {
                grpc_req.add_joint_pose_to(req.joint_pose[i]);
            }
        }
        else
        {
            geometryPoseToRepeatedDouble(req.cartesian_pose, grpc_req.mutable_joint_pose_to());
        }
        grpc_req.set_velocity(req.common.vel);
        grpc_req.set_acceleration(req.common.acc);
        grpc_req.set_time(req.common.time);
        grpc_req.set_blend_radius(req.common.radius);

        if (sendMoveJointToRobot(grpc_req))
        {
            res.ret = true;
        }
        else
        {
            res.ret = false;
        }
        return true;
    }
    bool TrajectoryMove::moveLine(lebai_msgs::MoveLine::Request &req, lebai_msgs::MoveLine::Response &res)
    {
        robotc::MoveLRequest grpc_req;
        grpc_req.set_pose_is_joint_angle(req.is_joint_pose);
        if (grpc_req.pose_is_joint_angle())
        {
            for (size_t i = 0; i < req.joint_pose.size(); ++i)
            {
                grpc_req.add_pose_to(req.joint_pose[i]);
            }
        }
        else
        {
            geometryPoseToRepeatedDouble(req.cartesian_pose, grpc_req.mutable_pose_to());
        }
        grpc_req.set_velocity(req.common.vel);
        grpc_req.set_acceleration(req.common.acc);
        grpc_req.set_time(req.common.time);
        grpc_req.set_blend_radius(req.common.radius);

        if (sendMoveLineToRobot(grpc_req))
        {
            res.ret = true;
        }
        else
        {
            res.ret = false;
        }
        return true;
    }

    bool TrajectoryMove::moveCircle(lebai_msgs::MoveCircle::Request &req, lebai_msgs::MoveCircle::Response &res)
    {
        robotc::MoveCRequest grpc_req;
        grpc_req.set_pose_via_is_joint(req.way_point_is_joint_pose);
        if (grpc_req.pose_via_is_joint())
        {
            for (size_t i = 0; i < req.way_point_joint_pose.size(); ++i)
            {
                grpc_req.add_pose_via(req.way_point_joint_pose[i]);
            }
        }
        else
        {
            geometryPoseToRepeatedDouble(req.way_point_cartesian_pose, grpc_req.mutable_pose_via());
        }

        grpc_req.set_pose_to_is_joint(req.end_point_is_joint_pose);
        if (grpc_req.pose_to_is_joint())
        {
            for (size_t i = 0; i < req.end_point_joint_pose.size(); ++i)
            {
                grpc_req.add_pose_to(req.end_point_joint_pose[i]);
            }
        }
        else
        {
            geometryPoseToRepeatedDouble(req.end_point_cartesian_pose, grpc_req.mutable_pose_to());
        }

        grpc_req.set_rad(req.circle_angle);
        grpc_req.set_velocity(req.common.vel);
        grpc_req.set_acceleration(req.common.acc);
        grpc_req.set_time(req.common.time);
        grpc_req.set_blend_radius(req.common.radius);

        if (sendMoveCircleToRobot(grpc_req))
        {
            res.ret = true;
        }
        else
        {
            res.ret = false;
        }
        return true;
    }

    // bool TrajectoryMove::untilInfoToSimpleMsg(const lebai_msgs::UntilInfo &in, UntilInfo &out)
    // {
    //     out.io_size_ = in.io_express.size();
    //     out.io_express_logic_ = in.io_express_logic;
    //     for (size_t i = 0; i < in.io_express.size(); ++i)
    //     {
    //         out.io_express_[i].setGroup(in.io_express[i].group);
    //         out.io_express_[i].setIndex(in.io_express[i].pin);
    //         out.io_express_[i].setMode(in.io_express[i].type);
    //         if (in.io_express[i].type == lebai_msgs::IOConditionalExpress::TYPE_DIGITAL)
    //         {
    //             out.io_express_[i].setIntVal(in.io_express[i].uint_value);
    //         }
    //         else if (in.io_express[i].type == lebai_msgs::IOConditionalExpress::TYPE_ANALOG)
    //         {
    //             out.io_express_[i].setRealVal(in.io_express[i].float_value);
    //         }
    //         out.io_express_[i].setLogicOperation(in.io_express[i].logic_operation);
    //     }
    // }

    // void trajectoryMoveJoint::trajectoryMoveJointCB(const trajectory_msgs::JointTrajectoryConstPtr &msg)
    // {
    //     ROS_INFO("Receiving joint trajectory message");

    //     // read current state value (should be atomic)
    //     int state = this->state_;

    //     ROS_DEBUG("Current state is: %d", state);
    //     if (TransferStates::IDLE != state)
    //     {
    //         if (msg->points.empty())
    //             ROS_INFO("Empty trajectory received, canceling current trajectory");
    //         else
    //             ROS_ERROR("Trajectory splicing not yet implemented, stopping current motion.");

    //         //  this->mutex_.lock();
    //         boost::mutex::scoped_lock lock(this->mutex_);
    //         trajectoryStop();
    //         //  this->mutex_.unlock();
    //         return;
    //     }

    //     //  // check for STOP command
    //     //  if (msg->points.empty())
    //     //  {
    //     //    ROS_INFO("Empty trajectory received, canceling current trajectory");
    //     //    trajectoryStop();
    //     //    return;
    //     //  }

    //     if (msg->points.empty())
    //     {
    //         //empty points request controller to stop.
    //         if (robot_status_ && robot_status_->in_motion.val == industrial_msgs::TriState::TRUE)
    //         {
    //             boost::mutex::scoped_lock lock(this->mutex_);
    //             trajectoryStop();
    //         }
    //         ROS_INFO("Empty trajectory received while in IDLE state, nothing is done");
    //         return;
    //     }
    //     //check motion possible
    //     if (!robot_status_)
    //     {
    //         ROS_INFO("Can't send trajectory, no robot status");
    //         return;
    //     }
    //     else
    //     {
    //         if (robot_status_->motion_possible.val == industrial_msgs::TriState::FALSE)
    //         {
    //             ROS_INFO("Can't send trajectory, motion not possible");
    //             return;
    //         }
    //     }

    //     // calc new trajectory
    //     std::vector<JointTrajPtFullMessage> new_traj_msgs;
    //     if (!trajectory_to_msgs(msg, &new_traj_msgs))
    //         return;

    //     // send command messages to robot
    //     send_to_robot(new_traj_msgs);
    // }

    // bool JointTrajectoryPtFullStreamer::send_to_robot(const std::vector<JointTrajPtFullMessage> &messages)
    // {
    //     ROS_INFO("Loading trajectory, setting state to streaming");
    //     //  this->mutex_.lock();

    //     boost::mutex::scoped_lock lock(this->mutex_);
    //     {
    //         ROS_INFO("Executing trajectory of size: %d", (int)messages.size());
    //         this->current_traj_ = messages;
    //         this->current_point_ = 0;
    //         this->state_ = TransferStates::STREAMING;
    //         this->streaming_start_ = ros::Time::now();
    //     }
    //     //  this->mutex_.unlock();

    //     return true;
    // }

    // void JointTrajectoryPtFullStreamer::robotStatusCB(const industrial_msgs::RobotStatusConstPtr &msg)
    // {
    //     robot_status_ = msg; //caching robot status for later use.
    // }

    // bool JointTrajectoryPtFullStreamer::stopMotionCB(industrial_msgs::StopMotion::Request &req,
    //                                                  industrial_msgs::StopMotion::Response &res)
    // {
    //     ROS_INFO("Stop motion callbacks");
    //     trajectoryStop();
    //     // no success/fail result from trajectoryStodp.  Assume success.
    //     res.code.val = industrial_msgs::ServiceReturnCode::SUCCESS;

    //     return true; // always return true.  To distinguish between call-failed and service-unavailable.
    // }

    // void JointTrajectoryPtFullStreamer::streamingThread()
    // {
    //     JointTrajPtFullMessage jtpMsg;
    //     jtpMsg.setSequence(SpecialSeqValues::START_TRAJECTORY_STREAMING);
    //     int connectRetryCount = 1;

    //     ROS_INFO("Starting joint trajectory streamer thread");
    //     while (ros::ok())
    //     {
    //         ros::Duration(0.005).sleep();

    //         // automatically re-establish connection, if required
    //         if (connectRetryCount-- > 0)
    //         {
    //             ROS_INFO("Connecting to robot motion server");
    //             this->connection_->makeConnect();
    //             ros::Duration(0.250).sleep(); // wait for connection

    //             if (this->connection_->isConnected())
    //                 connectRetryCount = 0;
    //             else if (connectRetryCount <= 0)
    //             {
    //                 ROS_ERROR("Timeout connecting to robot controller.  Send new motion command to retry.");
    //                 this->state_ = TransferStates::IDLE;
    //             }
    //             continue;
    //         }

    //         //    this->mutex_.lock();
    //         boost::mutex::scoped_lock lock(this->mutex_);

    //         SimpleMessage msg, reply;

    //         switch (this->state_)
    //         {
    //         case TransferStates::IDLE:
    //             ros::Duration(0.250).sleep(); //  slower loop while waiting for new trajectory
    //             break;

    //         case TransferStates::STREAMING:
    //             if (this->current_point_ >= (int)this->current_traj_.size())
    //             {
    //                 ROS_INFO("Trajectory streaming complete, setting state to IDLE");
    //                 this->state_ = TransferStates::IDLE;
    //                 break;
    //             }

    //             if (!this->connection_->isConnected())
    //             {
    //                 ROS_DEBUG("Robot disconnected.  Attempting reconnect...");
    //                 connectRetryCount = 5;
    //                 break;
    //             }

    //             jtpMsg = this->current_traj_[this->current_point_];
    //             jtpMsg.toRequest(msg);

    //             ROS_DEBUG("Sending joint trajectory point");
    //             if (this->connection_->sendAndReceiveMsg(msg, reply, false))
    //             {
    //                 ROS_INFO("Point[%d of %d] sent to controller",
    //                          this->current_point_, (int)this->current_traj_.size());
    //                 this->current_point_++;
    //             }
    //             else
    //                 ROS_WARN("Failed sent joint point, will try again");

    //             break;
    //         default:
    //             ROS_ERROR("Joint trajectory streamer: unknown state");
    //             this->state_ = TransferStates::IDLE;
    //             break;
    //         }

    //         //    this->mutex_.unlock();
    //     }

    //     ROS_WARN("Exiting trajectory streamer thread");
    // }

    // void JointTrajectoryPtFullStreamer::trajectoryStop()
    // {
    //     JointTrajPtFullMessage jMsg;
    //     SimpleMessage msg, reply;

    //     ROS_INFO("Joint trajectory handler: entering stopping state");
    //     jMsg.setSequence(SpecialSeqValues::STOP_TRAJECTORY);
    //     jMsg.toRequest(msg);
    //     ROS_DEBUG("Sending stop command");
    //     this->connection_->sendAndReceiveMsg(msg, reply);

    //     ROS_DEBUG("Stop command sent, entering idle mode");
    //     this->state_ = TransferStates::IDLE;
    // }

} // namespace lebai_driver
