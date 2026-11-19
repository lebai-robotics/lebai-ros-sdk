import re
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path("lebai_interfaces")
HUMBLE_BASELINE = "15860fdfa3cbef29892a3d139b813a840903a926"
HUMBLE_TREE = subprocess.run(
    [
        "git", "ls-tree", "-r", "--name-only", HUMBLE_BASELINE, "--",
        str(PACKAGE / "msg"), str(PACKAGE / "srv"),
    ],
    cwd=REPO_ROOT,
    capture_output=True,
    text=True,
)
HUMBLE_FILES = tuple(
    Path(filename)
    for filename in HUMBLE_TREE.stdout.splitlines()
    if Path(filename).suffix in (".msg", ".srv")
)
ROS2_QUALIFICATION = re.compile(r"^(\s*lebai_interfaces/)(?:msg|srv)/")


def require_humble_baseline():
    assert HUMBLE_TREE.returncode == 0, (
        f"Humble baseline {HUMBLE_BASELINE} is unavailable. "
        "For a shallow checkout, run `git fetch --unshallow origin humble-dev`. "
        "For a full checkout, run `git fetch origin humble-dev`.\n"
        f"{HUMBLE_TREE.stderr.strip()}"
    )
    assert HUMBLE_FILES, f"Humble baseline {HUMBLE_BASELINE} contains no interfaces"


def normalize_definition(definition):
    lines = []
    for line in definition.splitlines():
        content, comment_marker, _ = line.partition("#")
        if content.strip():
            if comment_marker:
                content = content.rstrip()
            lines.append(ROS2_QUALIFICATION.sub(r"\1", content))
    return lines


def assert_file_set_matches_humble(directory, suffix):
    require_humble_baseline()
    package_directory = REPO_ROOT / PACKAGE / directory
    actual = {
        path.relative_to(REPO_ROOT)
        for path in package_directory.rglob(f"*{suffix}")
        if path.is_file()
    }
    expected = {path for path in HUMBLE_FILES if path.suffix == suffix}
    assert actual == expected


def test_message_file_set_matches_humble():
    assert_file_set_matches_humble("msg", ".msg")


def test_service_file_set_matches_humble():
    assert_file_set_matches_humble("srv", ".srv")


@pytest.mark.parametrize(
    "relative_path",
    [pytest.param(path, id=str(path.relative_to(PACKAGE))) for path in HUMBLE_FILES]
    or [pytest.param(None, id="unavailable-humble-baseline")],
)
def test_normalized_definition_matches_humble(relative_path):
    require_humble_baseline()
    actual = REPO_ROOT / relative_path
    assert actual.is_file(), f"Missing interface definition: {relative_path}"
    expected = subprocess.run(
        ["git", "show", f"{HUMBLE_BASELINE}:{relative_path.as_posix()}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert normalize_definition(actual.read_text(encoding="utf-8")) == normalize_definition(expected)
