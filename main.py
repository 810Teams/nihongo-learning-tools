"""
    `main.py`
"""

from src.core.app_data import APP_NAME, AUTHOR, OPERATION_LIST, VERSION, CHART_BASE_PATH, STORAGE_BASE_PATH
from src.model.command import Command
from src.model.storage import Storage
from src.service.operation_service import OperationService
from src.util.logging import notice
from src.util.reader import extract_command_and_arguments, is_modification_argument, is_value_parsing_argument
from settings import DEFAULT_STORAGE

import os
import sys


class ProgressTrackerApplication:
    def __init__(self) -> None:
        self.operation_service: OperationService = None

    def run(self) -> None:
        """ Method: Run the application """
        # Title
        print()
        print('- {} -'.format(APP_NAME))
        print(('by {} ({})'.format(AUTHOR, VERSION)).center(len(APP_NAME)))

        # Storage naming
        if len(sys.argv) > 1:
            storage = Storage(sys.argv[1])
        elif isinstance(DEFAULT_STORAGE, str):
            storage = Storage(DEFAULT_STORAGE)
        else:
            print()
            notice('Please input the name of the storage.')
            print()
            storage = Storage(input('(Input) ').strip())
            print()

        # Storage loading
        if storage.try_load():
            notice('Storage \'{}\' already exists, proceeding to storage loading.'.format(storage.name), start='\n')
        else:
            notice('Storage \'{}\' does not exist yet and requires set-up.'.format(storage.name), start='\n')
            notice('Please input the columns of the storage.')
            print()
            columns: list = input('(Input) ').strip().replace(' ', str()).split(',')
            print()
            storage.setup(columns)

        storage.load()
        notice('Storage \'{}\' is loaded.'.format(storage.name))

        # Start
        print()
        for operation in OPERATION_LIST:
            print(operation)

        self.operation_service = OperationService(storage)
        self.start()

    def start(self) -> None:
        """ Method: Start operating the application """
        while True:
            print()
            line = input('(Command) ')

            if line.strip() == str():
                continue

            self.display_command_warnings(line)
            self.operation_service.execute(extract_command_and_arguments(line))

    def display_command_warnings(self, line: str) -> None:
        """ Method: Display command warnings before the command execution """
        warning_segments: Command = extract_command_and_arguments(line, get_warning=True)
        if len(warning_segments) > 0:
            print()
        for warning in warning_segments:
            if is_value_parsing_argument(warning):
                notice('Argument \'{}\' as well as its value is not recognized by the program.'.format(warning))
            elif is_modification_argument(warning):
                notice('Argument \'{}\' is not recognized by the program.'.format(warning))
            else:
                notice('Command segment \'{}\' is not recognized by the program.'.format(warning))
        if len(warning_segments) > 0:
            notice('Note that unrecognized command segments will not take effect.', end=str())

    def setup(self, folder_path_list: list=[]) -> None:
        """ Method: Verify required folder paths and set up folders if not exist """
        folder_path: str
        for folder_path in folder_path_list:
            try:
                os.mkdir(folder_path)
            except FileExistsError:
                pass


def main() -> None:
    """ Main function """
    application = ProgressTrackerApplication()
    application.setup([CHART_BASE_PATH, STORAGE_BASE_PATH])
    application.run()


main()
