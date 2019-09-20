'''
    `main.py`

    @author 810Teams
    @version a0.6.0
'''

from lib.default_loader import load_default_storage
from lib.operations import operate_a, operate_c, operate_r, operate_s, operate_v, operate_x
from lib.storage import Storage
from lib.utils import error, notice
import numpy


def main():
    ''' Main Function '''
    print()
    print('- Personal Kanji Tracker Terminal Application -')
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
        print('[A] Append Data (-k : kanji)')
        print('[C] Kanji Charts (-s <StyleName> : style, -o : open)')
        print('[R] Reload Storage')
        print('[S] Save Storage')
        print('[V] View Storage (-o : open)')
        print('[X] Exit Application')
        print()
        action = [i for i in input('(Action) ').split()]
        print()
        operate(storage_main, action[0].upper(), action[1:])


def operate(storage_main, action, args):
    ''' Function: Operate a specific action '''
    if action == 'A':
        operate_a(storage_main, args)
    elif action == 'C':
        operate_c(storage_main, args)
    elif action == 'R':
        operate_r(storage_main, args)
    elif action == 'S':
        operate_s(storage_main, args)
    elif action == 'V':
        operate_v(storage_main, args)
    elif action == 'X':
        operate_x(storage_main, args)
    else:
        error('Invalid action. Please try again.')


main()
