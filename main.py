'''
    `main.py`
'''

from lib.loaders import load_default_storage
from lib.operations import operate_a, operate_c, operate_r, operate_s, operate_v, operate_x
from lib.storage import Storage
from lib.utils import error, notice
import numpy

AUTHOR = '810Teams'
VERSION = 'b1.0.0'
OPERATIONS = {
    'A': 'Append Data (-k : kanji)',
    'C': 'Kanji Charts (-s <StyleName> : style, -o : open)',
    'R': 'Reload Storage',
    'S': 'Save Storage',
    'V': 'View Storage (-o : open)',
    'X': 'Exit Application'
}


def main():
    ''' Main Function '''
    print()
    print('- Personal Kanji Tracker App -')
    print(('by {} ({})'.format(AUTHOR, VERSION)).center(28))
    print()

    if load_default_storage():
        notice(
            'File \'DEFAULT_STORAGE.txt\' is found. Now proceeding to storage loading.')
        storage_main = Storage(load_default_storage())
    else:
        notice('Please Input Storage Name')
        storage_main = Storage(input('(Input) ').strip())
        print()
    storage_main.load()

    while True:
        print()
        print('- Action List -')

        for i in OPERATIONS:
            print('[{}] {}'.format(i, OPERATIONS[i]))

        print()
        action = [i for i in input('(Action) ').split()]
        print()
        operate(storage_main, action[0].upper(), action[1:])


def operate(storage_main, action, args):
    ''' Function: Operate a specific action '''
    try:
        eval('operate_{}(storage_main, args)'.format(action.lower()))
    except NameError:
        error('Invalid action. Please try again.')


main()
