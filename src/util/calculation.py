"""
    `src/util/calculation.py`
"""

from datetime import datetime, timedelta


def average(data: list):
    """ Function: Returns average value of the list """
    return sum(data)/len(data)


def add_day_to_date(date_string: str, days: int=1) -> str:
    """ Function: Add days to date """
    date = datetime.strptime(date_string, '%Y-%m-%d')
    added_days = timedelta(days=days)

    return str(date + added_days).split()[0]
