"""
    `core/util/validation.py`
"""

def is_valid_style(style_name: str) -> bool:
    """ Function: Verify if chart style is valid """
    try:
        exec('from pygal.style import {}'.format(style_name))
        return True
    except (NameError, SyntaxError, ImportError):
        return False
