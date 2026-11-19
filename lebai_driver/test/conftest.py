from pathlib import Path
import sys

import pytest

from fakes import FakeRospy


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / 'src'))


@pytest.fixture
def fake_rospy():
    return FakeRospy()
