"""
    `nihongo_flashcard_visualizer/util/format.py`
"""

from math import floor


def level_format(level_value: float, initial_level: int=1, remainder: bool=False) -> str:
    """ Function: Get a level format from a level value """
    return '{:.0f}-{:.0f}'.format(
        initial_level + level_value // 3,
        floor(level_value % 3)
    ) + ' (+{:.2f})'.format(level_value % 1) * remainder
