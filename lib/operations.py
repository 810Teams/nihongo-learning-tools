'''
    `operations.py`
    @author 810Teams
'''

from lib.analysis import analysis
from lib.default_loader import load_default_style
from lib.storage import Storage
from lib.utils import error, kanji_calculate, notice

import subprocess


def operate_a(storage_main, args):
    ''' Function: Operation Code 'A' (Add Data) '''
    if '-k' in args:
        notice('Please input kanji data in a-1,b-2,b-3 format.')
        print()
        temp = input('(Input) ')
        print()
        storage_main.append([kanji_calculate(int(i.split(
            '-')[0]), int(i.split('-')[1])) for i in temp.replace(' ', '').split(',')])
    else:
        notice('Please input data in a,b,c format.')
        print()
        temp = input('(Input) ')
        print()
        storage_main.append([int(i) for i in temp.replace(' ', '').split(',')])


def operate_c(storage_main, args):
    ''' Function: Operation Code 'C' (Create Charts) '''
    if '-s' in args and len(args) >= 2:
        analysis(storage_main.storage, style=args[args.index('-s') + 1])
    else:
        if load_default_style():
            notice(
                'File \'DEFAULT_STYLE.txt\' is found. Now proceeding to chart creation.')
            notice('Style \'{}\' will be used in chart creation.'.format(
                load_default_style()))
            analysis(storage_main.storage, style=load_default_style())
        else:
            analysis(storage_main.storage)

    if '-o' in args:
        try:
            subprocess.call(['script/view_charts.sh'])
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


def operate_r(storage_main, args):
    ''' Function: Operation Code 'R' (Reload Storage) '''
    storage_main.reload()


def operate_s(storage_main, args):
    ''' Function: Operation Code 'S' (Save Storage) '''
    storage_main.save()


def operate_v(storage_main, args):
    ''' Function: Operation Code 'V' (View Storage) '''
    storage_main.view()

    if 'o' in args:
        try:
            subprocess.call(['script/view_storage.sh'])
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


def operate_x(storage_main, args):
    ''' Function: Operation Code 'X' (Exit) '''
    exit()
