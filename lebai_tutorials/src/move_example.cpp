#include <ros/ros.h>
#include <lebai_msgs/MoveJoint.h>
#include <lebai_msgs/MoveLine.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "lebai_lm3_move_example");
    ros::NodeHandle n;

    ros::ServiceClient move_joint_client = n.serviceClient<lebai_msgs::MoveJoint>("/motion_service/move_joint");
    ros::ServiceClient move_line_client = n.serviceClient<lebai_msgs::MoveJoint>("/motion_service/move_line");
    move_joint_client.waitForExistence();
    ROS_INFO("Move joint service exist.\n");
    move_line_client.waitForExistence();
    ROS_INFO("Move line service exist.\n");

    //generate a move joint srv data.
    lebai_msgs::MoveJoint move_joint_srv;
    move_joint_srv.request.joint_pose = {-0.515705166127304, -1.383938292070577, 0.9317015810420413, -1.0843326694366626, -0.8334309368181174, -0.7919175817459623};
    move_joint_srv.request.is_joint_pose = 1;
    move_joint_srv.request.common.vel = 0.2;
    move_joint_srv.request.common.acc = 1.0;

    // call move joint service
    if (move_joint_client.call(move_joint_srv))
    {
        ROS_INFO("Successed to run move joint\n");
    }
    else
    {
        ROS_ERROR("Failed to run move joint");
    }


    //generate a move line srv data.
    lebai_msgs::MoveLine move_line_srv;
    move_line_srv.request.joint_pose = {-1.9979141024218048, -1.1726324385393299, 0.9936360553529241, -1.0942076707586763, -0.849345987492431, -0.8172282647460754};
    move_line_srv.request.is_joint_pose = 1;
    move_line_srv.request.common.vel = 0.2;
    move_line_srv.request.common.acc = 1.0;

    // call move joint service
    if (move_line_client.call(move_line_srv))
    {
        ROS_INFO("Successed to run move line\n");
    }
    else
    {
        ROS_ERROR("Failed to run move line");
    }
    return 0;
}