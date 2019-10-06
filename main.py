'''
    `main.py`
'''

from lib.loaders import load_default_storage
from lib.operations import Operation
from lib.operations import Argument
from lib.operations import operate_a
from lib.operations import operate_c
from lib.operations import operate_h
from lib.operations import operate_r
from lib.operations import operate_s
from lib.operations import operate_v
from lib.operations import operate_x
from lib.storage import Storage
from lib.utils import error
from lib.utils import notice

import numpy

APP_NAME = 'Kanji Tracker Application'
AUTHOR = '810Teams'
VERSION = 'b1.3.2'
OPERATIONS = [
    Operation('A', 'Append Data', [
        Argument('-add', 'Add mode'),
        Argument('-ntb', 'Notability mode')
    ]),
    Operation('C', 'Create Charts', [
        Argument('-days INTEGER', 'Duration'),
        Argument('-max-y INTEGER', 'Maximum y-labels'),
        Argument('-style STYLE_NAME', 'Style'),
        Argument('-dynamic', 'Dynamic fill'),
        Argument('-open', 'Open')
    ]),
    Operation('H', 'Help', []),
    Operation('R', 'Reload Storage', []),
    Operation('S', 'Save Storage', []),
    Operation('V', 'View Storage', [
        Argument('-open', 'Open')
    ]),
    Operation('X', 'Exit Application', []),
]


def main():
    ''' Main Function '''
    show_app_title()

    if load_default_storage():
        storage_main = Storage(load_default_storage()) 
    else:
        notice('Please Input Storage Name')
        storage_main = Storage(input('(Input) ').strip())
        print()
    
    if storage_main.try_load():
        notice('File \'DEFAULT_STORAGE.txt\' is found. Proceeding to storage loading.')
        notice('Storage \'{}\' is loaded.'.format(storage_main.name))
    storage_main.load()
    start_operating(storage_main)


def show_app_title():
    ''' Function: Show application title '''
    print()
    print('- {} -'.format(APP_NAME))
    print(('by {} ({})'.format(AUTHOR, VERSION)).center(len(APP_NAME)))
    print()


def start_operating(storage_main):
    ''' Function: Start operating application '''
    while True:
        print()
        print('- Operation List -')

        for i in OPERATIONS:
            print('[{}] {}'.format(i.code, i.title))
            for j in i.args:
                print('    {}{}: {}'.format(j.code, ' ' * (max([len(k.code) for k in i.args]) - len(j.code) + 1), j.description))

        print()

        try:
            action = [i for i in input('(Action) ').split()]
            print()
            operate(storage_main, action[0].upper(), action[1:])
        except IndexError:
            error('Invalid action format. Please try again.')


def operate(storage_main, action, args):
    ''' Function: Operate a specific action '''
    try:
        eval('operate_{}(storage_main, args)'.format(action.lower()))
    except (NameError, SyntaxError):
        error('Invalid action. Please try again.')


main()
