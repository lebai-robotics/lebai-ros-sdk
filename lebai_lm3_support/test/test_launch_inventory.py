from pathlib import Path

from ament_index_python.packages import get_package_share_path
from launch import LaunchContext, LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import pytest


PACKAGE_DIR = Path(__file__).resolve().parents[1]
SOURCE_LAUNCH_DIR = PACKAGE_DIR / "launch"
INSTALLED_LAUNCH_DIR = get_package_share_path("lebai_lm3_support") / "launch"
EXPECTED_LAUNCHES = frozenset(
    {
        "display_gripper.launch",
        "display_gripper.py",
        "display_lm3.launch.py",
        "display_lm3_l1.launch.py",
        "display_lm3_l1_with_gripper.launch.py",
        "display_lm3_with_gripper.launch.py",
        "standalone_lm3.launch.py",
    }
)


def _launch_names(launch_dir):
    return {
        path.name
        for path in launch_dir.iterdir()
        if path.is_file() or path.is_symlink()
    }


def test_launch_names_include_dangling_symlinks(tmp_path):
    dangling = tmp_path / "obsolete.launch.py"
    dangling.symlink_to(tmp_path / "missing.launch.py")

    assert _launch_names(tmp_path) == {"obsolete.launch.py"}


@pytest.mark.parametrize(
    ("location", "launch_dir"),
    [
        ("source", SOURCE_LAUNCH_DIR),
        ("installed", INSTALLED_LAUNCH_DIR),
    ],
)
def test_launch_inventory_is_exact(location, launch_dir):
    assert _launch_names(launch_dir) == EXPECTED_LAUNCHES, location


def test_installed_launch_entries_are_not_dangling_symlinks():
    dangling = sorted(
        path.name
        for path in INSTALLED_LAUNCH_DIR.iterdir()
        if path.is_symlink() and not path.exists()
    )

    assert not dangling, f"dangling installed launch symlinks: {dangling}"


@pytest.mark.parametrize(
    "launch_name",
    sorted(EXPECTED_LAUNCHES),
)
def test_every_expected_installed_launch_description_loads(launch_name):
    description = PythonLaunchDescriptionSource(
        str(INSTALLED_LAUNCH_DIR / launch_name)
    ).get_launch_description(LaunchContext())

    assert isinstance(description, LaunchDescription)
