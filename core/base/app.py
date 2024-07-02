"""
    `core/base/app.py`
"""

import os

from core.base.operation_service_base import OperationServiceBase


class ApplicationBase:
    def __init__(self) -> None:
        self.operation_service: OperationServiceBase = None

    def setup(self, folder_path_list: list[str]=[]):
        """ Method: Verify required folder paths and set up folders if not exist """
        folder_path: str
        for folder_path in folder_path_list:
            try:
                os.mkdir(folder_path)
            except FileExistsError:
                pass

    def _display_app_title(self, app_name: str, author: str, version: str):
        """ Method: Display application title """
        title: str = '┌-- {} --┐'.format(app_name)
        subtitle: str = '|' + 'by {} ({})'.format(author, version).center(len(title) - 2) + '|'
        footer: str = '└' + (len(title) - 2) * '-' + '┘'
        print()
        print(title)
        print(subtitle)
        print(footer)

    def _start(self) -> None:
        """ Method: Start operating the application """
        print()
        self.operation_service.display_operation_list()

        while True:
            print()
            line = input('(Command) ')

            if line.strip() == str():
                continue

            self.operation_service.execute(line)
