from pathlib import Path
from xml.etree import ElementTree

import roslaunch
import yaml

from lebai_driver.parameters import DEFAULT_PARAMETERS


PACKAGE = Path(__file__).resolve().parents[1]


def launch_config(name, *args):
    path = str(PACKAGE / 'launch' / (name + '.launch'))
    return roslaunch.config.load_config_default([(path, list(args))], None, verbose=False)


def test_driver_launch_default_parameters_model_and_remap():
    config = launch_config('driver')
    nodes = {n.name: n for n in config.nodes}
    driver = nodes['lebai_driver']
    assert (driver.namespace, driver.type) == ('/lebai/', 'lebai_driver_node.py')
    for name, default in DEFAULT_PARAMETERS.items():
        param = config.params['/lebai/lebai_driver/' + name]
        assert param.value == ('lebai' if name == 'namespace' else default)
    rsp = nodes['robot_state_publisher']
    assert (rsp.namespace, rsp.package, rsp.type) == ('/lebai/', 'robot_state_publisher', 'robot_state_publisher')
    assert dict(rsp.remap_args)['joint_states'] == 'model/joint_states'
    robot = ElementTree.fromstring(config.params['/lebai/robot_description'].value)
    assert robot.find("joint[@name='gripper_r_joint1']") is not None
    args = ElementTree.parse(PACKAGE / 'launch/driver.launch').getroot().findall('arg')
    assert {arg.get('name'): arg.get('default') for arg in args}['robot_model'] == 'lm3_with_gripper.xacro'


def test_driver_launch_override_all_runtime_arguments():
    values = dict(robot_ip='10.1.1.9', simulator=True, namespace='other', joint_names=list('abcdef'),
                  trajectory_action_name='arm/test', gripper_action_name='/grip/test',
                  gripper_joint_name='grip', io_state_device='flange')
    values.update({k: 2.5 for k in DEFAULT_PARAMETERS if k.endswith('_rate')})
    values.update({k: 3 for k in DEFAULT_PARAMETERS if k.endswith('_count')})
    assert values.keys() == DEFAULT_PARAMETERS.keys()
    args = [k + ':=' + str(v) for k, v in values.items()]
    config = launch_config('driver', 'publish_robot_description:=false', 'robot_model:=missing.xacro', *args)
    driver, = config.nodes
    assert driver.namespace == '/other/'
    assert '/other/robot_description' not in config.params
    for name, value in values.items():
        assert config.params['/other/lebai_driver/' + name].value == value


def test_discovery_and_serial_launch_inputs():
    discovery, = launch_config('discovery').nodes
    assert (discovery.namespace, discovery.name, discovery.type) == (
        '/lebai/', 'lebai_discovery', 'lebai_discovery_node.py')
    assert launch_config('discovery', 'namespace:=other').nodes[0].namespace == '/other/'
    serial = launch_config('serial_gripper')
    node, = serial.nodes
    assert (node.namespace, node.name, node.type) == ('/lebai/', 'lebai_serial_gripper', 'lebai_serial_gripper_node.py')
    assert serial.params['/lebai/lebai_serial_gripper/port_name'].value == '/dev/ttyUSB0'
    assert serial.params['/lebai/lebai_serial_gripper/gripper_state_publish_rate'].value == 10.0
    serial = launch_config('serial_gripper', 'namespace:=other', 'port_name:=/dev/custom', 'gripper_state_publish_rate:=3')
    assert serial.params['/other/lebai_serial_gripper/port_name'].value == '/dev/custom'
    assert serial.params['/other/lebai_serial_gripper/gripper_state_publish_rate'].value == 3.0


def test_joint_name_files_use_ros1_parameter_format():
    def read(model):
        path = PACKAGE / 'config' / ('joint_names_' + model + '.yaml')
        return yaml.safe_load(path.read_text())

    assert read('lm3')['controller_joint_names'] == DEFAULT_PARAMETERS['joint_names']
    assert read('gripper')['gripper_joint_names'] == [
        'gripper_l_joint1', 'gripper_l_joint2', 'gripper_l_joint_finger',
        'gripper_r_joint1', 'gripper_r_joint2', 'gripper_r_joint_finger',
    ]
