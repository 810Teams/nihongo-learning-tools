"""
    `nihongo_flashcard_visualizer/model/nihongo_backup.py`
"""

import os
import sqlite3

from core.error.invalid_settings_error import InvalidSettingsError
from core.util.format import path
from core.util.logging import error, notice
from nihongo_flashcard_visualizer.constant.app_data import *
from nihongo_flashcard_visualizer.constant.flashcard_type import FlashcardType
from nihongo_flashcard_visualizer.constant.nihongo_backup_constant import NihongoBackupConstant
from nihongo_flashcard_visualizer.settings import *
from sqlite3 import Connection, Cursor
from typing import Any


class NihongoBackup:
    def __init__(self) -> None:
        self.connection: Connection = None

    def extract(self) -> None:
        """ Function: Extracts database file from the zip """
        if isinstance(NIHONGO_BACKUP_PATH, str) and NIHONGO_BACKUP_PATH.strip() != str():
            nihongo_backup_path = path(NIHONGO_BACKUP_PATH)
            if not os.path.exists(nihongo_backup_path):
                raise InvalidSettingsError
        else:
            nihongo_backup_path = path(APPLICATION_DIRECTORY)

        nihongo_sqlite_zip_path = path(nihongo_backup_path, DATABASE_CONTAINER_NAME, DATABASE_FILE_NAME + ZIP_FILE_EXTENSION)

        if not os.path.exists(nihongo_sqlite_zip_path):
            raise FileNotFoundError

        os.system('unzip -o "{}" -d "{}"'.format(nihongo_sqlite_zip_path, path(DATABASE_BASE_PATH)))

    def get_flashcard_progress(self) -> dict[str, list[int]]:
        """ Function: Gets uncounted flashcard progress data """
        if self.connection is None or not isinstance(self.connection, Connection):
            if os.path.exists(path(DATABASE_BASE_PATH, DATABASE_FILE_NAME)):
                self.connection = sqlite3.connect(path(DATABASE_BASE_PATH, DATABASE_FILE_NAME))
            else:
                raise FileNotFoundError

        cursor: Cursor = self.connection.cursor()
        cursor.execute('SELECT {}, {}, {} FROM {}'.format(
            NihongoBackupConstant.Columns.PROGRESS,
            NihongoBackupConstant.Columns.STATUS,
            NihongoBackupConstant.Columns.KANJI_TEXT,
            NihongoBackupConstant.TABLE_NAME
        )) # May raise sqlite3.OperationalError if SQLite file exists

        data: list[list[Any]] = cursor.fetchall()

        return {
            FlashcardType.WORD: [i[0] for i in data if bool(i[1]) and i[2] == None],
            FlashcardType.KANJI: [i[0] for i in data if bool(i[1]) and i[2] != None],
            FlashcardType.ANY: [i[0] for i in data if bool(i[1])]
        }

    def get_counted_flashcard_progress(self) -> dict[str, list[int]]:
        """ Function: Get counted flashcard progress data """
        uncounted_data: dict[str, list[int]] = self.get_flashcard_progress()
        counted_data: dict[str, list[int]] = dict()

        for flashcard_type in uncounted_data:
            counted_data[flashcard_type] = [uncounted_data[flashcard_type].count(j) for j in range(0, 13)]

        return counted_data
