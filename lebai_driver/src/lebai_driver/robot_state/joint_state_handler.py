from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryFeedback
import rospy
import math



class JointStateHandler:
    def __init__(self, lebai_robot, joints_name, gripper_name):
        self.lebai_robot_ = lebai_robot
        self.joint_state_pub_ = rospy.Publisher('joint_states', JointState, queue_size=1)
        self.joint_control_state_pub_ = rospy.Publisher("feedback_states", FollowJointTrajectoryFeedback, queue_size=1)
        self.joints_name_ = joints_name
        self.gripper_name_ = gripper_name
        self.all_name_ = self.joints_name_
        if self.gripper_name_:
            self.all_name_.extend(self.gripper_name_)
        # rospy.logerr("joints_name %s"%(joints_name))
        # rospy.logerr("gripper_name %s"%(gripper_name))


    def run(self):
        joint_state = JointState()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = self.all_name_
        # rospy.logerr("joint_state.name %s"%(joint_state.name))

        positions = self.lebai_robot_.get_actual_joint_positions()
        velocities = self.lebai_robot_.get_actual_joint_speeds()
        torques = self.lebai_robot_.get_actual_joint_torques()

        joint_state.position = list(positions.pos)
        joint_state.velocity = list(velocities)
        joint_state.effort = list(torques)

        if self.gripper_name_:
            amplitude = self.lebai_robot_.get_claw_aio('amplitude')
            angle = 60.0 / 180.0 * math.pi * amplitude / 100.0
            gripper_position = [angle, -angle, -angle, angle, -angle, -angle]
            joint_state.position.extend(gripper_position)
            # rospy.logerr("joint_state.position %s"%(joint_state.position))
            joint_state.velocity.extend([0,0,0,0,0,0])
            joint_state.effort.extend([0,0,0,0,0,0])

        self.joint_state_pub_.publish(joint_state)

        control_state = FollowJointTrajectoryFeedback()
        control_state.header.stamp = rospy.Time.now()
        control_state.joint_names = self.joints_name_
        control_state.actual.positions = positions.pos
        self.joint_control_state_pub_.publish(control_state)
