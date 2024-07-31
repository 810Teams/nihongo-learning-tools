"""
    `base/service/operation_service_base.py`
"""

import os

from core.constant.identifier import *
from core.model.argument import Argument
from core.model.command import Command
from core.model.operation import Operation
from core.model.parameter import Parameter
from core.util.logging import error, notice
from settings import ENABLE_PYCLEAN


class OperationServiceBase:
    def __init__(self, operation_list: list=[]) -> None:
        self.operation_list: list[Operation] = operation_list

    def display_operation_list(self) -> None:
        """ Method: Display operation list """
        title: str = '|  Operation List  |'
        top_frame: str = '┌' + (len(title) - 2) * '-' + '┐'
        bottom_frame: str = '└' + (len(title) - 2) * '-' + '┘'

        print()
        print(top_frame)
        print(title)
        print(bottom_frame)

        print()
        for operation in self.operation_list:
            print(operation)

    def execute(self, line: str) -> None:
        """ Method: Validate and execute command """
        command: Command = self._extract_command_and_arguments(line)
        self._display_command_warnings(line)

        print()
        if not self._operation_exists(command, self.operation_list):
            error('Command \'{}\' error.'.format(command.name))
            error('Please check if the command exists.')
        elif not self._validate_command(command):
            error('Command \'{}\' error.'.format(command.name))
            error('Please check value types of the command as well as its arguments.')
        else:
            return eval('self._operate_{}(command)'.format(command.name))

    def _operate_help(self, command: Command) -> None:
        """ Operation: Display operation list """
        self.display_operation_list()

    def _operate_switch(self, command: Command) -> int:
        """ Operation: Switch application """
        notice('Switching application.')
        return APPLICATION_SWITCH_SIGNAL

    def _operate_exit(self, command: Command) -> None:
        """ Operation: Exit """
        notice('Exitting application.')
        if ENABLE_PYCLEAN:
            print()
            os.system('pyclean .')
        print()
        exit()

    def _open_file(self, path: str, display_error: bool=True) -> None:
        """ Function: Open file on system in a supported application """
        try:
            os.system('open {}'.format(path))
        except FileNotFoundError:
            error('File not found error, please try again.', display=display_error)
        except (OSError, PermissionError):
            error('Unexpected error, please try again.', display=display_error)

    def _extract_command_and_arguments(self, line: str, get_warning: bool=False) -> Command:
        """ Method: Convert a line of string to command object """
        line_parts: list = line.strip().split(' ')

        command: Command = Command(line_parts[0], argument_list=list())
        warning_segments: list = list()

        arg_found: bool = False
        warning_arg_found: bool = False

        for i in range(1, len(line_parts)):
            # Value-parsing argument spotted
            if self._is_value_parsing_argument(line_parts[i]):
                arg_found = True

                if not self._find_operation(command, self.operation_list).contains_parameter(line_parts[i]):
                    warning_segments.append(line_parts[i])
                    warning_arg_found = True
                else:
                    command.argument_list.append(Argument(line_parts[i]))


            # Modification argument spotted
            elif self._is_modification_argument(line_parts[i]):
                arg_found = False

                if not self._find_operation(command, self.operation_list).contains_parameter(line_parts[i]):
                    warning_segments.append(line_parts[i])
                    warning_arg_found = True
                else:
                    command.argument_list.append(Argument(line_parts[i]))

            # Previous item was argument, indicates that this is the value of the most recent argument
            elif arg_found:
                arg_found = False

                if warning_arg_found:
                    warning_arg_found = False
                else:
                    command.argument_list[-1].value = line_parts[i]

            # Value of the command itself
            elif command.value is None:
                arg_found = False
                command.value = line_parts[i]

            # Incorrect segment found
            else:
                warning_segments.append(line_parts[i])

        if get_warning:
            return warning_segments
        return command

    def _display_command_warnings(self, line: str) -> None:
        """ Method: Display command warnings before the command execution """
        warning_segments: list = self._extract_command_and_arguments(line, get_warning=True)

        if len(warning_segments) == 0:
            return

        print()
        for warning in warning_segments:
            if self._is_value_parsing_argument(warning):
                notice('Argument \'{}\' as well as its value is not recognized by the program.'.format(warning))
            elif self._is_modification_argument(warning):
                notice('Argument \'{}\' is not recognized by the program.'.format(warning))
            else:
                notice('Command segment \'{}\' is not recognized by the program.'.format(warning))
        notice('Note that unrecognized command segments will not take effect.', end=str())

    def _find_operation(self, command: Command, operation_list: list[Operation]) -> Operation | None:
        """ Method: Get defined operation object """
        operation: Operation
        for operation in operation_list:
            if operation.name == command.name:
                return operation
        return None

    def _operation_exists(self, command: Command, operation_list: list[Operation]) -> bool:
        """ Method: Verify opertion existence """
        return self._find_operation(command, operation_list) is not None

    def _validate_command(self, command: Command) -> bool:
        """ Method: Validate command """
        operation: Operation = self._find_operation(command, self.operation_list)

        if operation is None:
            return False

        return operation.validate_command(command)

    def _is_value_parsing_argument(self, line_part: str) -> bool:
        """ Method: Verify if value parsing argument type """
        length: int = len(VALUE_PARSING_ARGUMENT_IDENTIFIER)
        return len(line_part) > length and line_part[:length] == VALUE_PARSING_ARGUMENT_IDENTIFIER and line_part[length].isalpha()

    def _is_modification_argument(self, line_part: str) -> bool:
        """ Method: Verify if modification argument type """
        length: int = len(MODIFICATION_ARGUMENT_IDENTIFIER)
        return len(line_part) > length and line_part[:length] == MODIFICATION_ARGUMENT_IDENTIFIER and line_part[length].isalpha()

    def _get_argument_value(self, command: Command, parameter: Parameter) -> any:
        """ Method: Decide argument value based on argument in command and default value """
        if command.contains_argument(parameter.name):
            return parameter.value_type(command.get_argument(parameter.name).value)

        for operation in self.operation_list:
            if command.name == operation.name:
                for p in operation.parameter_list:
                    if parameter.name == p.name:
                        return p.default_value
