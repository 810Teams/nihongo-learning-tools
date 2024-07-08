"""
    `progress_tracker/app/progress_tracker_app.py`
"""

import sys

from core.base.app_base import ApplicationBase
from core.util.logging import notice
from progress_tracker.constant.app_data import *
from progress_tracker.model.storage import Storage
from progress_tracker.service.operation_service import OperationService
from progress_tracker.settings import DEFAULT_STORAGE


class ProgressTrackerApplication(ApplicationBase):
    def __init__(self):
        super().__init__()

    def setup(self) -> None:
        """ Method: Verify required folder paths and set up folders if not exist """
        super().setup(folder_path_list=[CHART_BASE_PATH, STORAGE_BASE_PATH])

    def start(self) -> None:
        """ Method: Run the application """
        # Title
        super()._display_app_title(APP_NAME, AUTHOR, VERSION)

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
        self.operation_service = OperationService(storage)
        self.operation_service.backup_service.validate_backup_path()
        return super().start()
