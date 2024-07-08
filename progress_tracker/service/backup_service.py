"""
    `progress_tracker/service/backup_service.py`
"""

import os
import shutil

from datetime import date

from core.util.format import path
from core.util.logging import error, notice
from progress_tracker.constant.app_data import STORAGE_BASE_PATH,STORAGE_FILE_EXTENSION
from progress_tracker.model.storage import Storage
from progress_tracker.settings import BACKUP_PATH_LIST, BACKUP_TO_ONLY_FIRST_PATH, ENABLE_BACKUP, LOAD_BACKUP_PATH_LIST


class BackupService:
    def __init__(self, storage: Storage) -> None:
        self.storage: Storage = storage

    def backup(self) -> None:
        """ Method: Copy storage file and save at designated path as backup """
        if ENABLE_BACKUP:
            self._do_backup()

    def load_backup(self) -> None:
        """ Method: Load backup from designated path to storage folder """
        # Step 1: Get valid load backup path
        load_backup_path: str = None
        backup_file_name_list: list[str] = None

        for p in LOAD_BACKUP_PATH_LIST:
            if os.path.exists(path(p)):
                load_backup_path = path(p)
                backup_file_name_list = os.listdir(load_backup_path)
                break

        if load_backup_path is None:
            error('Load backup path error. Please verify load backup path in `settings.py`.')
            return

        # Step 2: Check backup file existence
        backup_file_name_list = [file for file in backup_file_name_list if file[:len(self.storage.name)] == self.storage.name and file[-len(STORAGE_FILE_EXTENSION):] == STORAGE_FILE_EXTENSION]
        if len(backup_file_name_list) == 0:
            error('Loading backup file error. No backup file is found.')
            return

        # Step 3: In case of overriding existing storage, copy as another backup, then copy backup file to storage folder
        try:
            shutil.copy2(
                path(STORAGE_BASE_PATH, self._get_storage_file_name()),
                path(STORAGE_BASE_PATH, self._get_storage_file_name('old'))
            )
        except FileNotFoundError:
            error('Storage file copy error. Aborting storage backup loading process.')
            return

        # Step 4: Copy backup file to storage folder
        backup_file_name = sorted(backup_file_name_list)[-1]
        try:
            shutil.copy2(
                path(load_backup_path, backup_file_name),
                path(STORAGE_BASE_PATH, self._get_storage_file_name())
            )
        except FileNotFoundError:
            os.remove(path(STORAGE_BASE_PATH, self._get_storage_file_name('old')))
            return

        notice('Storage {} has been overridden by backup loading.'.format(self.storage.name))
        notice('In case of mistake, the overridden storage file can be recovered in `{}`.'.format(STORAGE_BASE_PATH))

    def validate_backup_path(self) -> None:
        """ Method: Validate backup path """
        if not ENABLE_BACKUP:
            notice('Backup is disabled. This can be enabled in `settings.py`.')
            return

        valid_backup_path_list = list()
        error_backup_path_list = list()

        for p in BACKUP_PATH_LIST:
            if os.path.exists(path(p)):
                valid_backup_path_list.append(path(p))
                if BACKUP_TO_ONLY_FIRST_PATH:
                    notice('Backup to only first path is set.')
                    notice('Backup path is set to `{}`.'.format(path(p)))
                    return
            else:
                error_backup_path_list.append(path(p))

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
        for p in BACKUP_PATH_LIST:
            try:
                shutil.copy2(
                    path(STORAGE_BASE_PATH, self._get_storage_file_name()),
                    path(p, self._get_storage_file_name(date.today().__str__()))
                )
                if BACKUP_TO_ONLY_FIRST_PATH:
                    break
            except FileNotFoundError:
                pass

    def _list_path(self, path_list: list[str]) -> None:
        for p in path_list:
            print('    - {}'.format(path(p)))

    def _get_storage_file_name(self, suffix: str=str()) -> str:
        if suffix.strip() != str():
            return self.storage.name + '_' + suffix + STORAGE_FILE_EXTENSION
        return self.storage.name + STORAGE_FILE_EXTENSION
