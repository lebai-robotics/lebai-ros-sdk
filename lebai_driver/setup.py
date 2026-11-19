## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from catkin_pkg.python_setup import generate_distutils_setup
from setuptools import setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=['lebai_driver'],
    package_dir={'': 'src'},
    install_requires=['pylebai>=2.0.8,<3'],
)

setup(**setup_args)
