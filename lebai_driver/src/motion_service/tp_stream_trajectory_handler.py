from lebai.type import JointPose, JointPose, CartesianPose, PVAT
from genpy.rostime import Duration
import rospy
from industrial_msgs.msg import RobotStatus, ServiceReturnCode
from industrial_msgs.srv import StopMotion, StopMotionResponse
from industrial_msgs.srv import CmdJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState


# class TransferState(Enum):
#     IDLE = 0
#     STREAMING = 1

class TPStreamTrajectoryHandler:
    def __init__(self, lebai_robot, joints_name):
        self.lebai_robot_ = lebai_robot
        self.sub_robot_status_ = rospy.Subscriber("robot_status", RobotStatus, self.robot_status_callback)
        self.robot_status_ = None
        self.joints_name_ = joints_name
        rospy.logwarn("No velocity limits set, velocity validation disabled")
        self.srv_stop_motion_ = rospy.Service("stop_motion", StopMotion, self.service_stop_motion)
        self.srv_joint_trajectory_ = rospy.Service("joint_path_command", CmdJointTrajectory, self.service_joint_trajectory)
        self.sub_joint_trajectory_ = rospy.Subscriber("joint_path_command", JointTrajectory, self. joint_trajectory_cb)
        self.sub_cur_pos_ = rospy.Subscriber("joint_states", JointState, self.joint_state_cb)
        # self.state_ = TransferState.IDLE

    def __del__(self):
        # self.lebai_robot_.stop()
        pass
    
    def robot_status_callback(self, data):        
        self.robot_status_ = data
        # print("xxx %s"%(self.robot_status_.motion_possible.val))
        pass
    
    def service_stop_motion(self, req):
        self.stop_motion()
        res = StopMotionResponse()
        res.code.val = ServiceReturnCode.SUCCESS
        return res

    def stop_motion(self):
        self.lebai_robot_.stop()
        # self.state_ = TransferState.IDLE
        return

    def service_joint_trajectory(self, req):
            #         ROS_INFO("Stop motion callbacks");
            # trajectoryStop();
            # // no success/fail result from trajectoryStodp.  Assume success.
            # res.code.val = industrial_msgs::ServiceReturnCode::SUCCESS;

            # return true; // always return true.  To distinguish between call-failed and service-unavailable.
        pass

    def joint_trajectory_cb(self, traj_msg):
        # state = self.state_
        # if state != TransferState.IDLE:
        #     if not traj_msg.points:
        #         rospy.loginfo("Empty trajectory received, canceling current trajectory")
        #     else:
        #         rospy.logerr("Trajectory splicing not yet implemented, stopping current motion.");
        #     self.stop_motion()
        #     return
        if self.robot_status_ == None:
            return
        if self.robot_status_.in_motion.val == True:
            self.stop_motion()
            return
        if not traj_msg.points:
            return            

        if self.robot_status_.motion_possible.val == False:
            rospy.loginfo("Can't send trajectory, motion not possible")
            return
        if self.is_valid_traj(traj_msg) == False:
            rospy.loginfo("Can't send trajectory, traj is not valid")
            return
        self.send_to_robot(traj_msg)
    
    def generate_data_list(self, traj_msg):        
        for i in range(len(traj_msg.points)-1):
            data = PVAT(traj_msg.points[i+1].time_from_start.to_sec() - traj_msg.points[i].time_from_start.to_sec(), traj_msg.points[i+1].positions,
            traj_msg.points[i+1].velocities, traj_msg.points[i+1].accelerations)
            yield data


    def send_to_robot(self, traj_msg):
        data_gen = self.generate_data_list(traj_msg)
        self.lebai_robot_.move_pvats(data_gen)


    def traj_msgs_to_sdk_params(self, traj):
        if self.is_valid_traj(traj) == None:
            return None
        # traj = JointTrajectory()
        data_to_robot = list()
        for i in range(len(traj.points)):
            data_to_robot.append(self.select(i, traj.joint_names, traj.points[i], self.joints_name_))

        
    # def select(i, traj_joint_names, point, robot_joint_names):
    #     if len(traj_joint_names) != len(robot_joint_names):
    #         return None
    #     data_to_robot = list()
    #     positions = list()
    #     velocities = list()
    #     accelerations = list()
    #     for i in range(len(traj_joint_names)):
    #         is_found = False
    #         robot_joint_idx = 0
    #         for j in range(len(robot_joint_names)):
    #             if traj_joint_names[i] == robot_joint_names[j]:
    #                 is_found = True
    #                 robot_joint_idx = j
    #         if not is_found:
    #             rospy.logerr("Expected joint (%s) not found in JointTrajectory.  Aborting command.", robot_joint_names[i])
    #             return None

    #         point = JointTrajectoryPoint()
    #         positions.append(point.positions[robot_joint_idx])
    #         velocities.append(point.velocities[robot_joint_idx])
    #         accelerations.append(point.accelerations[robot_joint_idx])
    #         duration_time =  point.time_from_start.to_sec()
    #         data = (positions, velocities, accelerations, duration_time)
    #         return data
        



        

    def is_valid_traj(self, traj):
        for i in range(len(traj.points)):
            point = traj.points[i]
            if not point.positions:
                rospy.logerr( "Validation failed: Missing position data for trajectory pt %d", i)
                return False
            #TODO vel limitation
            point = JointTrajectoryPoint()
            if i > 0 and point.time_from_start.to_sec() < 1e-6:
                rospy.logerr( "Validation failed: Missing valid timestamp data for trajectory pt %d", i)
                return False
            return True
         
    def joint_state_cb(self, data):
        self.joint_state = data
        pass

        

