"""
    `src/util/reader.py`
"""


from src.model.argument import Argument
from src.model.command import Command


def extract_command_and_arguments(line: str) -> Command:
    line_parts = line.split(' ')

    command = Command(line_parts[0], argument_list=list())

    i = 1
    arg_found = False
    while i < len(line_parts):
        # Argument spotted
        if line_parts[i][0] == '-' and line_parts[i][1].isalpha():
            command.argument_list.append(Argument(line_parts[i]))
            arg_found = True

        # Previous item was argument, indicates that this is the value of the most recent argument
        elif arg_found:
            command.argument_list[-1].value = line_parts[i]
            arg_found = False

        # Value of the command itself
        else:
            command.value = line_parts[i]

        i += 1

    return command
