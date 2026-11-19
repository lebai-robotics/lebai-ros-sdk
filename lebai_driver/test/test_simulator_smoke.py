import os
from pathlib import Path
import socket
import subprocess

import pytest
import yaml


@pytest.mark.integration
def test_driver_reads_simulator_state_and_runs_current_position_move(monkeypatch):
    robot_ip = os.environ.get('LEBAI_TEST_ROBOT_IP')
    if not robot_ip:
        pytest.skip('LEBAI_TEST_ROBOT_IP is not set')

    import roslaunch

    # Give this run its own ROS master and child nodes.
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    monkeypatch.setenv('ROS_MASTER_URI', 'http://127.0.0.1:%d' % port)
    monkeypatch.setenv('ROS_HOSTNAME', '127.0.0.1')
    launch_file = Path(__file__).resolve().parents[1] / 'launch/driver.launch'
    args = ['robot_ip:=' + robot_ip, 'simulator:=true', 'publish_robot_description:=false']
    launch = roslaunch.parent.ROSLaunchParent(
        roslaunch.core.generate_run_id(), [(str(launch_file), args)], port=port)

    def read(*command):
        output = subprocess.check_output(command, text=True, timeout=20)
        return next(yaml.safe_load_all(output))

    def service(name, **fields):
        request = yaml.safe_dump(fields, default_flow_style=True)
        response = read('rosservice', 'call', '/lebai/' + name, request)
        assert response['result']['success'], response['result']['message']
        return response

    try:
        launch.start()
        state = read('rostopic', 'echo', '-n', '1', '/lebai/status/robot')
        assert state['connected'], state['message']
        joints = read('rostopic', 'echo', '-n', '1', '/lebai/status/joint_states')
        assert len(joints['position']) == 6
        for topic in ('status/joint_motion', 'io/state'):
            state = read('rostopic', 'echo', '-n', '1', '/lebai/' + topic)
            assert state['connected'], state['message']
        service('motion/get_running_motion')
        for method in ('get_di', 'get_do', 'get_ai', 'get_ao', 'get_dio_mode'):
            service('io/' + method, device='robot', pin=0)
        service('start_stop/start_sys')
        try:
            move = service('motion/movej', target={'is_joint_pose': True, 'joint_positions': joints['position']},
                           params={'acceleration': 0.2, 'velocity': 0.2})
            service('motion/get_motion_state', motion_id=move['motion_id'])
            service('motion/wait_move', motion_id=move['motion_id'])
        finally:
            service('start_stop/stop_sys')
    finally:
        launch.shutdown()
