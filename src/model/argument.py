"""
    `src/model/argument.py`
"""

from src.model.parameter import Parameter


class Argument:
    def __init__(self, name:str, value=None):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        if self.value is None:
            return '{}'.format(self.name)
        return '{}: {}'.format(self.name, self.value)
        