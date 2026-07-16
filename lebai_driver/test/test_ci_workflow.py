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


def _workflow():
    return yaml.safe_load(WORKFLOW_PATH.read_text(encoding='utf-8'))


def _workflow_job():
    workflow = _workflow()
    return next(iter(workflow['jobs'].values()))


def _workflow_steps():
    return _workflow_job()['steps']


def _install_dependencies_script():
    steps = {step.get('name'): step for step in _workflow_steps()}
    return steps['Install dependencies']['run']


def _rosdep_update_retry_loop():
    lines = _install_dependencies_script().splitlines()
    start = next(
        (
            index for index, line in enumerate(lines)
            if line.strip() == 'for attempt in 1 2 3; do'
        ),
        None,
    )
    assert start is not None, 'rosdep update retry loop is missing'
    end = next(
        (
            index for index, line in enumerate(lines[start + 1:], start + 1)
            if line.strip() == 'done'
        ),
        None,
    )
    assert end is not None, 'rosdep update retry loop is incomplete'
    return '\n'.join(lines[start:end + 1])


def _run_rosdep_update_retry_loop(tmp_path, failures):
    trace_path = tmp_path / 'retry-trace'
    script = f'''\
set -eo pipefail
trace_file=$1
failures=$2
attempts=0

rosdep() {{
  test "$1" = update
  attempts=$((attempts + 1))
  printf 'rosdep:%s\\n' "$attempts" >> "$trace_file"
  if [ "$attempts" -le "$failures" ]; then
    return 1
  fi
  return 0
}}

sleep() {{
  printf 'sleep:%s\\n' "$1" >> "$trace_file"
}}

{_rosdep_update_retry_loop()}
'''
    result = subprocess.run(
        ['bash', '-c', script, 'bash', str(trace_path), str(failures)],
        capture_output=True,
        check=False,
        text=True,
    )
    trace = trace_path.read_text(encoding='utf-8').splitlines()
    return result, trace


def test_ci_has_one_job_without_a_pylebai_matrix():
    workflow = _workflow()

    assert len(workflow['jobs']) == 1
    assert 'strategy' not in _workflow_job()


def test_install_dependencies_preserves_strict_shell_options():
    commands = [
        line.strip() for line in _install_dependencies_script().splitlines()
        if line.strip()
    ]

    assert commands[0] == 'set -eo pipefail'


def test_install_dependencies_uses_latest_compatible_pylebai():
    install = _install_dependencies_script()
    commands = [line.strip() for line in install.splitlines()]

    assert 'python3 -m pip install "pylebai>=2.0.0,<3.0.0"' in commands
    assert 'matrix.' not in install


def test_rosdep_update_retry_stops_after_immediate_success(tmp_path):
    result, trace = _run_rosdep_update_retry_loop(tmp_path, failures=0)

    assert result.returncode == 0
    assert trace == ['rosdep:1']
    assert result.stderr == ''


def test_rosdep_update_retry_succeeds_on_third_attempt(tmp_path):
    result, trace = _run_rosdep_update_retry_loop(tmp_path, failures=2)

    assert result.returncode == 0
    assert trace == [
        'rosdep:1',
        'sleep:5',
        'rosdep:2',
        'sleep:5',
        'rosdep:3',
    ]
    assert result.stderr.splitlines() == [
        'rosdep update failed on attempt 1; retrying in 5 seconds',
        'rosdep update failed on attempt 2; retrying in 5 seconds',
    ]


def test_rosdep_update_retry_fails_after_third_attempt(tmp_path):
    result, trace = _run_rosdep_update_retry_loop(tmp_path, failures=3)

    assert result.returncode != 0
    assert trace == [
        'rosdep:1',
        'sleep:5',
        'rosdep:2',
        'sleep:5',
        'rosdep:3',
    ]
    assert result.stderr.splitlines() == [
        'rosdep update failed on attempt 1; retrying in 5 seconds',
        'rosdep update failed on attempt 2; retrying in 5 seconds',
        'rosdep update failed after 3 attempts',
    ]


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
