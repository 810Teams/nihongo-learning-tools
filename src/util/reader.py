"""
    `src/util/reader.py`
"""

from pygal.style import DefaultStyle, Style
from src.model.operation import Operation
from src.core.app_data import OPERATION_LIST, VALUE_PARSING_ARGUMENT_IDENTIFIER, MODIFICATION_ARGUMENT_IDENTIFIER
from src.model.argument import Argument
from src.model.command import Command


def extract_command_and_arguments(line: str, get_warning: bool=False) -> Command:
    line_parts = line.strip().split(' ')
    line_parts = [part for part in line_parts if part != str()]

    command = Command(line_parts[0], argument_list=list())
    warning_segments = list()

    i = 1
    arg_found = False
    warning_arg_found = False

    while i < len(line_parts):
        # Value-parsing argument spotted
        if is_value_parsing_argument(line_parts[i]):
            arg_found = True

            if not get_operation(command.name).contains_parameter(line_parts[i]):
                warning_segments.append(line_parts[i])
                warning_arg_found = True
            else:
                command.argument_list.append(Argument(line_parts[i]))


        # Modification argument spotted
        elif is_modification_argument(line_parts[i]):
            arg_found = False

            if not get_operation(command.name).contains_parameter(line_parts[i]):
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

        i += 1

    if get_warning:
        return warning_segments
    return command


def is_value_parsing_argument(line_part: str) -> bool:
    return len(line_part) > 1 and line_part[0] == VALUE_PARSING_ARGUMENT_IDENTIFIER and line_part[1].isalpha()


def is_modification_argument(line_part: str) -> bool:
    return len(line_part) > 2 and line_part[0:2] == MODIFICATION_ARGUMENT_IDENTIFIER and line_part[2].isalpha()


def operation_exists(name: str) -> bool:
    for operation in OPERATION_LIST:
        if operation.name == name:
            return True
    return False


def get_operation(name: str) -> Operation:
    for operation in OPERATION_LIST:
        if operation.name == name:
            return operation
    return None


def convert_csv_to_list(value: str, value_type: type=str, replace_null=str()) -> list:
    converted_list = [i.replace(' ', str()) for i in value.split(',')]

    for i in range(len(converted_list)):
        if (converted_list[i] == str()):
            converted_list[i] = replace_null
        else:
            converted_list[i] = value_type(converted_list[i])

    return converted_list


def contains_row_for_date(data: list, date: str) -> bool:
    filtered_data = [i for i in data if i[0] == date]

    return len(filtered_data) > 0


def find_row_by_date(data: list, date: str, use_index: int=-1) -> list:
    filtered_data = [i for i in data if i[0] == date]

    try:
        return filtered_data[use_index]
    except IndexError:
        return None


def is_nan(value) -> bool:
    return value != value


def contains_nan(row: list) -> bool:
    for i in row:
        if is_nan(i):
            return True
    return False


def is_empty(value) -> bool:
    try:
        return value == str() or value is None or is_nan(value)
    except TypeError:
        return True


def copy_list(value: list) -> list:
    return [i for i in value]


def read_style(style_name: str) -> Style:
    try:
        exec('from pygal.style import {}'.format(style_name))
        return eval(style_name)
    except (NameError, SyntaxError, ImportError):
        return DefaultStyle
