'''
    `operations.py`
'''

from src.analysis import analysis
from src.loaders import load_default_style
from src.storage import Storage
from src.utils import error
from src.utils import kanji_calculate
from src.utils import notice

import os
import numpy
import pandas

STYLES = (
    'DefaultStyle',
    'DarkStyle',
    'NeonStyle',
    'DarkSolarizedStyle',
    'LightSolarizedStyle',
    'LightStyle',
    'CleanStyle',
    'RedBlueStyle',
    'DarkColorizedStyle',
    'LightColorizedStyle',
    'TurquoiseStyle',
    'LightGreenStyle',
    'DarkGreenStyle',
    'DarkGreenBlueStyle',
    'BlueStyle'
)


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
    if '-add' in args:
        notice('Please input increasing data in a,b,c format.')
        print()
        temp = input('(Input) ')
        print()

        try:
            temp = [int(i.replace(' ', ''))for i in temp.split(',')]
            initial = storage_main.to_list()[-1][1:]
            storage_main.append([int(initial[i]) + temp[i] for i in range(len(initial))])
        except ValueError:
            error('Invalid value format. Please try again.')
    elif '-ntb' in args:
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
    # Step 1: -days argument
    if '-days' in args:
        # Step 1.1 - Test for valid format
        try:
            duration = int(args[args.index('-days') + 1])
        except (IndexError, ValueError):
            error('Duration must be an integer.')
            error('Aborting chart creation process.')
            return
        
        # Step 1.2 - Test for valid requirements
        if not (isinstance(duration, int) and -len(storage_main.storage) + 2 <= duration <= len(storage_main.storage) and duration != 1):
            error('Duration must be an integer between {} and {}, and not 1.'.format(-len(storage_main.storage) + 2, len(storage_main.storage)))
            error('Aborting chart creation process.')
            return
    else:
        duration = 0

    # Step 2: -max-y argument
    if '-max-y' in args:
        # Step 2.1 - Test for valid format
        try:
            max_y_labels = int(args[args.index('-max-y') + 1])
        except (IndexError, ValueError):
            error('Maximum y labels must be an integer.')
            error('Aborting chart creation process.')
            return
        
        # Step 2.2 - Test for valid requirements
        if not (max_y_labels >= 2):
            error('Maximum y labels must be an integer at least 2.')
            error('Aborting chart creation process.')
            return
    else:
        max_y_labels = 15
    
    # Step 3: -style argument
    if '-style' in args:
        # Step 3.1.1 - Test for valid format
        try:
            style = args[args.index('-style') + 1]
        except (IndexError, ValueError):
            error('Invalid style.')
            error('Aborting chart creation process.')
            return

        # Step 3.1.2 - Test for valid requirements
        if style not in STYLES:
            error('Invalid style.')
            error('Aborting chart creation process.')
            return
    elif load_default_style():
        style = load_default_style().strip()

        # Step 3.2.1 - Test for valid requirements
        if style not in STYLES:
            error('Invalid style found in \'DEFAULT_STYLE.txt\'.')
            error('Aborting chart creation process.')
            return

        notice('File \'DEFAULT_STYLE.txt\' is found. Now proceeding to chart creation.')
        notice('Style \'{}\' will be used in chart creation.'.format(style))
    else:
        style = 'DefaultStyle'

    # Step 4: Render charts
    analysis(storage_main.storage, duration=duration, max_y_labels=max_y_labels, style=style, dynamic=('-dynamic' in args))

    # Step 5: -open argument
    if '-open' in args:
        try:
            os.system('open charts/*')
            notice('Opening chart files.')
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


def operate_h(storage_main, args):
    ''' Function: Operation Code 'H' (Help) '''
    try:
        os.system('open HELP.md')
        notice('Opening \'HELP.md\'')
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

    if '-open' in args:
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
