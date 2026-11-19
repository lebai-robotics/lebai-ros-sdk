from pathlib import Path
import runpy
import xml.etree.ElementTree as ET

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


def test_external_driver_examples_disable_duplicate_tf():
    for page in ('moveit.rst', 'architecture.rst'):
        text = (DOCS / page).read_text().replace('\\\n', '')
        commands = [line for line in text.splitlines() if 'roslaunch lebai_driver driver.launch' in line]
        assert commands and all('publish_robot_description:=false' in line for line in commands)


def test_breaking_driver_version_matches_release_documentation():
    repo = DOCS.parent
    version = ET.parse(str(repo / 'lebai_driver/package.xml')).findtext('version')
    assert version == '2.0.0'
    assert runpy.run_path(str(DOCS / 'conf.py'))['release'] == version
    for page in (repo / 'README.md', DOCS / 'architecture.rst'):
        assert version in page.read_text()
