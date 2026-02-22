import ast
import io
import re
import tokenize

FORBIDDEN_PATTERNS = [
    r'ignore\s+(previous|above|instruction)',
    r'system\s*:',
    r'user\s*:',
    r'assistant\s*:',
    r'<\s*/\s*instruction\s*>',
    r'\[\s*INST\s*\]',
]


def contains_function(code: str) -> bool:
    try:
        tree = ast.parse(code)
        return any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))
    except SyntaxError:
        return False


def check_prompt_injection(code: str) -> tuple[bool, str]:
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            return False, "Error: This tool only generates unit tests for Python functions"
    return True, ""


def sanitize(source_code):
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source_code).readline)
        result = []
        for tok_type, tok_val, _, _, _ in tokens:
            if tok_type == tokenize.COMMENT:
                continue
            result.append((tok_type, tok_val))
        return tokenize.untokenize(result).strip()
    except:
        return source_code.strip()


def validate_input(user_input: str) -> tuple[bool, str]:
    if not contains_function(user_input):
        return False, "Error: This tool only generates unit tests for Python functions"
    is_safe, msg = check_prompt_injection(user_input)
    if not is_safe:
        return False, "Error: This tool only generates unit tests for Python functions"
    cleaned = sanitize(user_input)

    try:
        ast.parse(cleaned)
    except SyntaxError as e:
        return False, "Error: This tool only generates unit tests for Python functions"

    return True, cleaned