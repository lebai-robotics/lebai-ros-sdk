from pathlib import Path
import runpy

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
import setuptools


SUPPORTED_PYLEBAI_REQUIREMENT = 'pylebai>=2.0.0,<3.0.0'


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
