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


def maintained_python_paths():
    result = subprocess.run(
        [
            'git',
            'ls-files',
            '-co',
            '--exclude-standard',
            '-z',
            '--',
            *SOURCE_PATHS,
        ],
        cwd=REPOSITORY_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    relative_paths = sorted(filter(None, result.stdout.split('\0')))
    return tuple(REPOSITORY_ROOT / path for path in relative_paths)
