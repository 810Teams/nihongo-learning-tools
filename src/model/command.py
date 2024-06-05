"""
    `src/model/command.py`
"""

from src.model.argument import Argument
from src.util.string import compare_ignore_case


class Command:
    def __init__(self, name: str, value: any=None, argument_list: list=list()):
        self.name: str = name
        self.value: any = value
        self.argument_list: list = argument_list

    def __str__(self) -> str:
        if self.value is None:
            return '{}, [{}]'.format(self.name, self.argument_list)
        return '{}: {}, [{}]'.format(self.name, self.value, self.argument_list)

    def get_argument(self, argument_name: str) -> Argument:
        """ Method: Get argument object """
        for i in self.argument_list:
            if isinstance(i, Argument) and compare_ignore_case(argument_name, i.name):
                return i
        return None

    def contains_argument(self, argument_name: str) -> bool:
        """ Method: Check if contains specified argument """
        return self.get_argument(argument_name) is not None
