# Copyright 2022-2026 Shanghai Lebai Robotics Co., Ltd.
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

from pathlib import Path

import pytest
import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
LINTER_SCRIPT = REPOSITORY_ROOT / 'scripts' / 'run-linters.sh'
WORKFLOW_PATH = next(
    (REPOSITORY_ROOT / '.github' / 'workflows').glob('ros2_*_ci.yml')
)


def _workflow_steps():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding='utf-8'))
    job = next(iter(workflow['jobs'].values()))
    return job['steps']


def test_container_trusts_checked_out_workspace_before_linting():
    steps = _workflow_steps()
    linter_index = next(
        index for index, step in enumerate(steps)
        if step.get('name') == 'Run linters'
    )
    setup = '\n'.join(
        step.get('run', '') for step in steps[:linter_index]
    )

    assert 'git config --global --add safe.directory "$GITHUB_WORKSPACE"' in setup


def test_linter_script_disables_launch_testing_plugin():
    script = LINTER_SCRIPT.read_text(encoding='utf-8')

    assert '-p no:launch_testing' in script
    assert '-p no:launch_ros' in script


@pytest.mark.skipif(
    'lyrical' not in WORKFLOW_PATH.name,
    reason='MoveIt is released for this ROS distribution',
)
def test_lyrical_ci_defers_unreleased_moveit_package():
    steps = {step.get('name'): step for step in _workflow_steps()}
    install = steps['Install dependencies']['run']
    build = steps['Build']['run']
    unit_tests = steps['Run unit tests']['run']
    active_packages = (
        'lebai_interfaces lebai_driver lebai_resources lebai_lm3_support '
        'lebai_tutorials'
    )

    assert f'--from-paths {active_packages}' in install
    assert f'--packages-select {active_packages}' in build
    assert 'lebai_lm3_moveit_config' not in unit_tests
