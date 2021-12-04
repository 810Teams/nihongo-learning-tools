"""
    `src/util/transform.py`
"""

import numpy


def transpose(data: list):
    """ Function: Returns a transposed of nested list """
    return [
        [data[i][j] for i in range(len(data))] for j in range(len(data[0]))
    ]
    