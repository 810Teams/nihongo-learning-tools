"""
    `core/src/util/statistics.py`
"""

from math import sqrt


def average(data: list) -> float:
    """ Function: Returns average value of the list """
    return sum(data) / len(data)


def median(data: list) -> float:
    """ Function: Returns median of the list """
    data_copy: list = sorted([i for i in data])
    length: int = len(data)

    if length % 2 == 0:
        return (data_copy[length // 2 - 1] + data_copy[length // 2]) / 2
    return data_copy[length // 2]


def standard_dev(data: list) -> float:
    """ Function: Returns standard deviation of the list """
    return sqrt(sum([(i - average(data)) ** 2 for i in data]) / len(data))
