'''
    `storage.py`
    @author 810Teams
'''

from datetime import datetime
from lib.utils import error, notice
import os
import pandas


class Storage:
    def __init__(self, name):
        self.name = name
        self.storage = None

    def append(self, data, show_notice=True):
        ''' User Method: Append Data '''
        time = str(datetime.now())
        self.storage = self.storage.append(pandas.DataFrame(
            [[time[0:len(time)-7]] + data], columns=list(self.storage.columns)))

        if show_notice:
            notice('Data {} has been added to the storage.'.format(data))

    def load(self, show_notice=True):
        ''' Indirect User Method: Load Storage '''
        try:
            self.storage = pandas.read_csv('data/' + self.name + '.csv')
        except FileNotFoundError:
            if show_notice:
                notice('Storage \'{}\' does not exist. Proceeding to storage set up.'.format(
                    self.name))
                notice('Please input names of columns, separate values using commas.')
            Storage.setup(self, [i.strip()
                                 for i in input('(Input) ').split(',')])

    def reload(self, show_notice=True):
        ''' Indirect User Method: Reload Storage '''
        try:
            self.storage = pandas.read_csv('data/' + self.name + '.csv')
            if show_notice:
                notice('Storage \'{}\' is reloaded.'.format(self.name))
        except FileNotFoundError:
            self.load()

    def save(self, show_notice=True):
        ''' User Method: Save Storage '''
        try:
            os.remove(self.name + '.csv')
        except FileNotFoundError:
            pass
        self.storage.to_csv('data/' + self.name + '.csv',
                            index=None, header=True)

        if show_notice:
            notice('Storage \'{}\' saved successfully.'.format(self.name))

        self.reload(show_notice=False)

    def setup(self, columns, show_notice=True):
        ''' System Method: View Storage '''
        try:
            self.storage = pandas.DataFrame(
                [], columns=['timestamp'] + columns)
        except:
            if show_notice:
                error('Something unexpected happened. Please try again.')

    def view(self):
        ''' User Method: View Storage '''
        print(self.storage)
