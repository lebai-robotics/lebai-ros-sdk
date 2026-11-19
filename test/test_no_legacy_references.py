import ast
import os
from pathlib import Path
import re
import subprocess

import pytest


REPO = Path(__file__).resolve().parents[1]
LEGACY_PACKAGE = 'lebai_msgs'
LEGACY_CPP_PACKAGE = 'roscpp'
RETIRED_PACKAGES = (LEGACY_PACKAGE, 'industrial_msgs', 'industrial_robot_client', LEGACY_CPP_PACKAGE)
RETIRED = RETIRED_PACKAGES + (
    'LebaiRobot', 'move_example.cpp',
) + tuple(name + '_node.py' for name in ('io_service', 'motion_service', 'robot_state', 'system_service'))
RETIRED_LAUNCHES = tuple(name + '.launch' for name in (
    'io_service', 'motion_service', 'robot_state', 'system_service', 'robot_interface',
    'two_robot_interface', 'test_param_utils', 'test_lebai_driver',
))
REFERENCE = re.compile(
    r'\b(?:' + '|'.join(map(re.escape, RETIRED + RETIRED_LAUNCHES)) + r')\b'
    # Standard Catkin variable suffixes are uppercase. Lowercase components
    # before the suffix belong to the package name.
    + r'|\b(?:' + '|'.join(map(re.escape, RETIRED_PACKAGES)) + r')_[A-Z][A-Z0-9_]*\b'
)
IMPORT_ALIAS = r'[\w.]+(?:\s+as\s+\w+)?'
TEXT_IMPORT = re.compile(
    r'\bfrom\s+([\w.]+)\s+import\b|\bimport\s+(' + IMPORT_ALIAS + r'(?:\s*,\s*' + IMPORT_ALIAS + r')*)'
)
GENERATED_DIRS = {'build', 'devel', 'install', 'logs', 'site', '__pycache__'}
NEGATIVE_CONTROL_ASSIGNMENTS = {
    Path('test/test_no_legacy_references.py'): {'LEGACY_PACKAGE', 'LEGACY_CPP_PACKAGE', 'RETIRED_PACKAGES', 'RETIRED'},
    Path('lebai_tutorials/test/test_examples.py'): {'forbidden'},
}


def migration_table_lines(lines):
    start, end = '.. BEGIN LEGACY MIGRATION', '.. END LEGACY MIGRATION'
    assert lines.count(start) == lines.count(end) == 1, 'Expected one bounded migration table'
    first, last = lines.index(start), lines.index(end)
    assert first < last and lines[first + 2] == '.. list-table::'
    assert all(not line.strip() or line.startswith('   ') for line in lines[first + 3:last])
    return range(first + 3, last)


def legacy_imports(tree, path):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and not node.level:
            modules = [node.module]
        else:
            continue
        if any(name.split('.')[0] == 'lebai' for name in modules):
            yield f'{path}:{node.lineno}: legacy SDK import'


def remove_negative_control_literals(tree, path, lines):
    assignments = NEGATIVE_CONTROL_ASSIGNMENTS.get(path)
    if not assignments:
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not any(
                isinstance(target, ast.Name) and target.id in assignments for target in node.targets):
            continue
        for literal in ast.walk(node.value):
            if isinstance(literal, ast.Constant) and literal.value in RETIRED:
                i = literal.lineno - 1
                # Python reports UTF-8 byte offsets for AST source spans.
                line = lines[i].encode('utf-8')
                blank = b' ' * (literal.end_col_offset - literal.col_offset)
                lines[i] = (line[:literal.col_offset] + blank + line[literal.end_col_offset:]).decode('utf-8')


def logical_lines(lines):
    start = 1
    parts = []
    for number, line in enumerate(lines, 1):
        if parts and re.search(r'\w$', parts[-1]) and re.match(r'\w', line):
            parts.append(' ')
        if line.endswith('\\'):
            if line[:-1]:
                parts.append(line[:-1])
            continue
        yield start, ''.join(parts) + line
        parts.clear()
        start = number + 1
    if parts:
        yield start, ''.join(parts)


