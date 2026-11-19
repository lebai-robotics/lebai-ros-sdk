from pathlib import Path

import pytest


DOCS = Path(__file__).resolve().parent


@pytest.mark.parametrize('path', ['install.rst', '../README.md'])
def test_native_requirements(path):
    documentation = DOCS / path
    assert documentation.is_file()
    contents = documentation.read_text(encoding='utf-8')
    for requirement in ('Noetic', 'Ubuntu 20.04', 'Python 3.8', 'pylebai>=2.0.8,<3'):
        assert requirement in contents


def test_both_lm3_moveit_modes_are_documented():
    documentation = DOCS / 'moveit.rst'
    assert documentation.is_file()
    contents = documentation.read_text(encoding='utf-8')
    for mode in ('has_gripper:=true', 'has_gripper:=false'):
        assert 'roslaunch lebai_lm3_moveit_config lm3.launch ' + mode in contents
