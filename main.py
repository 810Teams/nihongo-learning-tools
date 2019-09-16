'''
    `main.py`

    @author 810Teams
    @version a0.5.0
'''

from lib.analysis import analysis
from lib.storage import Storage
from lib.utils import error, kanji_calculate, notice
import numpy

def main():
    ''' Main Function '''
    print()
    print('- Personal Kanji Tracker Terminal Application -')
    print()

    if load_default_storage():
        notice('File \'DEFAULT_STORAGE.txt\' is found. Now proceeding to storage loading.')
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
        print('[C] Kanji Charts (-s <StyleName> : style)')
        print('[R] Reload Storage')
        print('[S] Save Storage')
        print('[V] View Storage')
        print('[X] Exit Application')
        print()
        action = [i for i in input('(Action) ').split()]
        print()
        operate(storage_main, action[0].upper(), action[1:])

def operate(storage_main, action, args):
    ''' Function: Operate a specific action '''
    if action == 'A':
        if '-k' in args:
            notice('Please input kanji data in a-1,b-2,b-3 format.')
            print()
            temp = input('(Input) ')
            print()
            storage_main.append([kanji_calculate(int(i.split('-')[0]), int(i.split('-')[1])) for i in temp.replace(' ', '').split(',')])
        else:
            notice('Please input data in a,b,c format.')
            print()
            temp = input('(Input) ')
            print()
            storage_main.append([int(i) for i in temp.replace(' ', '').split(',')])
    elif action == 'C':
        if '-s' in args:
            analysis(storage_main.storage, style=args[args.index('-s') + 1])
        else:
            if load_default_style():
                notice('File \'DEFAULT_STYLE.txt\' is found. Now proceeding to chart creation.')
                notice('Style \'{}\' will be used in chart creation.'.format(load_default_style()))
                analysis(storage_main.storage, style=load_default_style())
            else:
                analysis(storage_main.storage)
    elif action == 'R':
        storage_main.reload()
    elif action == 'S':
        storage_main.save()
        notice('Storage \'{}\' saved successfully.'.format(storage_main.name))
    elif action == 'V':
        storage_main.view()
    elif action == 'X':
        exit()
    else:
        error('Invalid action.')

def load_default_storage():
    ''' Function: Load default storage '''
    try:
        name = list(open('DEFAULT_STORAGE.txt'))[0].replace('\n', '').strip()
        return name
    except FileNotFoundError:
        return None

def load_default_style():
    ''' Function: Load default style '''
    try:
        name = [i.replace('\n', '').strip() for i in list(open('DEFAULT_STYLE.txt'))][0]
        return name
    except FileNotFoundError:
        return None

main()
