"""
    `main.py`
"""

from src.model.storage import Storage
from src.service.operation import OperationService
from src.util.logging import error
from src.util.logging import notice
from settings import DEFAULT_STORAGE
from src.util.reader import extract_command_and_arguments


APP_NAME = 'Progress Tracker Application'
AUTHOR = '810Teams'
VERSION = 'v1.3.0'
# OPERATIONS = [
#     Operation('a', 'append', 'Append Data', [
#         Argument('-add', 'Add mode'),
#         Argument('-cus INTEGER', 'Custom written method')
#     ]),
#     Operation('c', 'chart', 'Create Charts', [
#         Argument('-average INTEGER', 'Average (Default: All)'),
#         Argument('-days INTEGER', 'Duration (Default: All)'),
#         Argument('-max-y INTEGER', 'Maximum y-labels (Default: 15)'),
#         Argument('-style STYLE_NAME', 'Style'),
#         Argument('-x-label [date,count,both]', 'X-label type (Default: date)'),
#         Argument('-allow-float', 'Allow floating points'),
#         Argument('-dynamic', 'Dynamic Fill'),
#         Argument('-open', 'Open'),
#         Argument('-open-only', 'Open Only'),
#         Argument('-today', 'Today')
#     ]),
#     Operation('h', 'help', 'Help', []),
#     Operation('r', 'reload', 'Reload Storage', []),
#     Operation('s', 'save', 'Save Storage', []),
#     Operation('v', 'view', 'View Storage', [
#         Argument('-open', 'Open')
#     ]),
#     Operation('x', 'exit', 'Exit Application', []),
# ]


class ProgressTrackerApplication:
    def __init__(self) -> None:
        self.operation_service = OperationService(None)

    def run(self):
        """ Main Function """
        self.show_app_title()

        if isinstance(DEFAULT_STORAGE, str):
            storage_main = Storage(DEFAULT_STORAGE) 
        else:
            notice('Please Input Storage Name')
            print()
            storage_main = Storage(input('(Input) ').strip())
            print()
        
        if storage_main.try_load():
            notice('Default storage is set, proceeding to storage loading.')
            notice('Storage \'{}\' is loaded.'.format(storage_main.name))
        storage_main.load()

        # show_operations()
        self.operation_service.storage = storage_main
        self.start_operating(storage_main)


    def show_app_title(self):
        """ Function: Show application title """
        print()
        print('- {} -'.format(APP_NAME))
        print(('by {} ({})'.format(AUTHOR, VERSION)).center(len(APP_NAME)))
        print()


    # def show_operations():
    #     """ Function: Show operation list """
    #     print()
    #     print('- Operation List -')

    #     for i in OPERATIONS:
    #         # print('[{}] {}'.format(i.command, i.title))
    #         print('[{}]'.format(i.command))
    #         for j in i.args:
    #             print('    {}{}: {}'.format(j.name, ' ' * (max([len(k.name) for k in i.args]) - len(j.name) + 1), j.description))


    def start_operating(self, storage_main):
        """ Function: Start operating application """
        while True:
            print()
            try:
                line = input('(Command) ')
                print()
                self.operate(line)
            except IndexError:
                error('Invalid action format. Please try again.')


    def operate(self, line: str):
        """ Function: Operate a specific action """
        self.operation_service.execute(extract_command_and_arguments(line))


def main():
    application = ProgressTrackerApplication()
    application.run()


main()
