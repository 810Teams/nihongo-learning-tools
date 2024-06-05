"""
    `src/service/backup_service.py`
"""

from datetime import date
from settings import BACKUP_PATH, ENABLE_BACKUP
from src.core.app_data import STORAGE_BASE_PATH, STORAGE_FILE_EXTENSION

import shutil


class BackupService:
    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name

    def trigger_backup(self) -> None:
        """ Method: Trigger backup process """
        if ENABLE_BACKUP:
            self.copy()

    def copy(self) -> None:
        """ Method: Copy data and save elsewhere as backup """
        shutil.copy2(
            '{}'.format(
                STORAGE_BASE_PATH + self.storage_name + STORAGE_FILE_EXTENSION
            ),
            '{}/{}'.format(
                BACKUP_PATH.rstrip('/').rstrip('\\'),
                self.storage_name + '_' + date.today().__str__() + STORAGE_FILE_EXTENSION
            )
        )
