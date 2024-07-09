"""
    `progress_tracker/util/transform.py`
"""

from typing import Any


def transpose(data: list[list[Any]]) -> list[list[Any]]:
    """ Function: Returns a transposed of nested list """
    return [
        [data[i][j] for i in range(len(data))] for j in range(len(data[0]))
    ]
