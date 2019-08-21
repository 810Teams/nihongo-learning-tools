"""
    `storage.py`
    @author 810Teams
"""

from datetime import datetime
import os
import pandas

class Storage:
    def __init__(self, name):
        self.name = name
        self.storage = None

    def save(self):
        try:
            os.remove(self.name + '.csv')
        except FileNotFoundError:
            pass
        self.storage.to_csv(self.name + '.csv', index=None, header=True)
    
    def add(self, data):
        self.storage = self.storage.append(pandas.DataFrame([[str(datetime.now())] + data], columns=list(self.storage.columns)))
    
    def new(self, columns):
        self.storage = pandas.DataFrame([], columns=['timestamp'] + columns)

    def load(self):
        try:
            self.storage = pandas.read_csv(self.name + '.csv')
        except FileNotFoundError:
            print('[ERROR] File \'{}.csv\' not found. Please create the file before loading.'.format(self.name))
    
    def view(self):
        print(self.storage)
