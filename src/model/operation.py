"""
    `src/model/operation.py`
"""

from src.model.command import Command


class Operation:
    def __init__(self, name: str, code: str=None, value_type: type=None, description: str=str(), argument_list: list=list()):
        self.command = name
        self.code = code
        self.value_type = value_type
        self.description = description
        self.argument_list = argument_list

        if self.code is None:
            self.code = name[0]

    def __str__(self) -> str:
        message = '[{}]'.format(self.command)

        if self.value_type is not None:
            message += ' [{}]'.format(self.value_type)

        for i in self.argument_list:
            message += '\n    {}'.format(i)

        return message
