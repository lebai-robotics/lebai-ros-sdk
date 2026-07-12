from pathlib import Path
import runpy
import xml.etree.ElementTree as ET

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
import setuptools


SUPPORTED_PYLEBAI_REQUIREMENT = 'pylebai>=2.0.0,<3.0.0'
PACKAGE_DIR = Path(__file__).resolve().parents[1]
REPOSITORY = PACKAGE_DIR.parent


def test_setup_requires_supported_pylebai_versions(monkeypatch):
    setup_metadata = {}
    setup_path = Path(__file__).resolve().parents[1] / 'setup.py'
    monkeypatch.setattr(
        setuptools,
        'setup',
        lambda **metadata: setup_metadata.update(metadata),
    )
    monkeypatch.chdir(setup_path.parent)

    runpy.run_path(str(setup_path), run_name='__main__')

    pylebai_requirements = [
        requirement
        for requirement in setup_metadata['install_requires']
        if Requirement(requirement).name == 'pylebai'
    ]
    assert pylebai_requirements == [SUPPORTED_PYLEBAI_REQUIREMENT]

    specifiers = SpecifierSet(
        str(Requirement(pylebai_requirements[0]).specifier),
    )
    assert '1.4.4' not in specifiers
    assert '2.0.0' in specifiers
    assert '2.9.9' in specifiers
    assert '3.0.0' not in specifiers


def test_geometry_runtime_dependencies_are_declared():
    driver_manifest = ET.parse(PACKAGE_DIR / 'package.xml').getroot()
    driver_dependencies = {
        dependency.text
        for dependency in driver_manifest.findall('exec_depend')
    }
    interface_manifest = ET.parse(
        REPOSITORY / 'lebai_interfaces' / 'package.xml'
    ).getroot()
    interface_dependencies = {
        dependency.text
        for dependency in interface_manifest.findall('depend')
    }

    assert {'geometry_msgs', 'tf_transformations'} <= driver_dependencies
    assert 'geometry_msgs' in interface_dependencies
