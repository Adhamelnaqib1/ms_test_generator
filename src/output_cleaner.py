import ast
import re


def clean_output(raw_output: str) -> str:
    cleaned = re.sub(r'```python\s*', '', raw_output)
    cleaned = re.sub(r'```\s*', '', cleaned)
    lines = cleaned.split('\n')
    code_lines = []
    in_code = False
    for line in lines:
        stripped = line.strip()
        if not in_code and (stripped.startswith('import') or stripped.startswith('from') or stripped.startswith('def') or stripped.startswith('class')):
            in_code = True
        if in_code:
            code_lines.append(line)

    while code_lines and not code_lines[-1].strip():
        code_lines.pop()

    result = '\n'.join(code_lines)

    try:
        ast.parse(result)
    except SyntaxError:
        raise ValueError("Error: This tool only generates unit tests for Python functions")

    tree = ast.parse(result)
    has_test = any(
        isinstance(node, (ast.FunctionDef, ast.ClassDef)) and 'test' in node.name.lower()
        for node in ast.walk(tree)
    )
    if not has_test:
        raise ValueError("Error: This tool only generates unit tests for Python functions")

    return result


def enforce_constraints(raw_output: str) -> str:
    forbidden = ['here are', 'below is', 'above is', 'the following', 'explanation', 'note:']
    lines = raw_output.split('\n')
    filtered_lines = []
    for line in lines:
        if not any(phrase in line.lower() for phrase in forbidden):
            filtered_lines.append(line)

    filtered = '\n'.join(filtered_lines)
    cleaned = clean_output(filtered)
    return cleaned