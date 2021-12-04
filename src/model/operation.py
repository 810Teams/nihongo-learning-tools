"""
    `src/model/operation.py`
"""

from src.model.argument import Argument
from src.model.command import Command
from src.model.parameter import Parameter
from src.util.string import compare_ignore_case


class Operation:
    def __init__(self, name: str, code: str=None, value_type: type=None, description: str=str(), parameter_list: list=list()):
        self.name = name
        self.code = code
        self.value_type = value_type
        self.description = description
        self.parameter_list = parameter_list

        if self.code is None:
            self.code = name[0]

    def __str__(self) -> str:
        message = '[{}]'.format(self.name)

        if self.value_type is not None:
            message += ' [{}]'.format(self.value_type)

        for i in self.parameter_list:
            message += '\n    {}'.format(i)

        return message

    def get_parameter(self, parameter_name: str) -> Parameter:
        for i in self.parameter_list:
            if isinstance(i, Parameter) and compare_ignore_case(parameter_name, i.name):
                return i
        return None

    def contains_parameter(self, parameter_name: str) -> bool:
        return self.get_parameter(parameter_name) is not None

    def validate_command(self, command: Command) -> bool:
        if self.name != command.name:
            return False
        if self.value_type is None and command.value is not None:
            return False
        if self.value_type is not None and command.value is not None:
            try:
                self.value_type(command.value)
            except:
                return False

        arg: Argument
        for arg in command.argument_list:
            if self.contains_parameter(arg.name):
                param = self.get_parameter(arg.name)
                if not param.validate_argument(arg):
                    return False

        return True
