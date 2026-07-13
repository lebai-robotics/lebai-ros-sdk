# Copyright 2022-2026 Shanghai Lebai Robotics Co., Ltd.
# Copyright 2015 Open Source Robotics Foundation, Inc.
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

from ament_copyright.main import main
from linter_paths import maintained_python_paths
from pathlib import Path
import pytest
import subprocess


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_PATHS = (
    'docs/*.py',
    'lebai_driver/setup.py',
    'lebai_driver/launch/*.py',
    'lebai_driver/lebai_driver/*.py',
    'lebai_driver/test/*.py',
    'lebai_lm3_support/launch/*.py',
    'lebai_lm3_support/launch/display_gripper.launch',
    'lebai_lm3_support/test/*.py',
    'lebai_lm3_moveit_config/launch/*.py',
    'lebai_lm3_moveit_config/test/*.py',
    'lebai_tutorials/scripts/*.py',
    'lebai_tutorials/test/*.py',
)
APPROVED_NOTICE = '# Copyright 2022-2026 Shanghai Lebai Robotics Co., Ltd.'
APACHE_BOILERPLATE = '''# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.'''
EXCLUDED_PREFIXES = (
    'build/',
    'install/',
    'log/',
    'site/',
    'docs/superpowers/',
)


def _expected_source_paths():
    result = subprocess.run(
        [
            'git',
            'ls-files',
            '-co',
            '--exclude-standard',
            '--',
            *SOURCE_PATHS,
        ],
        cwd=REPOSITORY_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return tuple(sorted(result.stdout.splitlines()))


def _selected_source_paths():
    return tuple(maintained_python_paths())


@pytest.mark.linter
def test_linter_paths_match_git_source_selection(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    selected = _selected_source_paths()
    relative = tuple(
        path.relative_to(REPOSITORY_ROOT).as_posix()
        for path in selected
    )

    assert all(path.is_absolute() for path in selected)
    assert relative == _expected_source_paths()
    assert 'lebai_lm3_support/launch/display_gripper.launch' in relative


@pytest.mark.linter
def test_linter_paths_exclude_generated_output():
    relative = (
        path.relative_to(REPOSITORY_ROOT).as_posix()
        for path in _selected_source_paths()
    )

    assert all(
        not path.startswith(EXCLUDED_PREFIXES)
        for path in relative
    )


@pytest.mark.copyright
@pytest.mark.linter
def test_maintained_sources_have_approved_header():
    missing_notice = []
    missing_license = []

    for path in maintained_python_paths():
        content = path.read_text(encoding='utf-8')
        relative = path.relative_to(REPOSITORY_ROOT).as_posix()
        if APPROVED_NOTICE not in content.splitlines()[:3]:
            missing_notice.append(relative)
        if APACHE_BOILERPLATE not in content:
            missing_license.append(relative)

    assert not missing_notice, f'Missing approved notice: {missing_notice}'
    assert not missing_license, f'Missing Apache boilerplate: {missing_license}'


@pytest.mark.copyright
@pytest.mark.linter
def test_copyright():
    rc = main(argv=[str(path) for path in maintained_python_paths()])
    assert rc == 0, 'Found errors'
