"""
    `progress_tracker/model/storage.py`
"""

import os
import numpy
import pandas

from datetime import datetime
from io import TextIOWrapper
from pandas import DataFrame
from typing import Any

from core.util.format import path
from progress_tracker.constant.app_data import STORAGE_BASE_PATH, STORAGE_FILE_EXTENSION
from progress_tracker.constant.storage_constant import StorageConstant
from progress_tracker.util.reader import is_empty


class Storage:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.data: DataFrame = None

    def append(self, new_data: list[Any]) -> None:
        """ User Method: Append data """
        time = str(datetime.now())
        row = pandas.DataFrame([[time[0:len(time) - 7]] + new_data], columns=list(self.data.columns))
        self.data = pandas.concat((self.data, row,))

    def load(self) -> None:
        """ Indirect User Method: Load storage """
        columns = pandas.read_csv(self.get_path()).columns[1:]
        temp_data = pandas.read_csv(self.get_path(), dtype=dict([(col, StorageConstant.Type.STRING) for col in columns]))

        dtype_data = dict()

        for col in columns:
            dtype_data[col] = StorageConstant.Type.INT64
            for item in temp_data[col]:
                if not is_empty(item):
                    try:
                        int(item)
                    except ValueError:
                        dtype_data[col] = StorageConstant.Type.FLOAT64
                        break

        self.data = pandas.read_csv(self.get_path(), dtype=dtype_data)

    def reload(self) -> None:
        """ Indirect User Method: Reload storage """
        self.load()

    def save(self) -> None:
        """ User Method: Save storage """
        try:
            os.remove(self.get_path())
        except FileNotFoundError:
            pass

        self.data.to_csv(self.get_path(), index=None, header=True)
        self.reload()

    def setup(self, columns: list[str]) -> pandas.DataFrame:
        """ System Method: View storage """
        self.data = pandas.DataFrame([], columns=[StorageConstant.Columns.TIMESTAMP] + columns)
        f: TextIOWrapper = open('{}'.format(self.get_path()), 'w')
        f.write(','.join([StorageConstant.Columns.TIMESTAMP] + columns))
        f.close()

    def try_load(self) -> bool:
        """ System Method: Try loading a storage """
        try:
            if self.data == None:
                pandas.read_csv(self.get_path())
            return True
        except FileNotFoundError:
            return False

    def to_list(self) -> list[Any]:
        """ System Method: Returns a list of storage data """
        return numpy.array(self.data).tolist()

    def get_columns(self) -> list[str]:
        """ System Method: Returns a list of columns """
        return self.data.columns[1:]

    def get_path(self) -> str:
        """ System Method: Return storage full path """
        return path(STORAGE_BASE_PATH, self.name + STORAGE_FILE_EXTENSION)
