# MS Test Generator

A CLI-based AI developer tool that automatically generates high-quality unit tests for any given Python function. It uses the Groq API with strict output constraints to behave like a specialized developer tool, not a chatbot.

## Requirements

- Python 3.10+
- A Groq API key (free at [console.groq.com](https://console.groq.com))

## Installation

Clone the repository:

```bash
git clone https://github.com/Adhamelnaqib1/ms-test-generator.git
cd ms_test_generator
```

Install dependencies:

```bash
pip install groq python-dotenv
```

Create a `.env` file inside the `src` directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Project Structure

```
ms-test-generator/
├── src/
│   ├── cli.py              # CLI logic and argument parsing
│   ├── validator.py        # Input validation, sanitization, prompt injection prevention
│   ├── llm_client.py       # Groq API interaction and system prompt
│   ├── output_cleaner.py   # Output enforcement and cleaning
│   └── .env                # API key (not committed)
├── sample.py               # Example function for testing
├── .gitignore
└── README.md
```

## Usage

Navigate into the `src` directory and run:

```bash
cd src
python cli.py ../your_function.py
```

**Example:**

Given `sample.py`:

```python
def add(a, b):
    return a + b
```

Run:

```bash
cd src
python cli.py ../sample.py
```

Output:

```python
from user_code import *
import pytest

def test_add_normal_case():
    assert add(1, 2) == 3

def test_add_negative_numbers():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 0) == 0
...
```

Save output directly to a file:

```bash
python cli.py ../sample.py > test_sample.py
```

## How It Works

1. The input file is read and validated, it must contain at least one Python function
2. The source code is scanned for prompt injection patterns
3. Comments are stripped using Python's `tokenize` module before being sent to the LLM
4. The Groq API is called with a strict system prompt and `temperature=0` for deterministic output
5. The raw output is cleaned, markdown fences and prose are stripped, and the result is validated with `ast.parse()` before being printed

## Constraints

- Input must be a Python file containing at least one function
- Any other input returns: `Error: This tool only generates unit tests for Python functions`
- Output is raw Python pytest code only — no explanations, no markdown, no commentary

## Security

- API key is loaded from `.env` and never exposed
- Source code comments are stripped before being sent to the LLM to prevent prompt injection
- Common prompt injection patterns are detected and rejected