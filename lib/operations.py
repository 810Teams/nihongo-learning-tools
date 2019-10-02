'''
    `operations.py`
'''

from lib.analysis import analysis
from lib.loaders import load_default_style
from lib.storage import Storage
from lib.utils import error, kanji_calculate, notice

import os
import numpy
import pandas


class Operation:
    def __init__(self, code, title, args):
        self.code = code
        self.title = title
        self.args = args
    
    def operate(self, storage_main, args):
        try:
            eval('operate_{}(storage_main, args)'.format(self.code.lower()))
        except (NameError, SyntaxError):
            error('Invalid action. Please try again.')


class Argument:
    def __init__(self, code, description):
        self.code = code
        self.description = description


def operate_a(storage_main, args):
    ''' Function: Operation Code 'A' (Add Data) '''
    if '-a' in args:
        notice('Please input increasing data in a,b,c format.')
        print()
        temp = input('(Input) ')
        print()

        try:
            temp = [int(i.replace(' ', ''))for i in temp.split(',')]
            initial = storage_main.tolist()[-1][1:]
            storage_main.append([int(initial[i]) + temp[i] for i in range(len(initial))])
        except ValueError:
            error('Invalid value format. Please try again.')
    elif '-k' in args:
        notice('Please input kanji data in a x,b y,c z format.')
        print()
        temp = input('(Input) ')
        print()

        try:
            storage_main.append([kanji_calculate(int(i.split()[0]), int(i.split()[1])) for i in temp.split(',')])
        except ValueError:
            error('Invalid value format. Please try again.')
    else:
        notice('Please input data in a,b,c format.')
        print()
        temp = input('(Input) ')
        print()

        try:
            storage_main.append([int(i.replace(' ', ''))for i in temp.split(',')])
        except ValueError:
            error('Invalid value format. Please try again.')


def operate_c(storage_main, args):
    ''' Function: Operation Code 'C' (Create Charts) '''
    # Step 1: -d argument
    try:
        duration = int(args[args.index('-d') + 1])
    except (IndexError, ValueError):
        duration = None
    
    # Step 2: -s argument
    try:
        style = args[args.index('-s') + 1]
    except (IndexError, ValueError):
        if load_default_style():
            notice('File \'DEFAULT_STYLE.txt\' is found. Now proceeding to chart creation.')
            notice('Style \'{}\' will be used in chart creation.'.format(load_default_style()))
            style = load_default_style()
        else:
            style = 'DefaultStyle'

    # Step 3: Render charts
    analysis(storage_main.storage, duration=duration, dynamic=('-dy' in args), style=style)

    # Step 4: -o argument
    if '-o' in args:
        try:
            os.system('open charts/*')
            notice('Opening chart files...')
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

    if '-o' in args:
        try:
            os.system('open data/' + storage_main.name + '.csv')
            print()
            notice('Opening file \'{}.csv\''.format(storage_main.name))
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


def operate_x(storage_main, args):
    ''' Function: Operation Code 'X' (Exit) '''
    notice('Exitting application.')
    print()
    exit()
