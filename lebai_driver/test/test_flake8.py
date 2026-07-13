# Copyright 2022-2026 Shanghai Lebai Robotics Co., Ltd.
# Copyright 2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from configparser import ConfigParser

from ament_flake8.main import main_with_errors
from linter_paths import maintained_python_paths, REPOSITORY_ROOT
import pytest


FLAKE8_CONFIG = REPOSITORY_ROOT / 'scripts' / 'ament_flake8.ini'


@pytest.mark.flake8
@pytest.mark.linter
def test_flake8_config_uses_stable_core_rules():
    config = ConfigParser()

    assert config.read(FLAKE8_CONFIG) == [str(FLAKE8_CONFIG)]
    assert config['flake8']['select'] == 'E,F,W,C90'
    assert config['flake8'].getint('max-line-length') == 99
    assert config['flake8'].getboolean('show-source')
    assert config['flake8'].getboolean('statistics')


@pytest.mark.flake8
@pytest.mark.linter
def test_flake8():
    rc, errors = main_with_errors(
        argv=[
            '--config',
            str(FLAKE8_CONFIG),
            *(str(path) for path in maintained_python_paths()),
        ],
    )
    assert rc == 0, \
        'Found %d code style errors / warnings:\n' % len(errors) + \
        '\n'.join(errors)
