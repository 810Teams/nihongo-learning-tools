"""
    `src/util/string.py`
"""


def compare_ignore_case(string_a: str, string_b: str) -> bool:
    """ Function: Compare 2 strings ignoring case """
    return string_a.lower() == string_b.lower()
