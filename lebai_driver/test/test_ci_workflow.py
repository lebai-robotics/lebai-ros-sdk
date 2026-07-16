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
import subprocess

import pytest
import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
LINTER_SCRIPT = REPOSITORY_ROOT / 'scripts' / 'run-linters.sh'
WORKFLOW_PATH = next(
    (REPOSITORY_ROOT / '.github' / 'workflows').glob('ros2_*_ci.yml')
)


def _workflow_steps():
    return _workflow_job()['steps']


def _workflow_job():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding='utf-8'))
    return next(iter(workflow['jobs'].values()))


def _install_script():
    steps = {step.get('name'): step for step in _workflow_steps()}
    return steps['Install dependencies']['run']


def _rosdep_retry_script():
    install = _install_script()
    start_marker = 'for attempt in 1 2 3; do'
    assert start_marker in install, 'rosdep update must have a bounded retry loop'
    start = install.index(start_marker)
    end = install.index('\ndone', start) + len('\ndone')
    return install[start:end]


def _run_rosdep_retry(failures):
    script = f'''\
set -eo pipefail
call_count=0
rosdep() {{
  call_count=$((call_count + 1))
  printf 'attempt=%s\\n' "$call_count"
  if [ "$call_count" -le {failures} ]; then
    return 1
  fi
}}
sleep() {{
  printf 'sleep=%s\\n' "$1"
}}
{_rosdep_retry_script()}
'''
    return subprocess.run(
        ['bash'],
        input=script,
        text=True,
        capture_output=True,
        check=False,
    )


def test_ci_has_one_job_without_a_pylebai_version_matrix():
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding='utf-8'))

    assert len(workflow['jobs']) == 1
    assert 'strategy' not in _workflow_job()


def test_ci_installs_latest_compatible_released_pylebai():
    install = _install_script()

    assert 'python3 -m pip install "pylebai>=2.0.0,<3.0.0"' in install
    assert 'matrix.pylebai' not in install


def test_install_dependencies_enables_strict_shell_error_handling():
    assert _install_script().startswith('set -eo pipefail\n')


def test_rosdep_update_stops_after_success():
    result = _run_rosdep_retry(failures=0)

    assert result.returncode == 0
    assert result.stdout.splitlines() == ['attempt=1']
    assert result.stderr == ''


def test_rosdep_update_retries_twice_before_succeeding():
    result = _run_rosdep_retry(failures=2)

    assert result.returncode == 0
    assert result.stdout.splitlines() == [
        'attempt=1',
        'sleep=5',
        'attempt=2',
        'sleep=5',
        'attempt=3',
    ]
    assert result.stderr.count('retrying in 5 seconds') == 2


def test_rosdep_update_exits_after_the_third_failure():
    result = _run_rosdep_retry(failures=3)

    assert result.returncode != 0
    assert result.stdout.splitlines() == [
        'attempt=1',
        'sleep=5',
        'attempt=2',
        'sleep=5',
        'attempt=3',
    ]
    assert 'rosdep update failed after 3 attempts' in result.stderr


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
        'lebai_interfaces lebai_driver lebai_lm3_support lebai_tutorials'
    )

    assert f'--from-paths {active_packages}' in install
    assert f'--packages-select {active_packages}' in build
    assert 'lebai_lm3_moveit_config' not in unit_tests
