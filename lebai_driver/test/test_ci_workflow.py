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

import os
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
    job = next(iter(_workflow()['jobs'].values()))
    return job['steps']


def _workflow():
    return yaml.safe_load(WORKFLOW_PATH.read_text(encoding='utf-8'))


def _install_dependencies_script():
    steps = {step.get('name'): step for step in _workflow_steps()}
    return steps['Install dependencies']['run']


def _rosdep_retry_loop():
    install = _install_dependencies_script()
    start_marker = 'for attempt in 1 2 3; do'
    end_marker = '\ndone\n'

    assert start_marker in install
    start = install.index(start_marker)
    assert end_marker in install[start:]
    end = install.index(end_marker, start) + len(end_marker)
    return install[start:end]


def _write_executable(path, script):
    path.write_text(script, encoding='utf-8')
    path.chmod(0o755)


def _read_records(path):
    if not path.exists():
        return []
    return path.read_text(encoding='utf-8').splitlines()


def _run_rosdep_retry_loop(tmp_path, failures):
    bin_dir = tmp_path / 'bin'
    bin_dir.mkdir()
    attempts_file = tmp_path / 'attempts'
    sleeps_file = tmp_path / 'sleeps'
    _write_executable(
        bin_dir / 'rosdep',
        '''#!/usr/bin/env bash
count=0
if [ -f "$ATTEMPTS_FILE" ]; then
  count=$(wc -l < "$ATTEMPTS_FILE")
fi
count=$((count + 1))
printf '%s\\n' "$count" >> "$ATTEMPTS_FILE"
[ "$count" -gt "$ROSDEP_FAILURES" ]
''',
    )
    _write_executable(
        bin_dir / 'sleep',
        '''#!/usr/bin/env bash
printf '%s\\n' "$1" >> "$SLEEPS_FILE"
''',
    )
    env = {
        **os.environ,
        'ATTEMPTS_FILE': str(attempts_file),
        'PATH': f'{bin_dir}:{os.environ["PATH"]}',
        'ROSDEP_FAILURES': str(failures),
        'SLEEPS_FILE': str(sleeps_file),
    }
    result = subprocess.run(
        ['bash', '-c', f'set -eo pipefail\n{_rosdep_retry_loop()}'],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )
    return (
        result,
        _read_records(attempts_file),
        _read_records(sleeps_file),
    )


def test_workflow_has_one_job_without_a_strategy_matrix():
    jobs = _workflow()['jobs']

    assert len(jobs) == 1
    assert 'strategy' not in next(iter(jobs.values()))


def test_install_dependencies_uses_latest_compatible_pylebai():
    install = _install_dependencies_script()

    assert install.startswith('set -eo pipefail\n')
    assert (
        'python3 -m pip install "pylebai>=2.0.0,<3.0.0"' in install
    )
    assert '${{ matrix.' not in WORKFLOW_PATH.read_text(encoding='utf-8')


def test_rosdep_retry_succeeds_immediately_without_sleep_or_log(tmp_path):
    result, attempts, sleeps = _run_rosdep_retry_loop(tmp_path, failures=0)

    assert result.returncode == 0
    assert attempts == ['1']
    assert sleeps == []
    assert result.stdout == ''
    assert result.stderr == ''


def test_rosdep_retry_succeeds_on_third_attempt(tmp_path):
    result, attempts, sleeps = _run_rosdep_retry_loop(tmp_path, failures=2)

    assert result.returncode == 0
    assert attempts == ['1', '2', '3']
    assert sleeps == ['5', '5']
    assert result.stderr.splitlines() == [
        'rosdep update failed on attempt 1; retrying in 5 seconds',
        'rosdep update failed on attempt 2; retrying in 5 seconds',
    ]


def test_rosdep_retry_fails_after_third_attempt_without_final_sleep(tmp_path):
    result, attempts, sleeps = _run_rosdep_retry_loop(tmp_path, failures=3)

    assert result.returncode != 0
    assert attempts == ['1', '2', '3']
    assert sleeps == ['5', '5']
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
        'lebai_interfaces lebai_driver lebai_resources lebai_lm3_support '
        'lebai_tutorials'
    )

    assert f'--from-paths {active_packages}' in install
    assert f'--packages-select {active_packages}' in build
    assert 'lebai_lm3_moveit_config' not in unit_tests
