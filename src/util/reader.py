"""
    `src/util/reader.py`
"""


import pandas
from src.model.argument import Argument
from src.model.command import Command


def extract_command_and_arguments(line: str) -> Command:
    line_parts = line.split(' ')

    command = Command(line_parts[0], argument_list=list())

    i = 1
    arg_found = False
    while i < len(line_parts):
        # Value-parsing argument spotted
        if line_parts[i][0] == '-' and line_parts[i][1].isalpha():
            command.argument_list.append(Argument(line_parts[i]))
            arg_found = True

        # Modification argument spotted
        elif line_parts[i][0:2] == '--' and line_parts[i][2].isalpha():
            command.argument_list.append(Argument(line_parts[i]))
            arg_found = False

        # Previous item was argument, indicates that this is the value of the most recent argument
        elif arg_found:
            command.argument_list[-1].value = line_parts[i]
            arg_found = False

        # Value of the command itself
        elif command.value is None:
            command.value = line_parts[i]
            arg_found = False

        i += 1

    return command


def get_line_warning_segments(line: str) -> list:
    line_parts = line.split(' ')

    warning_segments = list()

    i = 1
    arg_found = False
    command_value_exist = False
    while i < len(line_parts):
        # Value-parsing argument spotted
        if line_parts[i][0] == '-' and line_parts[i][1].isalpha():
            arg_found = True

        # Modification argument spotted
        elif line_parts[i][0:2] == '--' and line_parts[i][2].isalpha():
            arg_found = False

        # Previous item was argument, indicates that this is the value of the most recent argument
        elif arg_found:
            arg_found = False

        # Value of the command itself
        elif not command_value_exist:
            command_value_exist = True
            arg_found = False

        # Incorrect segment found, add segment to warning list
        else:
            warning_segments.append(line_parts[i])

        i += 1

    return warning_segments


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
