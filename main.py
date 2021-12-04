"""
    `main.py`
"""

from src.core.app_data import APP_NAME, AUTHOR, OPERATION_LIST, VERSION
from src.model.storage import Storage
from src.service.operation_service import OperationService
from src.util.logging import error, notice
from src.util.reader import extract_command_and_arguments
from settings import DEFAULT_STORAGE

import sys


class ProgressTrackerApplication:
    def __init__(self) -> None:
        self.operation_service = OperationService(None)

    def run(self) -> None:
        """ Main Function """
        print()
        print('- {} -'.format(APP_NAME))
        print(('by {} ({})'.format(AUTHOR, VERSION)).center(len(APP_NAME)))

        if isinstance(DEFAULT_STORAGE, str):
            storage = Storage(DEFAULT_STORAGE)
        else:
            print()
            notice('Please Input Storage Name')
            print()
            storage = Storage(input('(Input) ').strip())

        if storage.try_load():
            print()
            notice('Default storage is set, proceeding to storage loading.')
            notice('Storage \'{}\' is loaded.'.format(storage.name))
        storage.load()

        print()
        for operation in OPERATION_LIST:
            print(operation)

        self.operation_service.storage = storage
        self.operation_service.render_service.storage = storage
        self.start()

    def start(self) -> None:
        """ Function: Start operating application """
        while True:
            try:
                print()
                line = input('(Command) ')

                if line.strip() == str():
                    continue

                self.operation_service.execute(extract_command_and_arguments(line))
            except IndexError:
                error('Invalid action format. Please try again.')


def main() -> None:
    application = ProgressTrackerApplication()
    application.run()


main()
