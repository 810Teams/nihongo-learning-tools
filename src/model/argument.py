"""
    `src/model/argument.py`
"""


class Argument:
    def __init__(self, name: str, value: type=None):
        self.name: str = name
        self.value: type = value

    def __str__(self) -> str:
        if self.value is None:
            return '{}'.format(self.name)
        return '{}: {}'.format(self.name, self.value)
        