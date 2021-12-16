"""
    `src/service/backup_service.py`
"""

from settings import BACKUP_PATH, ENABLE_BACKUP
from datetime import date

import shutil


class BackupService:
    def __init__(self, storage_name: str) -> None:
        self.storage_name = storage_name


    def trigger_backup(self) -> None:
        if ENABLE_BACKUP:
            self.copy()


    def copy(self) -> None:
        shutil.copy2(
            'data/{}'.format(
                self.storage_name + '.csv'
            ),
            '{}/{}'.format(
                BACKUP_PATH.rstrip('/').rstrip('\\'),
                self.storage_name + '_' + date.today().__str__() + '.csv'
            )
        )
