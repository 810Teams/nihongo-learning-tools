"""
    `main.py`
"""

from src.model.parameter import Parameter
from src.app_data import APP_NAME, AUTHOR, VERSION
from src.model.argument import Argument
from src.model.operation import Operation
from src.model.storage import Storage
from src.service.operation_service import OperationService
from src.util.logging import error, notice
from src.util.reader import extract_command_and_arguments
from settings import DEFAULT_STORAGE


OPERATIONS = [
    Operation('append', code='a', value_type=str, description='Append Data', argument_list=[
        Parameter('-add', description='Add mode'),
        Parameter('-cus', value_type=int, description='Custom written method')
    ]),
    Operation('chart', code='c', description='Create Charts', argument_list=[
        Parameter('-average', value_type=int, description='Average (Default: All)'),
        Parameter('-days', value_type=int, description='Duration (Default: All)'),
        Parameter('-max-y', value_type=int, description='Maximum y-labels (Default: 15)'),
        Parameter('-style', value_type=str, description='Style'),
        Parameter('-x-label', value_type=str, description='X-label type (Default: date [date,count,both])'),
        Parameter('-allow-float', description='Allow floating points'),
        Parameter('-dynamic', description='Dynamic Fill'),
        Parameter('-open', description='Open'),
        Parameter('-open-only', description='Open Only'),
        Parameter('-today', description='Today')
    ]),
    Operation('reload', code='r', description='Reload Storage', argument_list=[]),
    Operation('save', code='s', description='Save Storage', argument_list=[]),
    Operation('view', code='v', description='View Storage', argument_list=[
        Parameter('-open', 'Open')
    ]),
    Operation('exit', code='x', description='Exit Application', argument_list=[]),
]


class ProgressTrackerApplication:
    def __init__(self) -> None:
        self.operation_service = OperationService(None)

    def run(self) -> None:
        """ Main Function """
        print()
        print('- {} -'.format(APP_NAME))
        print(('by {} ({})'.format(AUTHOR, VERSION)).center(len(APP_NAME)))

        if isinstance(DEFAULT_STORAGE, str):
            storage = Storage(DEFAULT_STORAGE) 
        else:
            print()
            notice('Please Input Storage Name')
            print()
            storage = Storage(input('(Input) ').strip())
            
        if storage.try_load():
            print()
            notice('Default storage is set, proceeding to storage loading.')
            notice('Storage \'{}\' is loaded.'.format(storage.name))
        storage.load()

        print()
        for i in OPERATIONS:
            print(i)

        self.operation_service.storage = storage
        self.operation_service.render_service.storage = storage
        self.start()

    def start(self) -> None:
        """ Function: Start operating application """
        while True:
            try:
                print()
                line = input('(Command) ')

                if line.strip() == str():
                    continue

                self.operation_service.execute(extract_command_and_arguments(line))
            except IndexError:
                error('Invalid action format. Please try again.')
        

def main() -> None:
    application = ProgressTrackerApplication()
    application.run()


main()
