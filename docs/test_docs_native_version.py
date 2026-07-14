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

from __future__ import annotations

import importlib.util
from pathlib import Path


DOCS_DIR = Path(__file__).resolve().parent


def load_conf():
    spec = importlib.util.spec_from_file_location("docs_conf", DOCS_DIR / "conf.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_docs_use_sphinx_native_version_metadata():
    conf = load_conf()

    assert conf.version == "ROS2 Lyrical"
    assert conf.release == "ROS2 Lyrical / Ubuntu 26.04 / lyrical-dev"
    assert conf.html_theme_options["display_version"] is True


def test_docs_do_not_use_custom_version_badge_assets():
    assert not (DOCS_DIR / "_templates" / "version-badge.html").exists()
    assert not (DOCS_DIR / "_templates" / "layout.html").exists()
    assert not (DOCS_DIR / "_static" / "version-badge.css").exists()
