'''
    `main.py`
'''

from src.loaders import load_default_storage
from src.operations import Operation
from src.operations import Argument
from src.operations import operate_append
from src.operations import operate_chart
from src.operations import operate_help
from src.operations import operate_reload
from src.operations import operate_save
from src.operations import operate_view
from src.operations import operate_exit
from src.storage import Storage
from src.utils import error
from src.utils import notice

import numpy

APP_NAME = 'Kanji Tracker Application'
AUTHOR = '810Teams'
VERSION = 'b1.5.1'
OPERATIONS = [
    Operation('a', 'append', 'Append Data', [
        Argument('-add', 'Add mode'),
        Argument('-ntb', 'Notability mode')
    ]),
    Operation('c', 'chart', 'Create Charts', [
        Argument('-average INTEGER', 'Average (Default: All)'),
        Argument('-days INTEGER', 'Duration (Default: All)'),
        Argument('-max-y INTEGER', 'Maximum y-labels (Default: 15)'),
        Argument('-style STYLE_NAME', 'Style'),
        Argument('-dynamic', 'Dynamic Fill'),
        Argument('-open', 'Open'),
        Argument('-today', 'Today')
    ]),
    Operation('h', 'help', 'Help', []),
    Operation('r', 'reload', 'Reload Storage', []),
    Operation('s', 'save', 'Save Storage', []),
    Operation('v', 'view', 'View Storage', [
        Argument('-open', 'Open')
    ]),
    Operation('x', 'exit', 'Exit Application', []),
]


def main():
    ''' Main Function '''
    show_app_title()

    if load_default_storage():
        storage_main = Storage(load_default_storage()) 
    else:
        notice('Please Input Storage Name')
        print()
        storage_main = Storage(input('(Input) ').strip())
        print()
    
    if storage_main.try_load():
        notice('File \'DEFAULT_STORAGE.txt\' is found. Proceeding to storage loading.')
        notice('Storage \'{}\' is loaded.'.format(storage_main.name))
    storage_main.load()

    show_operations()
    start_operating(storage_main)


def show_app_title():
    ''' Function: Show application title '''
    print()
    print('- {} -'.format(APP_NAME))
    print(('by {} ({})'.format(AUTHOR, VERSION)).center(len(APP_NAME)))
    print()


def show_operations():
    ''' Function: Show operation list '''
    print()
    print('- Operation List -')

    for i in OPERATIONS:
        # print('[{}] {}'.format(i.command, i.title))
        print('[{}]'.format(i.command))
        for j in i.args:
            print('    {}{}: {}'.format(j.name, ' ' * (max([len(k.name) for k in i.args]) - len(j.name) + 1), j.description))


def start_operating(storage_main):
    ''' Function: Start operating application '''
    while True:
        print()
        try:
            action = [i for i in input('(Command) ').split()]
            print()
            operate(storage_main, action[0].lower(), action[1:])
        except IndexError:
            error('Invalid action format. Please try again.')


def operate(storage_main, action, args):
    ''' Function: Operate a specific action '''
    try:
        eval('operate_{}(storage_main, args)'.format(action.lower()))
    except (NameError, SyntaxError):
        try:
            eval('operate_{}(storage_main, args)'.format([i.command for i in OPERATIONS if i.code == action.lower()][0]))
        except (IndexError, NameError, SyntaxError):
            error('Invalid action. Please try again.')

main()