def repository_problems(repo):
    files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=repo)
    problems = []
    if (repo / LEGACY_PACKAGE).exists():
        problems.append(f'legacy package directory: {LEGACY_PACKAGE}')
    for name in files.split(b'\0'):
        if not name:
            continue
        path = Path(os.fsdecode(name))
        if (GENERATED_DIRS.intersection(path.parts) or path.suffix in ('.whl', '.pyc')
                or any(part.endswith('.egg-info') for part in path.parts)):
            problems.append(f'{path}: tracked build product')
            continue
        if REFERENCE.search(str(path)) or (path.parts[0] == 'lebai_tutorials' and path.suffix == '.cpp'):
            problems.append(f'{path}: retired path')
        data = (repo / path).read_bytes()
        if b'\0' in data:
            continue
        source = data.decode('utf-8', errors='replace')
        lines = source.splitlines()
        shebang = lines[0] if lines and lines[0].startswith('#!') else ''
        if path.suffix == '.py' or re.search(r'\bpython[\d.]*\b', shebang):
            tree = ast.parse(source, filename=str(path))
            problems.extend(legacy_imports(tree, path))
            remove_negative_control_literals(tree, path, lines)
        history = migration_table_lines(lines) if path == Path('docs/architecture.rst') else ()
        for index in history:
            lines[index] = ''
        for number, line in enumerate(lines, 1):
            for match in REFERENCE.finditer(line):
                problems.append(f'{path}:{number}: {match.group()}')
        for number, line in logical_lines(lines):
            for match in TEXT_IMPORT.finditer(line):
                if match[2] and re.match(r'\s+\w', line[match.end():]):
                    continue  # Plain prose continues after the apparent module list.
                # Check the module after "from" or each module in a plain import list.
                modules = (match[1] or match[2]).split(',')
                if any(module.split()[0].split('.')[0] == 'lebai' for module in modules):
                    problems.append(f'{path}:{number}: {match.group()}')
    return problems


def test_no_legacy_references_or_tracked_build_products():
    problems = repository_problems(REPO)
    assert not problems, '\n' + '\n'.join(problems)


@pytest.fixture
def scan_tracked_file(tmp_path, monkeypatch):
    for variable in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        monkeypatch.delenv(variable, raising=False)
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path, check=True)

    def scan(name, source):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding='utf-8')
        subprocess.run(['git', 'add', '--', name], cwd=tmp_path, check=True)
        return repository_problems(tmp_path)

    return scan


def test_retired_package_variables(scan_tracked_file):
    contents = (
        'add_dependencies(node ${%s_EXPORTED_TARGETS})\n'
        'target_link_libraries(node ${%s_LIBRARIES})\n'
        'echo "$%s_VERSION"\n'
        'if(%s_FOUND)\n'
    ) % (LEGACY_PACKAGE, LEGACY_CPP_PACKAGE, LEGACY_PACKAGE, LEGACY_CPP_PACKAGE)
    problems = scan_tracked_file('CMakeLists.txt', contents)
    assert [problem.split(':')[1] for problem in problems] == ['1', '2', '3', '4']

    valid = ('add_dependencies(node ${lebai_interfaces_EXPORTED_TARGETS})\n'
             'target_link_libraries(node ${rospy_LIBRARIES})\n'
             'moveit_commander.roscpp_initialize(argv)\n'
             'include_directories(${%s_serialization_INCLUDE_DIRS})\n'
             'echo "$%s_serialization_LIBRARIES"\n') % (LEGACY_CPP_PACKAGE, LEGACY_CPP_PACKAGE)
    assert scan_tracked_file('CMakeLists.txt', valid) == []


@pytest.mark.parametrize('name', ['install/setup.bash', 'module/__pycache__/node.cpython-38.pyc',
                                  'module/node.pyc'])
def test_tracked_install_space_and_bytecode_are_reported(scan_tracked_file, name):
    assert scan_tracked_file(name, '') == [name + ': tracked build product']


def test_documented_import_with_empty_continuation_lines(scan_tracked_file):
    code = 'import\\\n\\\n\\\n' + 'lebai.type\n'
    ast.parse(code)
    assert scan_tracked_file('docs/example.rst', code) == [
        'docs/example.rst:1: import ' + 'lebai.type',
    ]


def test_documented_imports_use_the_new_sdk(scan_tracked_file):
    old_sdk = 'lebai'
    contents = ('.. code-block:: python\n\n'
                '   from %s.type import JointPose\n'
                '   import %s as sdk\n'
                '   import os, %s.robot\n'
                '   import os, \\\n'
                '       %s.type\n'
                'import\\\n'
                '%s.type\n') % (old_sdk, old_sdk, old_sdk, old_sdk, old_sdk)
    problems = scan_tracked_file('docs/install.rst', contents)
    assert [problem.split(':')[1] for problem in problems] == ['3', '4', '5', '6', '8']

    valid = ('   from lebai_interfaces import msg\n'
             '   from pylebai import Robot\n'
             '   import lebai_driver, lebai_interfaces\n'
             '   from local_helpers import lebai\n'
             '   import os, \\\n'
             '       lebai_interfaces.msg\n'
             '   from local_helpers import \\\n'
             '       lebai\n'
             '\nA plain paragraph lists items to import locally,\n'
             'lebai.type metadata among them.\n'
             'Another paragraph lists items to import locally, \\\n'
             'lebai.type metadata among them.\n')
    assert scan_tracked_file('docs/install.rst', valid) == []
    history = ('.. BEGIN LEGACY MIGRATION\n\n.. list-table::\n\n'
               '   * - ``from %s.type import JointPose``\n\n.. END LEGACY MIGRATION\n') % old_sdk
    assert scan_tracked_file('docs/architecture.rst', history) == []
