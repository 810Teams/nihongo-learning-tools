"""
    `storage.py`
"""

from datetime import datetime

import numpy
import pandas

import os


class Storage:
    def __init__(self, name):
        self.name = name
        self.data = None


    def append(self, new_data) -> None:
        """ User Method: Append Data """
        time = str(datetime.now())
        row = pandas.DataFrame([[time[0:len(time)-7]] + new_data], columns=list(self.data.columns))
        self.data = self.data.append(row)


    def load(self) -> None:
        """ Indirect User Method: Load Storage """
        self.data = pandas.read_csv('data/' + self.name + '.csv')


    def reload(self) -> None:
        """ Indirect User Method: Reload Storage """
        try:
            self.data = pandas.read_csv('data/' + self.name + '.csv')
        except FileNotFoundError:
            self.load()


    def save(self) -> None:
        """ User Method: Save Storage """
        try:
            os.remove(self.name + '.csv')
        except FileNotFoundError:
            pass

        self.data.to_csv('data/' + self.name + '.csv', index=None, header=True)
        self.reload()


    def setup(self, columns) -> pandas.DataFrame:
        """ System Method: View Storage """
        self.data = pandas.DataFrame([], columns=['timestamp'] + columns)


    def try_load(self) -> bool:
        """ System Method: Try loading a storage """
        try:
            if self.data == None:
                pandas.read_csv('data/' + self.name + '.csv')
            return True
        except FileNotFoundError:
            return False


    def to_list(self) -> list:
        """ System Method: Returns a list of storage data """
        return numpy.array(self.data).tolist()


    def get_columns(self) -> list:
        """ System Method: Returns a list of columns """
        return self.data.columns[1:]
