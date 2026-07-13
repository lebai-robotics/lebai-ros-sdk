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

import importlib.util
import inspect
from pathlib import Path
import re
import signal

from ament_index_python.packages import get_package_share_path
from launch import LaunchContext, LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.utilities import (
    normalize_to_list_of_substitutions,
    perform_substitutions,
)
from launch_ros.actions import Node
import pytest


PACKAGE_DIR = Path(__file__).resolve().parents[1]
SOURCE_LAUNCH_DIR = PACKAGE_DIR / "launch"
INSTALLED_LAUNCH_DIR = get_package_share_path("lebai_lm3_support") / "launch"
DISPLAY_GRAPH_TEST = PACKAGE_DIR / "test" / "test_display_launch_graph.py"
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
DIRECT_DISPLAY_LAUNCHES = EXPECTED_LAUNCHES - {
    "standalone_lm3.launch.py",
}
DISPLAY_NODE_PACKAGES = {
    "joint_state_publisher_gui",
    "robot_state_publisher",
    "rviz2",
}
NAMESPACE_CASES = [
    pytest.param("", "/", id="root"),
    pytest.param("test_robot", "/test_robot", id="test_robot"),
]


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


@pytest.mark.parametrize("launch_name", sorted(EXPECTED_LAUNCHES))
@pytest.mark.parametrize(("namespace", "expected_namespace"), NAMESPACE_CASES)
def test_display_launch_namespace_surface_resolves_for_every_node(
    launch_name,
    namespace,
    expected_namespace,
):
    context = LaunchContext()
    description = PythonLaunchDescriptionSource(
        str(SOURCE_LAUNCH_DIR / launch_name)
    ).get_launch_description(context)
    namespace_argument = _one_entity(
        description,
        DeclareLaunchArgument,
        lambda entity: entity.name == "namespace",
    )

    default_namespace = perform_substitutions(
        context,
        namespace_argument.default_value,
    )
    assert default_namespace == ""
    context.launch_configurations["namespace"] = namespace

    if launch_name in DIRECT_DISPLAY_LAUNCHES:
        nodes = [
            entity
            for entity in description.entities
            if isinstance(entity, Node)
        ]
        assert {node.node_package for node in nodes} == DISPLAY_NODE_PACKAGES
        for node in nodes:
            resolved = _resolve(context, node._Node__node_namespace)
            assert _absolute_namespace(resolved) == expected_namespace
    else:
        includes = [
            entity
            for entity in description.entities
            if isinstance(entity, IncludeLaunchDescription)
        ]
        assert len(includes) == 2
        for include in includes:
            arguments = {
                _resolve(context, name): _resolve(context, value)
                for name, value in include.launch_arguments
            }
            assert _absolute_namespace(arguments["namespace"]) == (
                expected_namespace
            )


def test_display_graph_launch_test_is_registered_with_cmake():
    cmake_source = (PACKAGE_DIR / "CMakeLists.txt").read_text()
    matches = re.findall(
        r"add_test\(\s+NAME\s+(\S+)\s+COMMAND\s+(.*?)"
        r"\s+WORKING_DIRECTORY",
        cmake_source,
        flags=re.DOTALL,
    )
    commands = {
        name: " ".join(command.split())
        for name, command in matches
    }

    assert set(commands) == {
        "test_display_launch_graph",
        "test_gripper_mimic",
        "test_launch_inventory",
        "test_package_dependencies",
        "test_robot_models",
        "test_rviz_config",
    }
    assert "test/test_display_launch_graph.py" in (
        commands["test_display_launch_graph"]
    )
    assert "--no-xvfb" not in commands["test_display_launch_graph"]
    for name, command in commands.items():
        if name != "test_display_launch_graph":
            assert "--no-xvfb" in command, name


def test_display_graph_outer_matrix_contains_all_fourteen_cases(monkeypatch):
    module = _load_display_graph_test(monkeypatch)

    assert len(module.DISPLAY_CASES) == 14
    assert hasattr(module, "test_display_launch_graph_case")
    assert not hasattr(module, "generate_test_description")


@pytest.mark.hermetic
def test_display_graph_outer_case_starts_isolated_child_and_accepts_success(
    monkeypatch,
):
    module = _load_display_graph_test(monkeypatch)
    calls = []

    class SuccessfulProcess:
        pid = 1234
        returncode = 0

        def communicate(self, timeout=None):
            assert timeout == 90
            return "child passed\n", None

    def record_popen(command, **kwargs):
        calls.append((command, kwargs))
        return SuccessfulProcess()

    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("expected Popen"),
    )
    monkeypatch.setattr(module.subprocess, "Popen", record_popen)
    module.test_display_launch_graph_case(3, object())

    assert len(calls) == 1
    command, kwargs = calls[0]
    assert command[-2:] == ["-q", "--no-xvfb"]
    assert kwargs["start_new_session"] is True
    assert kwargs["stdout"] is module.subprocess.PIPE
    assert kwargs["stderr"] is module.subprocess.STDOUT
    assert kwargs["text"] is True
    assert kwargs["env"][module.CASE_INDEX_ENV] == "3"
    assert kwargs["env"]["RMW_IMPLEMENTATION"] == "rmw_cyclonedds_cpp"
    assert not any(
        forbidden in " ".join(command)
        for forbidden in ("robot_ip", "server", "controller")
    )


