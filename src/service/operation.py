"""
    `operations.py`
"""

from custom.append import custom_append_head
from settings import DEFAULT_STORAGE, DEFAULT_STYLE

from src.service.render import RenderService
from src.model.command import Command
from src.model.storage import Storage
from src.util.logging import error
from src.util.logging import notice

import os


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


class OperationService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.render_service = RenderService(storage)


    def execute(self, command: Command) -> None:
        try:
            exec('self.operate_{}(command)'.format(command.name))
        except AttributeError:
            print()
            error('Command name \'{}\' does not exist.'.format(command.name))
    

    def operate_append(self, command: Command) -> None:
        """ Function: Operation Code 'A' (Add Data) """
        print()

        if command.contains_argument('-add'):
            notice('Please input increasing data in a,b,c format.')
            print()
            temp = input('(Input) ')

            try:
                temp = [i.replace(' ', '') for i in temp.split(',')]

                for i in range(len(temp)):
                    if (temp[i] == ''):
                        temp[i] = 0
                    else:
                        temp[i] = int(temp[i])

                initial = self.storage.to_list()[-1][1:]
                self.storage.append([int(initial[i]) + temp[i] for i in range(len(initial))])
            except ValueError:
                error('Invalid value format. Please try again.')

        elif command.contains_argument('-custom'):
            try:
                custom_id = int(command.get_argument('-custom').value)
                if custom_id not in (1, 2, 3, 4, 5):
                    error('Custom ID must be an integer from 1 to 5.')
                    return
            except (IndexError, ValueError):
                error('Custom ID must be an integer.')
                return
            
            notice('Please input custom formatted data.')
            print()
            temp = input('(Input) ')

            try:
                self.storage.append(custom_append_head(temp, custom_id))
            except IndexError:
                error('Invalid value format. Please try again.')
                error('Function \'custom_append_{}\' might not have been implemented.'.format(custom_id))

        else:
            notice('Please input data in a,b,c format.')
            print()
            temp = input('(Input) ')

            try:
                temp = [i.replace(' ', '') for i in temp.split(',')]

                for i in range(len(temp)):
                    if (temp[i] == ''):
                        temp[i] = 0
                    else:
                        temp[i] = int(temp[i])

                self.storage.append(temp)
            except ValueError:
                error('Invalid value format. Please try again.')


    def operate_chart(self, command: Command) -> None:
        """ Function: Operation Code 'C' (Create Charts) """
        print()
        
        # Step 0: -open-only argument
        if command.contains_argument('-open-only'):
            try:
                os.open('charts/*')
                notice('Opening chart files.')
            except (FileNotFoundError, OSError, PermissionError):
                error('Chart files opening error')
            finally:
                return

        # Step 1: -average argument
        average_range = None
        if command.contains_argument('-average-range'):
            # Test for valid format
            try:
                average_range = int(command.get_argument('-average-range').value)
            except (IndexError, ValueError):
                error('Average range must be an integer.')
                error('Aborting chart creation process.')
                return

        # Step 2: -days argument
        days = 0
        if command.contains_argument('-days'):
            # Test for valid format
            try:
                days = int(command.get_argument('-days').value)
            except (IndexError, ValueError):
                error('Duration must be an integer.')
                error('Aborting chart creation process.')
                return
        
        # Step 3: -max-dots argument
        max_dots = 100
        if command.contains_argument('-max-dots'):
            try:
                max_dots = int(command.get_argument('-max-dots').value)
            except (IndexError, ValueError):
                error('Maximum dots must be an integer.')
                error('Aborting chart creation process.')
                return

        # Step 4: -max-y argument
        max_y_labels = 15
        if command.contains_argument('-max-y'):
            # Step 4.1 - Test for valid format
            try:
                max_y_labels = int(command.get_argument('-max-y').value)
            except (IndexError, ValueError):
                error('Maximum y labels must be an integer.')
                error('Aborting chart creation process.')
                return
            
            # Step 4.2 - Test for valid requirements
            if not (max_y_labels >= 2):
                error('Maximum y labels must be an integer at least 2.')
                error('Aborting chart creation process.')
                return
        
        # Step 5: -style argument
        style = 'DefaultStyle'
        if command.contains_argument('-style'):
            # Step 5.1.1 - Test for valid format
            try:
                style = command.get_argument('-style').value
            except (IndexError, ValueError):
                error('Invalid style.')
                error('Aborting chart creation process.')
                return

            # Step 5.1.2 - Test for valid requirements
            if style not in STYLES:
                error('Invalid style.')
                error('Aborting chart creation process.')
                return
        elif DEFAULT_STYLE:
            style = DEFAULT_STYLE

            # Step 4.2.1 - Test for valid requirements
            if DEFAULT_STYLE not in STYLES:
                error('Invalid style found in \'settings.py\'.')
                error('Aborting chart creation process.')
                return

            notice('Default style is found in \'settings.py\', now proceeding to chart creation.')
            notice('Style \'{}\' will be used in chart creation.'.format(DEFAULT_STYLE))

        # Step 6: -x-label argument
        x_label = 'date'
        if command.contains_argument('-x-label'):
            # Step 6.1 - Test for valid format
            try:
                x_label = command.get_argument('-x-label').value
            except (IndexError, ValueError):
                error('X-label type must be a string.')
                error('Aborting chart creation process.')
                return
            
            # Step 6.2 - Test for valid requirements
            if x_label not in ('date', 'count', 'both'):
                error('X-label type must be either \'date\', \'count\', or \'both\'')
                error('Aborting chart creation process.')
                return
            
        # Step 7: Render charts
        self.render_service.render_all(
            allow_float=command.contains_argument('-allow-float'),
            average_range=average_range,
            days=days,
            is_dynamic=command.contains_argument('-dynamic'),
            is_today=command.contains_argument('-today'),
            max_dots=max_dots,
            max_y_labels=max_y_labels,
            style=style,
            x_label=x_label
        )

        # Step 8: -open argument
        if command.contains_argument('-open'):
            try:
                os.open('charts/*')
                notice('Opening chart files.')
            except (FileNotFoundError, OSError, PermissionError):
                error('Something unexpected happened, please try again.')


    def operate_help(self, command: Command) -> None:
        """ Function: Operation Code 'H' (Help) """
        try:
            os.open('HELP.md')
            notice('Opening \'HELP.md\'')
        except (FileNotFoundError, OSError, PermissionError):
            error('Something unexpected happened, please try again.')


    def operate_reload(self, command: Command) -> None:
        """ Function: Operation Code 'R' (Reload Storage) """
        self.storage.reload()


    def operate_save(self, command: Command) -> None:
        """ Function: Operation Code 'S' (Save Storage) """
        self.storage.save()


    def operate_view(self, command: Command) -> None:
        """ Function: Operation Code 'V' (View Storage) """
        self.storage.view()

        if command.contains_argument('-open'):
            try:
                os.open('data/' + self.storage.name + '.csv')
                print()
                notice('Opening file \'{}.csv\''.format(self.storage.name))
            except (FileNotFoundError, OSError, PermissionError):
                error('Opening storage file \'{}\' error.'.format(self.storage.name))


    def operate_exit(self, command: Command) -> None:
        """ Function: Operation Code 'X' (Exit) """
        notice('Exitting application.')
        print()
        exit()
