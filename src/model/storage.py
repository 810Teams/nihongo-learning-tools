"""
    `storage.py`
"""

from datetime import datetime
from src.util.logging import error, notice

import numpy
import pandas

import os


class Storage:
    def __init__(self, name):
        self.name = name
        self.data = None

    def append(self, new_data, show_notice=True):
        """ User Method: Append Data """
        time = str(datetime.now())
        self.data = self.data.append(pandas.DataFrame([[time[0:len(time)-7]] + new_data], columns=list(self.data.columns)))

        notice('Data {} has been added to the storage.'.format(new_data), show=show_notice)

    def load(self, show_notice=True, template=None):
        """ Indirect User Method: Load Storage """
        try:
            self.data = pandas.read_csv('data/' + self.name + '.csv')
        except FileNotFoundError:
            notice('Storage \'{}\' does not exist. Proceeding to storage set up.'.format(self.name), show=show_notice)

            if template == 'jlpt':
                notice('Storage \'{}\' has been set up by JLPT template.'.format(self.name), show=show_notice)
                Storage.setup(self, ['N5', 'N4', 'N3', 'N2', 'N1', '-'])
            else:
                notice('Please input names of columns, separate values using commas.', show=show_notice)
                print()
                Storage.setup(self, [i.strip()for i in input('(Input) ').split(',')])

    def reload(self, show_notice=True):
        """ Indirect User Method: Reload Storage """
        try:
            self.data = pandas.read_csv('data/' + self.name + '.csv')
            notice('Storage \'{}\' is reloaded.'.format(self.name), show=show_notice)
        except FileNotFoundError:
            self.load()

    def save(self, show_notice=True):
        """ User Method: Save Storage """
        try:
            os.remove(self.name + '.csv')
        except FileNotFoundError:
            pass
        self.data.to_csv('data/' + self.name + '.csv', index=None, header=True)

        notice('Storage \'{}\' saved successfully.'.format(self.name), show=show_notice)
        self.reload(show_notice=False)

    def view(self):
        """ User Method: View Storage """
        print(self.data)

    def setup(self, columns, show_notice=True):
        """ System Method: View Storage """
        try:
            self.data = pandas.DataFrame([], columns=['timestamp'] + columns)
        except:
            error('Something unexpected happened. Please try again.', show=show_notice)

    def try_load(self):
        """ System Method: Try loading a storage """
        try:
            if self.data == None:
                self.data = pandas.read_csv('data/' + self.name + '.csv')
                self.data = None
            return True
        except FileNotFoundError:
            return False

    def to_list(self):
        """ System Method: Returns a list of storage data """
        return numpy.array(self.data).tolist()
