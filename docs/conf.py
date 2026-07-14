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

project = 'lebai-ros-sdk'
copyright = '2026, Lebai Robotics'
author = 'Lebai Robotics'
language = 'zh_CN'
version = 'ROS2 Lyrical'
release = 'ROS2 Lyrical / Ubuntu 26.04 / lyrical-dev'

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'superpowers']

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'display_version': True,
    'titles_only': True,
}
html_title = 'Lebai ROS2 SDK 文档'
html_static_path = ['_static']
html_js_files = ['version-switcher.js']
