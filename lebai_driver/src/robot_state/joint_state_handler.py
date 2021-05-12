from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryFeedback
import rospy



class JointStateHandler:
    def __init__(self, lebai_robot, joints_name):
        self.lebai_robot_ = lebai_robot
        self.joint_state_pub_ = rospy.Publisher('joint_states', JointState, queue_size=1)
        self.joint_control_state_pub_ = rospy.Publisher("feedback_states", FollowJointTrajectoryFeedback, queue_size=1)
        self.joints_name_ = joints_name

    def run(self):
        positions = self.lebai_robot_.get_actual_joint_positions()
        velocities = self.lebai_robot_.get_actual_joint_speeds()
        torques = self.lebai_robot_.get_actual_joint_torques()
        joint_state = JointState()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = self.joints_name_
        joint_state.position = list(positions.pos)
        joint_state.velocity = list(velocities)
        joint_state.effort = list(torques)
        self.joint_state_pub_.publish(joint_state)

        control_state = FollowJointTrajectoryFeedback()
        control_state.header.stamp = rospy.Time.now()
        control_state.joint_names = self.joints_name_
        control_state.actual.positions = positions.pos
        self.joint_control_state_pub_.publish(control_state)
