import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a specialized unit test generator. Your sole purpose is to generate Python unit tests.

STRICT RULES:
1. Output ONLY valid Python code
2. NO markdown code fences (no ```python or ```)
3. NO explanations, NO comments except test docstrings
4. NO introductory text like "Here are the tests:"
5. Use pytest framework
6. Include tests for: normal cases, edge cases, error cases
7. Import the function under test with `from user_code import *`
8. Output must be executable Python code starting with imports

Violation of these rules causes system failure."""


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment")
    return Groq(api_key=api_key)


def generate_tests(code: str, model: str = "llama-3.3-70b-versatile") -> str:
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Generate unit tests for this function:\n\n{code}"}
        ],
        temperature=0,
        max_tokens=2000
    )

    return response.choices[0].message.content