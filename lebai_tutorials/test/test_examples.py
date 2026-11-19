import ast
import runpy
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import actionlib
import pytest
import rospy
from control_msgs.msg import GripperCommandResult
from lebai_interfaces.msg import Result
from lebai_interfaces.srv import MoveJointResponse


PACKAGE = Path(__file__).resolve().parents[1]
SCRIPTS = PACKAGE / 'scripts'
EXAMPLES = {
    'io_example': ('ServiceProxy', '/lebai/io/set_do', '/lebai/io/set_ao'),
    'move_example': ('ServiceProxy', '/lebai/motion/movej', '/lebai/motion/movel'),
    'joint_state_subscriber': ('Subscriber', '/lebai/status/joint_states'),
    'moveit_manipulator_example': ('moveit_commander', 'MoveGroupCommander', 'manipulator'),
    'moveit_gripper_amplitude_example': ('SimpleActionClient',
                                       '/lebai_gripper_controller/gripper_cmd',
                                       'has_gripper:=true'),
}


@pytest.mark.parametrize('name', EXAMPLES)
def test_example_imports_with_no_ros_master(name, monkeypatch):
    path = SCRIPTS / (name + '.py')
    assert path.is_file()
    monkeypatch.syspath_prepend(str(SCRIPTS))
    # Leave generated ROS message and service classes real. The empty rospy
    # stub also catches examples that initialize a node or call ROS at import.
    __import__('actionlib')
    __import__('moveit_commander')
    monkeypatch.setitem(sys.modules, 'rospy', ModuleType('rospy'))
    module = runpy.run_path(str(path))
    assert callable(module['main'])


@pytest.mark.parametrize('name, references', EXAMPLES.items())
def test_example_uses_noetic_interfaces(name, references):
    path = SCRIPTS / (name + '.py')
    assert path.is_file()
    source = path.read_text(encoding='utf-8')
    ast.parse(source)
    for reference in references:
        assert reference in source
    if name in ('io_example', 'move_example'):
        assert 'from lebai_interfaces.srv import ' in source


def test_tutorials_have_no_retired_clients():
    assert not list(PACKAGE.rglob('*.cpp'))
    assert not (SCRIPTS / 'robot_state.py').exists()
    forbidden = (
        'rclpy', 'lebai_msgs', 'industrial_', '/io_service/', '/motion_service/',
        '/system_service/', '/robot_status', '/io_status', '/gripper_status',
    )
    for path in SCRIPTS.glob('*.py'):
        source = path.read_text(encoding='utf-8')
        for reference in forbidden:
            assert reference not in source, (path, reference)


def test_shared_argument_helpers():
    path = SCRIPTS / 'lebai_tutorials_common.py'
    assert path.is_file()
    helpers = runpy.run_path(str(path))
    parse_six_numbers = helpers['parse_six_numbers']
    assert parse_six_numbers('0,1,2,3,4,5') == [0, 1, 2, 3, 4, 5]
    for value in ('0,1,2,3,4', '0,1,2,3,4,nan', '0,1,2,3,4,5,'):
        with pytest.raises(ValueError):
            parse_six_numbers(value)

    amplitude_to_gripper_joint = helpers['amplitude_to_gripper_joint']
    assert amplitude_to_gripper_joint(50) == pytest.approx(0.5235987756)
    for value in (-1, 101, float('nan')):
        with pytest.raises(ValueError):
            amplitude_to_gripper_joint(value)


def test_checked_response_keeps_sdk_error_details():
    checked_response = runpy.run_path(str(SCRIPTS / 'lebai_tutorials_common.py'))['checked_response']
    success = MoveJointResponse(result=Result(success=True), motion_id=17)
    assert checked_response('/lebai/motion/movej', success).motion_id == 17

    failure = MoveJointResponse(result=Result(success=False, code=2, message='unavailable'))
    with pytest.raises(RuntimeError, match=r'/lebai/motion/movej failed \(2\): unavailable'):
        checked_response('/lebai/motion/movej', failure)


@pytest.fixture
def run_gripper_example(monkeypatch):
    script = SCRIPTS / 'moveit_gripper_amplitude_example.py'
    monkeypatch.syspath_prepend(str(SCRIPTS))
    monkeypatch.setattr(rospy, 'init_node', Mock())
    client = Mock(spec=actionlib.SimpleActionClient)
    client.wait_for_server.return_value = True
    client.wait_for_result.return_value = True
    client.get_result.return_value = GripperCommandResult(reached_goal=True)
    create_client = Mock(return_value=client)
    monkeypatch.setattr(actionlib, 'SimpleActionClient', create_client)

    def run(max_effort):
        monkeypatch.setattr(sys, 'argv', [str(script), '--amplitude', '50', f'--max-effort={max_effort}'])
        with pytest.raises(SystemExit) as exit_status:
            runpy.run_path(str(script), run_name='__main__')
        return exit_status.value.code, create_client, client

    return run


@pytest.mark.parametrize('max_effort', ['nan', 'inf', '-inf'])
def test_gripper_example_rejects_nonfinite_max_effort(run_gripper_example, capsys, max_effort):
    exit_code, create_client, client = run_gripper_example(max_effort)
    create_client.assert_not_called()
    client.send_goal.assert_not_called()
    assert exit_code == 2
    assert '--max-effort must be finite' in capsys.readouterr().err


@pytest.mark.parametrize('max_effort', ['0', '-1'])
def test_gripper_example_passes_through_nonpositive_finite_effort(run_gripper_example, max_effort):
    exit_code, _, client = run_gripper_example(max_effort)
    assert exit_code == 0
    client.send_goal.assert_called_once()
    assert client.send_goal.call_args.args[0].command.max_effort == float(max_effort)
