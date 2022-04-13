## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=['lebai_driver', 'lebai_driver.io_service',
    'lebai_driver.motion_service','lebai_driver.robot_state',
    'lebai_driver.system_service'],
    package_dir={'': 'src'},
)

setup(**setup_args)
