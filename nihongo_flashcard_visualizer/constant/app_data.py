"""
    `nihongo_flashcard_visualzer/constant/app_data.py`
"""

from core.model.operation import Operation
from core.model.parameter import Parameter
from core.util.format import path
from nihongo_flashcard_visualizer.settings import *


APP_NAME = 'Nihongo Flashcard Visualizer'
AUTHOR = '810Teams'
VERSION = 'v3.0.0a'

APPLICATION_DIRECTORY = 'nihongo_flashcard_visualizer'
DATABASE_BASE_PATH = path(APPLICATION_DIRECTORY, 'data')
DATABASE_CONTAINER_NAME = 'NihongoBackup.nihongodata'
DATABASE_FILE_NAME = 'Flashcards.sqlite'
ZIP_FILE_EXTENSION = '.zip'
CHART_BASE_PATH = path(APPLICATION_DIRECTORY, 'export')
CHART_FILE_EXTENSION = '.svg'


class OperationList:
    class Chart:
        class ParameterList:
            no_dot_shrink = Parameter('-no-dot-shrink', description='Disable dots shrinking')
            show_correlation = Parameter('-show-correl', description='Show correlation')
            simulation_mode = Parameter('-simulation-mode', description='Simulation mode')
            open = Parameter('-open', description='Open after render')
            open_only = Parameter('-open-only', description='Open without render')
            days = Parameter('--days', value_type=int, default_value=DEFAULT_DAYS, validation=lambda i: i > 2, error_message='Days value must be an integer at least 2.', description='Duration')
            incorrect_probability = Parameter('--inc-p', value_type=float, default_value=DEFAULT_INCORRECT_PROBABILITY, description='Incorrect probability')
            max_y = Parameter('--max-y', value_type=int, default_value=DEFAULT_MAX_Y_LABELS, description='Maximum y-labels')
            style = Parameter('--style', value_type=str, default_value=DEFAULT_STYLE, description='Style')

        operation = Operation('chart', description='Create Charts', parameter_list=[
            ParameterList.no_dot_shrink,
            ParameterList.show_correlation,
            ParameterList.simulation_mode,
            ParameterList.open,
            ParameterList.open_only,
            ParameterList.days,
            ParameterList.max_y,
            ParameterList.incorrect_probability,
            ParameterList.style,
        ])

    class Extract:
        class ParameterList:
            pass

        operation = Operation('extract', description='Extract and Update the SQLite File', parameter_list=[])

    class Help:
        class ParameterList:
            pass

        operation = Operation('help', description='Display All Commands', parameter_list=[])

    class Statistics:
        class ParameterList:
            pass

        operation = Operation('stat', description='View Statistics', parameter_list=[])

    class Exit:
        class ParameterList:
            pass

        operation = Operation('exit', description='Exit Application', parameter_list=[])


OPERATION_LIST = [
    OperationList.Chart.operation,
    OperationList.Extract.operation,
    OperationList.Help.operation,
    OperationList.Statistics.operation,
    OperationList.Exit.operation,
]
