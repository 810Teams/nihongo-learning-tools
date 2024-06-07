"""
    `src/service/backup_service.py`
"""

from datetime import date
from settings import ENABLE_BACKUP, BACKUP_PATH_LIST, BACKUP_TO_ONLY_FIRST_PATH, LOAD_BACKUP_PATH_LIST
from src.core.app_data import STORAGE_BASE_PATH, STORAGE_FILE_EXTENSION
from src.model.storage import Storage
from src.util.logging import error, notice

import os
import shutil


class BackupService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def backup(self) -> None:
        """ Method: Copy storage file and save at designated path as backup """
        if ENABLE_BACKUP:
            self._do_backup()

    def load_backup(self) -> None:
        """ Method: Load backup from designated path to storage folder """
        # Step 1: Get valid load backup path
        load_backup_path: str = None
        for path in LOAD_BACKUP_PATH_LIST:
            if os.path.exists(self._process_path(path)):
                load_backup_path = path
                break

        if load_backup_path is None:
            error('Load backup path error. Please verify load backup path in `settings.py`.')
            return

        # Step 2: Verify load backup path existence
        try:
            backup_file_name_list = os.listdir(self._process_path(load_backup_path))
        except FileExistsError:
            error('Load backup path error. Please verify load backup path in `settings.py`.')
            return

        # Step 3: Check backup file existence
        backup_file_name_list = [file for file in backup_file_name_list if file[:len(self.storage.name)] == self.storage.name and file[-len(STORAGE_FILE_EXTENSION):] == STORAGE_FILE_EXTENSION]
        if len(backup_file_name_list) == 0:
            error('Loading backup file error. No backup file is found.')
            return

        # Step 4: In case of overriding existing storage, copy as another backup
        try:
            shutil.copy2(
                '{}'.format(STORAGE_BASE_PATH + self.storage.name + STORAGE_FILE_EXTENSION),
                '{}'.format(STORAGE_BASE_PATH + self.storage.name + '-old' + STORAGE_FILE_EXTENSION)
            )
            notice('Storage {} has been overridden by backup loading.'.format(self.storage.name))
            notice('In case of mistake, the overridden storage file can be recovered in `{}`.'.format(STORAGE_BASE_PATH))
        except FileNotFoundError:
            pass

        # Step 5: Copy backup file to storage folder
        backup_file_name = sorted(backup_file_name_list)[-1]

        for path in LOAD_BACKUP_PATH_LIST:
            try:
                shutil.copy2(
                    '{}/{}'.format(self._process_path(path), backup_file_name),
                    '{}'.format(STORAGE_BASE_PATH + self.storage.name + STORAGE_FILE_EXTENSION)
                )
                break
            except FileNotFoundError:
                pass

    def validate_backup_path(self) -> None:
        """ Method: Validate backup path """
        valid_backup_path_list = list()
        error_backup_path_list = list()

        for path in BACKUP_PATH_LIST:
            if os.path.exists(self._process_path(path)):
                valid_backup_path_list.append(self._process_path(path))
                if BACKUP_TO_ONLY_FIRST_PATH:
                    notice('Backup to only first path is set.')
                    notice('Backup path is set to `{}`.'.format(self._process_path(path)))
                    return
            else:
                error_backup_path_list.append(self._process_path(path))

        if len(valid_backup_path_list) == BACKUP_PATH_LIST:
            notice('All backup paths are valid.')
            notice('Storage file will be backup to the following paths.')
            self._list_path(valid_backup_path_list)
        elif len(error_backup_path_list) == BACKUP_PATH_LIST:
            error('All backup paths are invalid. Please verify backup path in `settings.py`.')
            self._list_path(error_backup_path_list)
        else:
            error('Invalid backup paths exist as follow. Please verify backup path in `settings.py`.')
            self._list_path(error_backup_path_list)
            notice('Storage file will be backup to the following valid paths.')
            self._list_path(valid_backup_path_list)

    def _do_backup(self) -> None:
        for path in BACKUP_PATH_LIST:
            try:
                shutil.copy2(
                    '{}'.format(STORAGE_BASE_PATH + self.storage.name + STORAGE_FILE_EXTENSION),
                    '{}/{}'.format(self._process_path(path), self.storage.name + '_' + date.today().__str__() + STORAGE_FILE_EXTENSION)
                )
                if BACKUP_TO_ONLY_FIRST_PATH:
                    break
            except FileNotFoundError:
                pass

    def _process_path(self, path: str) -> str:
        return path.rstrip('/').rstrip('\\')

    def _list_path(self, path_list: list) -> None:
        for path in path_list:
            print('    - {}'.format(self._process_path(path)))
