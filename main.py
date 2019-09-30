'''
    `main.py`
'''

from lib.loaders import load_default_storage
from lib.operations import Operation, Argument, operate_a, operate_c, operate_r, operate_s, operate_v, operate_x
from lib.storage import Storage
from lib.utils import error, notice
import numpy

AUTHOR = '810Teams'
VERSION = 'b1.1.0'
OPERATIONS = [
    Operation('A', 'Append Data', [
        Argument('-k', 'kanji notability list')
    ]),
    Operation('C', 'Create Charts', [
        Argument('-d <days>', 'duration'),
        Argument('-dy', 'dynamic fill'),
        Argument('-o', 'open'),
        Argument('-s <style_name>', 'style')
    ]),
    Operation('R', 'Reload Storage', []),
    Operation('S', 'Save Storage', []),
    Operation('V', 'View Storage', [
        Argument('-o', 'open')
    ]),
    Operation('X', 'Exit Application', []),
]


def main():
    ''' Main Function '''
    show_app_title()

    if load_default_storage():
        notice('File \'DEFAULT_STORAGE.txt\' is found. Now proceeding to storage loading.')
        storage_main = Storage(load_default_storage())
        notice('Storage \'{}\' is loaded.'.format(storage_main.name))
    else:
        notice('Please Input Storage Name')
        storage_main = Storage(input('(Input) ').strip())
        print()

    storage_main.load(template='jlpt')
    start_operating(storage_main)


def show_app_title():
    ''' Function: Show application title '''
    print()
    print('- Personal Kanji Tracker App -')
    print(('by {} ({})'.format(AUTHOR, VERSION)).center(28))
    print()


def start_operating(storage_main):
    ''' Function: Start operating application '''
    while True:
        print()
        print('- Action List -')

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
