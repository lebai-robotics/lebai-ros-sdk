from setuptools import setup
from setuptools import find_packages
import os
from glob import glob

package_name = 'lebai_driver'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'config'),
         glob(os.path.join('config', '*.yaml'))),
    ],
    # install_requires=['setuptools'],
    zip_safe=True,
    maintainer='liufang',
    maintainer_email='liufang_robot@outlook.com',
    description='Lebai driver',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_state = lebai_driver.robot_state.robot_state_node:main',
            'io_service = lebai_driver.io_service.io_service_node:main',
            'system_service = lebai_driver.system_service.system_service_node:main',
            'motion = lebai_driver.motion.motion_node:main',
        ],
    },
)