@pytest.mark.hermetic
def test_display_graph_outer_case_reports_nonzero_child_output(monkeypatch):
    module = _load_display_graph_test(monkeypatch)

    class FailedProcess:
        pid = 2345
        returncode = 7

        @staticmethod
        def communicate(timeout=None):
            assert timeout == 90
            return "child failure details\n", None

    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("expected Popen"),
    )
    monkeypatch.setattr(
        module.subprocess,
        "Popen",
        lambda *_args, **_kwargs: FailedProcess(),
    )

    with pytest.raises(AssertionError, match="child failure details"):
        module.test_display_launch_graph_case(3, object())


@pytest.mark.hermetic
def test_display_graph_outer_case_kills_process_group_on_timeout(monkeypatch):
    module = _load_display_graph_test(monkeypatch)
    kill_calls = []

    class TimedOutProcess:
        pid = 3456
        returncode = None

        def __init__(self):
            self.communicate_timeouts = []

        def communicate(self, timeout=None):
            self.communicate_timeouts.append(timeout)
            if len(self.communicate_timeouts) == 1:
                raise module.subprocess.TimeoutExpired(
                    cmd="child",
                    timeout=timeout,
                    output=b"startup output\n",
                )
            if len(self.communicate_timeouts) == 2:
                raise module.subprocess.TimeoutExpired(
                    cmd="child",
                    timeout=timeout,
                    output="shutdown output\n",
                )
            self.returncode = -signal.SIGKILL
            return "killed output\n", None

    process = TimedOutProcess()
    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("expected Popen"),
    )
    monkeypatch.setattr(
        module.subprocess,
        "Popen",
        lambda *_args, **_kwargs: process,
    )
    monkeypatch.setattr(
        module.os,
        "killpg",
        lambda pid, sig: kill_calls.append((pid, sig)),
    )

    with pytest.raises(AssertionError, match="timed out") as error:
        module.test_display_launch_graph_case(3, object())

    assert process.communicate_timeouts == [90, 5, None]
    assert kill_calls == [
        (process.pid, signal.SIGTERM),
        (process.pid, signal.SIGKILL),
    ]
    assert "startup output" in str(error.value)
    assert "killed output" in str(error.value)


def test_display_graph_child_defines_one_case_and_scopes_domain(
    monkeypatch,
):
    selected_index = 3
    module = _load_display_graph_test(monkeypatch, selected_index)

    assert not hasattr(module, "test_display_launch_graph_case")
    assert hasattr(module, "generate_test_description")
    test_runs = list(module.generate_test_description())
    assert len(test_runs) == 1
    _partial, launch_arguments = test_runs[0]
    expected = module.DISPLAY_CASES[selected_index]
    assert launch_arguments == dict(zip(
        (
            "launch_name",
            "namespace",
            "domain_id",
            "rviz_config_name",
        ),
        expected,
    ))

    generator = inspect.unwrap(module.generate_test_description)
    domain_id = expected[2]

    description = generator(
        expected[0],
        expected[1],
        domain_id,
        expected[3],
    )
    set_domain, include = description.entities[:2]

    assert isinstance(set_domain, SetEnvironmentVariable)
    assert isinstance(include, IncludeLaunchDescription)
    context = LaunchContext()
    set_domain.execute(context)
    assert context.environment["ROS_DOMAIN_ID"] == str(domain_id)


def _load_display_graph_test(monkeypatch, selected_index=None):
    if selected_index is None:
        monkeypatch.delenv("LEBAI_DISPLAY_GRAPH_CASE_INDEX", raising=False)
        suffix = "outer"
    else:
        monkeypatch.setenv(
            "LEBAI_DISPLAY_GRAPH_CASE_INDEX",
            str(selected_index),
        )
        suffix = f"child_{selected_index}"
    spec = importlib.util.spec_from_file_location(
        f"_display_launch_graph_{suffix}",
        DISPLAY_GRAPH_TEST,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _one_entity(description, entity_type, predicate):
    matches = [
        entity
        for entity in description.entities
        if isinstance(entity, entity_type) and predicate(entity)
    ]
    assert len(matches) == 1
    return matches[0]


def _absolute_namespace(namespace):
    stripped = namespace.strip("/")
    return f"/{stripped}" if stripped else "/"


def _resolve(context, value):
    return perform_substitutions(
        context,
        normalize_to_list_of_substitutions(value),
    )
