import ast
import os
from pathlib import Path
import re
import subprocess


REPO = Path(__file__).resolve().parents[1]
LEGACY_PACKAGE = 'lebai_msgs'
RETIRED = (
    LEGACY_PACKAGE, 'industrial_msgs', 'industrial_robot_client', 'LebaiRobot', 'roscpp',
    'move_example.cpp',
) + tuple(name + '_node.py' for name in ('io_service', 'motion_service', 'robot_state', 'system_service'))
RETIRED_LAUNCHES = tuple(name + '.launch' for name in (
    'io_service', 'motion_service', 'robot_state', 'system_service', 'robot_interface',
    'two_robot_interface', 'test_param_utils', 'test_lebai_driver',
))
REFERENCE = re.compile(r'\b(?:' + '|'.join(map(re.escape, RETIRED + RETIRED_LAUNCHES)) + r')\b')
GENERATED_DIRS = {'build', 'devel', 'logs', 'site'}
NEGATIVE_CONTROL_ASSIGNMENTS = {
    Path('test/test_no_legacy_references.py'): {'LEGACY_PACKAGE', 'RETIRED'},
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


def test_no_legacy_references_or_tracked_build_products():
    files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=REPO)
    problems = []
    if (REPO / LEGACY_PACKAGE).exists():
        problems.append(f'legacy package directory: {LEGACY_PACKAGE}')
    for name in files.split(b'\0'):
        if not name:
            continue
        path = Path(os.fsdecode(name))
        if (GENERATED_DIRS.intersection(path.parts) or path.suffix == '.whl'
                or any(part.endswith('.egg-info') for part in path.parts)):
            problems.append(f'{path}: tracked build product')
            continue
        if REFERENCE.search(str(path)) or (path.parts[0] == 'lebai_tutorials' and path.suffix == '.cpp'):
            problems.append(f'{path}: retired path')
        data = (REPO / path).read_bytes()
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
        for number, line in enumerate(lines):
            if number in history:
                continue
            for match in REFERENCE.finditer(line):
                problems.append(f'{path}:{number + 1}: {match.group()}')
    assert not problems, '\n' + '\n'.join(problems)
