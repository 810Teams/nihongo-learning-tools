'''
    `storage.py`
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
        self.storage = self.storage.append(pandas.DataFrame([[time[0:len(time)-7]] + data], columns=list(self.storage.columns)))

        notice('Data {} has been added to the storage.'.format(data), show=show_notice)

    def load(self, show_notice=True, template=None):
        ''' Indirect User Method: Load Storage '''
        try:
            self.storage = pandas.read_csv('data/' + self.name + '.csv')
        except FileNotFoundError:
            notice('Storage \'{}\' does not exist. Proceeding to storage set up.'.format(self.name), show=show_notice)

            if template == 'jlpt':
                notice('Storage \'{}\' has been set up by JLPT template.'.format(self.name), show=show_notice)
                Storage.setup(self, ['n5', 'n4', 'n3', 'n2', 'n1', '-'])
            else:
                notice('Please input names of columns, separate values using commas.', show=show_notice)
                Storage.setup(self, [i.strip()for i in input('(Input) ').split(',')])

    def reload(self, show_notice=True):
        ''' Indirect User Method: Reload Storage '''
        try:
            self.storage = pandas.read_csv('data/' + self.name + '.csv')
            notice('Storage \'{}\' is reloaded.'.format(self.name), show=show_notice)
        except FileNotFoundError:
            self.load()

    def save(self, show_notice=True):
        ''' User Method: Save Storage '''
        try:
            os.remove(self.name + '.csv')
        except FileNotFoundError:
            pass
        self.storage.to_csv('data/' + self.name + '.csv', index=None, header=True)

        notice('Storage \'{}\' saved successfully.'.format(self.name), show=show_notice)
        self.reload(show_notice=False)

    def setup(self, columns, show_notice=True):
        ''' System Method: View Storage '''
        try:
            self.storage = pandas.DataFrame([], columns=['timestamp'] + columns)
        except:
            error('Something unexpected happened. Please try again.', show=show_notice)

    def view(self):
        ''' User Method: View Storage '''
        print(self.storage)
