#!/usr/bin/env python3
import time
import unittest

import rospy
import rostest


SERVICES = {
    'start_stop': 'start_sys stop_sys powerdown stop estop start_teach_mode end_teach_mode pause_move resume_move reboot',
    'motion': 'movej movel movec speedj speedl move_pvat wait_move stop_move skip_move get_running_motion get_motion_state',
    'io': 'set_do get_di get_do set_dos get_dis get_dos set_ao get_ai get_ao set_aos get_ais get_aos set_dio_mode get_dio_mode',
    'led': 'set_led',
    'signal': 'get_signals set_signals',
    'resource': 'load_tcp_list load_pose_list load_frame_list load_trajectory_list',
    'claw': 'init_claw set_claw get_claw',
}
STATUS = ('status/joint_states', 'claw/joint_states', 'model/joint_states',
          'status/robot', 'status/joint_motion', 'io/state', 'claw/state')
ACTIONS = ('/lebai_trajectory_controller', '/lebai_gripper_controller/gripper_cmd')


class DriverInterfaces(unittest.TestCase):
    __test__ = False  # rostest starts the ROS master and the node under test.

    def test_driver_owns_expected_graph(self):
        driver = '/lebai/lebai_driver'
        publishers = {'/lebai/' + topic for topic in STATUS}
        publishers.update(base + '/' + suffix for base in ACTIONS for suffix in ('status', 'feedback', 'result'))
        subscribers = {base + '/' + suffix for base in ACTIONS for suffix in ('goal', 'cancel')}
        services = {'/lebai/' + group + '/' + name for group, names in SERVICES.items() for name in names.split()}

        deadline = time.monotonic() + 20
        while not rospy.is_shutdown():
            code, message, state = rospy.get_master().getSystemState()
            self.assertEqual(code, 1, message)
            missing = {}
            for kind, expected, entries in zip(('publishers', 'subscribers', 'services'),
                                               (publishers, subscribers, services), state):
                absent = expected - {name for name, owners in entries if driver in owners}
                if absent:
                    missing[kind] = sorted(absent)
            if not missing:
                return
            if time.monotonic() >= deadline:
                self.fail('Missing driver registrations: %s' % missing)
            time.sleep(0.1)
        self.fail('ROS shut down before driver registration')


if __name__ == '__main__':
    rospy.init_node('driver_interfaces_test')
    rostest.rosrun('lebai_driver', 'driver_interfaces', DriverInterfaces)
