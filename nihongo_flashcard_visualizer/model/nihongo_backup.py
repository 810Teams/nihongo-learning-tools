"""
    `nihongo_flashcard_visualizer/model/nihongo_backup.py`
"""

import os
import sqlite3

from core.util.format import path
from core.util.logging import error, notice
from nihongo_flashcard_visualizer.constant.app_data import *
from nihongo_flashcard_visualizer.constant.flashcard_type import FlashcardType
from nihongo_flashcard_visualizer.constant.nihongo_backup_constant import NihongoBackupConstant
from nihongo_flashcard_visualizer.settings import *
from sqlite3 import Connection, Cursor


class NihongoBackup:
    def __init__(self) -> None:
        self.connection: Connection = None

    def extract(self) -> None:
        """ Function: Extracts database file from the zip """
        if isinstance(NIHONGO_BACKUP_PATH, str) and NIHONGO_BACKUP_PATH.strip() != str():
            nihongo_path = path(NIHONGO_BACKUP_PATH, DATABASE_CONTAINER_NAME, DATABASE_FILE_NAME + ZIP_FILE_EXTENSION)
        else:
            nihongo_path = path(APPLICATION_DIRECTORY, DATABASE_CONTAINER_NAME, DATABASE_FILE_NAME + ZIP_FILE_EXTENSION)

        if os.path.exists(nihongo_path):
            os.system('unzip -o "{}" -d "{}"'.format(nihongo_path, path(DATABASE_BASE_PATH)))
        elif os.path.exists(NIHONGO_BACKUP_PATH):
            error('Extraction error. Nihongo backup file not found.')
        else:
            error('Extraction error. Please verify Nihongo backup path in `settings.py`.')

    def create_connection(self) -> None:
        """ Function: Creates the database connection """
        try:
            self.connection = sqlite3.connect('{}'.format(path(DATABASE_BASE_PATH, DATABASE_FILE_NAME)))
        except sqlite3.OperationalError:
            error('Please extract SQLite file before proceeding.')

    def _get_progress(self) -> dict[str, list[int]]:
        """ Function: Gets flashcard progress from database """
        if self.connection is None:
            self.create_connection()

        cursor: Cursor = self.connection.cursor()
        cursor.execute('SELECT {}, {}, {} FROM {}'.format(
            NihongoBackupConstant.Columns.PROGRESS,
            NihongoBackupConstant.Columns.STATUS,
            NihongoBackupConstant.Columns.KANJI_TEXT,
            NihongoBackupConstant.TABLE_NAME
        ))

        data: list[list[any]] = cursor.fetchall()
        return {
            FlashcardType.WORD: [i[0] for i in data if bool(i[1]) and i[2] == None],
            FlashcardType.KANJI: [i[0] for i in data if bool(i[1]) and i[2] != None],
            FlashcardType.ANY: [i[0] for i in data if bool(i[1])]
        }

    def get_uncounted_flashcard_process(self) -> dict[str, list[int]]:
        """ Function: Get uncounted flashcard process data """
        try:
            self._get_progress()
        except sqlite3.OperationalError:
            error('SQLite file not found. Beginning the extraction.')
            print()
            self.extract()
            print()

        return self._get_progress()

    def get_counted_flashcard_progress(self) -> dict:
        """ Function: Get counted flashcard progress data """
        uncounted_data: dict[str, list[int]] = self.get_uncounted_flashcard_process()
        counted_data: dict[str, list[int]] = dict()

        for flashcard_type in uncounted_data:
            counted_data[flashcard_type] = [uncounted_data[flashcard_type].count(j) for j in range(0, 13)]

        return counted_data
