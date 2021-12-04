"""
    `src/util/string.py`
"""


def compare_ignore_case(string_a: str, string_b: str) -> bool:
    return string_a.lower() == string_b.lower()
