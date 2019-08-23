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

    def append(self, data):
        ''' User Method: Append Data '''
        time = str(datetime.now())
        self.storage = self.storage.append(pandas.DataFrame([[time[0:len(time)-7]] + data], columns=list(self.storage.columns)))

    def delete(self):
        ''' User Method: Delete Storage '''
        notice('Delete this storage? This cannot be undone.')
        response = input('(Y/N) ').strip().upper()

        while (response not in ['Y', 'N']):
            if response == 'Y':
                os.remove(self.name + '.csv')
            elif response == 'N':
                pass
            else:
                error('Invalid choice. Please input again.')
                response = input('(Y/N) ')

    def load(self):
        ''' Indirect User Method: Load Storage '''
        try:
            self.storage = pandas.read_csv(self.name + '.csv')
            notice('Storage \'{}\' loaded.'.format(self.name))
        except FileNotFoundError:
            notice('Storage \'{}\' does not exist. Proceeding to storage set up.'.format(self.name))
            notice('Please input names of columns, separate values using commas.')
            Storage.setup(self, [i.strip() for i in input('(Input) ').split(',')])

    def save(self):
        ''' User Method: Save Storage '''
        try:
            os.remove(self.name + '.csv')
        except FileNotFoundError:
            pass
        self.storage.to_csv(self.name + '.csv', index=None, header=True)
    
    def setup(self, columns):
        ''' System Method: View Storage '''
        try:
            self.storage = pandas.DataFrame([], columns=['timestamp'] + columns)
        except:
            error('Something unexpected happened. Please try again.')

    def view(self):
        ''' User Method: View Storage '''
        print(self.storage)
