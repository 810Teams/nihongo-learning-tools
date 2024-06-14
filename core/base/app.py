"""
    `core/base/app.py`
"""

import os

from core.base.operation_service_base import OperationServiceBase


class ApplicationBase:
    def __init__(self, operation_service: OperationServiceBase) -> None:
        self.operation_service: OperationServiceBase = operation_service

    def setup(self, folder_path_list: list=[]):
        """ Method: Verify required folder paths and set up folders if not exist """
        folder_path: str
        for folder_path in folder_path_list:
            try:
                os.mkdir(folder_path)
            except FileExistsError:
                pass

    def display_app_title(self, app_name: str, author: str, version: str):
        # Title
        print()
        print('- {} -'.format(app_name))
        print(('by {} ({})'.format(author, version)).center(len(app_name)))

    def _start(self) -> None:
        """ Method: Start operating the application """
        while True:
            print()
            line = input('(Command) ')

            if line.strip() == str():
                continue

            self.operation_service.execute(line)
