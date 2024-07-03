"""
    `core/model/operation.py`
"""

from typing import Callable

from core.model.argument import Argument
from core.model.command import Command
from core.model.parameter import Parameter
from core.util.logging import error
from core.util.string import compare_ignore_case


class Operation:
    def __init__(
            self,
            name: str,
            value_type: type=None,
            default_value: any=None,
            validation: Callable[[any], bool]=lambda x: True,
            error_message: str=str(),
            description: str=str(),
            parameter_list: list[Parameter]=list()
        ):
        self.name: str = name
        self.value_type: type = value_type
        self.default_value: value_type = default_value
        self.validation: Callable[[any], bool] = validation
        self.error_message: str = error_message.strip()
        self.description: str = description
        self.parameter_list: list[Parameter] = parameter_list

    def __str__(self) -> str:
        message = '[{}]'.format(self.name)

        if self.value_type is not None:
            message += ' {}'.format(self.value_type)

        for i in self.parameter_list:
            message += '\n    {}'.format(i)

        return message

    def get_parameter(self, parameter_name: str) -> Parameter:
        """ Method: Get parameter object """
        for i in self.parameter_list:
            if isinstance(i, Parameter) and compare_ignore_case(parameter_name, i.name):
                return i
        return None

    def contains_parameter(self, parameter_name: str) -> bool:
        """ Method: Check if parameter exists """
        return self.get_parameter(parameter_name) is not None

    def validate_command(self, command: Command, display_error: bool=True) -> bool:
        """ Method: Validate command """
        if self.name != command.name:
            error('Command name mismatches operation name.', display=display_error)
            return False
        if self.value_type is None and command.value is not None:
            error('Operation {} does not require value.'.format(self.name), display=display_error)
            return False
        if self.value_type is not None and command.value is None:
            error('Operation {} requires value with type {} but none is found.'.format(self.name, self.value_type), display=display_error)
            return False
        if self.value_type is not None and command.value is not None:
            try:
                self.value_type(command.value)
            except (TypeError, ValueError):
                error('Value of command {} must be type {}.'.format(command.name, self.value_type), display=display_error)
                return False

            if not self.validation(command.value):
                if isinstance(self.error_message, str) and len(self.error_message) > 0:
                    error(self.error_message, display=display_error)
                else:
                    error('Value validation of command {} error.'.format(command.name), display=display_error)
                return False

        arg: Argument
        for arg in command.argument_list:
            if self.contains_parameter(arg.name):
                param: Parameter = self.get_parameter(arg.name)
                if not param.validate_argument(arg, display_error=True):
                    return False

        return True
