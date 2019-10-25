'''
    `operations.py`
'''

from custom.custom_append import custom_append_1
from custom.custom_append import custom_append_2
from custom.custom_append import custom_append_3
from custom.custom_append import custom_append_4
from custom.custom_append import custom_append_5
from src.analysis import analysis, clean
from src.loaders import load_default_style
from src.storage import Storage
from src.utils import error
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
    def __init__(self, code, command, title, args):
        self.code = code
        self.command = command
        self.title = title
        self.args = args
    
    def operate(self, storage_main, args):
        try:
            eval('operate_{}(storage_main, args)'.format(self.command.lower()))
        except (NameError, SyntaxError):
            error('Invalid action. Please try again.')


class Argument:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def operate_append(storage_main, args):
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
    elif '-cus' in args:
        try:
            custom_id = int(args[args.index('-cus') + 1])
            if custom_id not in (1, 2, 3, 4, 5):
                error('Custom ID must be an integer from 1 to 5.')
                return
        except (IndexError, ValueError):
            error('Custom ID must be an integer.')
            return
        
        notice('Please input custom formatted data.')
        print()
        temp = input('(Input) ')
        print()

        try:
            eval('storage_main.append([custom_append_{}([int(i.split()[0]), int(i.split()[1])]) for i in temp.split(\',\')])'.format(custom_id))
        except IndexError:
            error('Invalid value format. Please try again.')
            error('Function \'custom_append_{}\' might not have been implemented.'.format(custom_id))
    else:
        notice('Please input data in a,b,c format.')
        print()
        temp = input('(Input) ')
        print()

        try:
            storage_main.append([int(i.replace(' ', ''))for i in temp.split(',')])
        except ValueError:
            error('Invalid value format. Please try again.')


def operate_chart(storage_main, args):
    ''' Function: Operation Code 'C' (Create Charts) '''
    # Step 1: -average argument
    if '-average' in args:
        # Test for valid format
        try:
            average_range = int(args[args.index('-average') + 1])
        except (IndexError, ValueError):
            error('Average range must be an integer.')
            error('Aborting chart creation process.')
            return
    else:
        average_range = None

    # Step 2: -days argument
    if '-days' in args:
        # Test for valid format
        try:
            duration = int(args[args.index('-days') + 1])
        except (IndexError, ValueError):
            error('Duration must be an integer.')
            error('Aborting chart creation process.')
            return
    else:
        duration = 0

    # Step 3: -max-y argument
    if '-max-y' in args:
        # Step 3.1 - Test for valid format
        try:
            max_y_labels = int(args[args.index('-max-y') + 1])
        except (IndexError, ValueError):
            error('Maximum y labels must be an integer.')
            error('Aborting chart creation process.')
            return
        
        # Step 3.2 - Test for valid requirements
        if not (max_y_labels >= 2):
            error('Maximum y labels must be an integer at least 2.')
            error('Aborting chart creation process.')
            return
    else:
        max_y_labels = 15
    
    # Step 4: -style argument
    if '-style' in args:
        # Step 4.1.1 - Test for valid format
        try:
            style = args[args.index('-style') + 1]
        except (IndexError, ValueError):
            error('Invalid style.')
            error('Aborting chart creation process.')
            return

        # Step 4.1.2 - Test for valid requirements
        if style not in STYLES:
            error('Invalid style.')
            error('Aborting chart creation process.')
            return
    elif load_default_style():
        style = load_default_style().strip()

        # Step 4.2.1 - Test for valid requirements
        if style not in STYLES:
            error('Invalid style found in \'DEFAULT_STYLE.txt\'.')
            error('Aborting chart creation process.')
            return

        notice('File \'DEFAULT_STYLE.txt\' is found. Now proceeding to chart creation.')
        notice('Style \'{}\' will be used in chart creation.'.format(style))
    else:
        style = 'DefaultStyle'

    # Step 5: Render charts
    analysis(
        storage_main,
        allow_float=('-allow-float' in args),
        average_range=average_range,
        duration=duration,
        is_dynamic=('-dynamic' in args),
        max_y_labels=max_y_labels,
        style=style,
        is_today=('-today' in args)
    )

    # Step 6: -open argument
    if '-open' in args:
        try:
            os.system('open charts/*')
            notice('Opening chart files.')
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


def operate_help(storage_main, args):
    ''' Function: Operation Code 'H' (Help) '''
    try:
        os.system('open HELP.md')
        notice('Opening \'HELP.md\'')
    except (FileNotFoundError, OSError, PermissionError):
        error('Something unexpected happened, please try again.')


def operate_reload(storage_main, args):
    ''' Function: Operation Code 'R' (Reload Storage) '''
    storage_main.reload()


def operate_save(storage_main, args):
    ''' Function: Operation Code 'S' (Save Storage) '''
    storage_main.save()


def operate_view(storage_main, args):
    ''' Function: Operation Code 'V' (View Storage) '''
    storage_main.view()

    if '-open' in args:
        try:
            os.system('open data/' + storage_main.name + '.csv')
            print()
            notice('Opening file \'{}.csv\''.format(storage_main.name))
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


def operate_exit(storage_main, args):
    ''' Function: Operation Code 'X' (Exit) '''
    notice('Exitting application.')
    print()
    exit()
