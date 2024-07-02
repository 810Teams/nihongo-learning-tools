"""
    `core/util/opener.py`
"""

import os

from core.util.logging import error


def open_file(path: str, display_error: bool=True):
    """ Function: Open file on system in a supported application """
    try:
        os.system('open {}'.format(path))
    except FileNotFoundError:
        error('File not found error, please try again.', display=display_error)
    except (OSError, PermissionError):
        error('Something unexpected happened, please try again.', display=display_error)
