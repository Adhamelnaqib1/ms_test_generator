
import sys
import argparse

from validator import validate_input
from llm_client import generate_tests
from output_cleaner import enforce_constraints


def main():
    parser = argparse.ArgumentParser(
        description='Generate unit tests for Python functions'
    )
    parser.add_argument(
        'file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='Python file containing function (default: stdin)'
    )

    args = parser.parse_args()

    try:
        user_code = args.file.read()
    except Exception:
        print("Error: This tool only generates unit tests for Python functions", file=sys.stderr)
        sys.exit(1)
    finally:
        if args.file is not sys.stdin:
            args.file.close()

    is_valid, result = validate_input(user_code)
    if not is_valid:
        print(result, file=sys.stderr)
        sys.exit(1)

    cleaned_code = result

    try:
        raw_tests = generate_tests(cleaned_code)
    except Exception:
        print("Error: This tool only generates unit tests for Python functions", file=sys.stderr)
        sys.exit(1)

    try:
        final_tests = enforce_constraints(raw_tests)
    except ValueError:
        print("Error: This tool only generates unit tests for Python functions", file=sys.stderr)
        sys.exit(1)


    print(final_tests)


if __name__ == '__main__':
    main()