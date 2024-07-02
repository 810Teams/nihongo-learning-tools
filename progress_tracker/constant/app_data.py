"""
    `core/app_data.py`
"""

from core.model.operation import Operation
from core.model.parameter import Parameter
from core.util.format import path
from progress_tracker.settings import DEFAULT_AVERAGE_RANGE, DEFAULT_DAYS, DEFAULT_DOTS_COUNT, DEFAULT_MAX_Y_LABELS, DEFAULT_STYLE, DEFAULT_X_LABEL


APP_NAME = 'Progress Tracker Application'
AUTHOR = '810Teams'
VERSION = 'v3.0.0a'

APPPLICATION_DIRECTORY = 'progress_tracker/'
STORAGE_BASE_PATH =  path(APPPLICATION_DIRECTORY, 'data')
STORAGE_FILE_EXTENSION = '.csv'
CHART_BASE_PATH =  path(APPPLICATION_DIRECTORY, 'export')
CHART_FILE_EXTENSION = '.svg'


class OperationList:
    class Append:
        class ParameterList:
            add: Parameter = Parameter('-add', description='Add mode')
            custom: Parameter = Parameter('--custom', value_type=int, description='Custom written method')

        operation = Operation = Operation('append', value_type=str, description='Append Data', parameter_list=[
            ParameterList.add,
            ParameterList.custom,
        ])

    class Chart:
        class ParameterList:
            allow_float: Parameter = Parameter('-allow-float', description='Allow floating points')
            dynamic: Parameter = Parameter('-dynamic', description='Dynamic fill')
            open: Parameter = Parameter('-open', description='Open after render')
            today: Parameter = Parameter('-today', description='Today')
            average_range: Parameter = Parameter('--average-range', value_type=int, description='Average range (Default: {})'.format(DEFAULT_AVERAGE_RANGE))
            days: Parameter = Parameter('--days', value_type=int, description='Duration in days (Default: {})'.format(DEFAULT_DAYS))
            dots_count: Parameter = Parameter('--dots-count', value_type=int, description='Maximum dot count (Default: {})'.format(DEFAULT_DOTS_COUNT))
            max_y: Parameter = Parameter('--max-y', value_type=int, description='Maximum y-labels (Default: {})'.format(DEFAULT_MAX_Y_LABELS))
            style: Parameter = Parameter('--style', value_type=str, description='Style (Default: {})'.format(DEFAULT_STYLE))
            x_label: Parameter = Parameter('--x-label', value_type=str, description='X-label type (Default: {}) (Available: [date, count, both])'.format(DEFAULT_X_LABEL))

        operation: Operation = Operation('chart', description='Create Charts', parameter_list=[
            ParameterList.allow_float,
            ParameterList.dynamic,
            ParameterList.open,
            ParameterList.today,
            ParameterList.average_range,
            ParameterList.days,
            ParameterList.dots_count,
            ParameterList.max_y,
            ParameterList.style,
            ParameterList.x_label,
        ])

    class Help:
        class ParameterList:
            pass

        operation: Operation = Operation('help', description='Display All Commands', parameter_list=[])

    class Open:
        class ParameterList:
            pass

        operation: Operation = Operation('open', description='Open Storage File', parameter_list=[])

    class Reload:
        class ParameterList:
            pass

        operation: Operation = Operation('reload', description='Reload Storage', parameter_list=[])

    class Save:
        class ParameterList:
            pass

        operation: Operation = Operation('save', description='Save Storage', parameter_list=[])

    class Sync:
        class ParameterList:
            pass

        operation: Operation = Operation('sync', description='Load Storage Backup', parameter_list=[])

    class View:
        class ParameterList:
            pass

        operation: Operation = Operation('view', description='View Storage', parameter_list=[])

    class Exit:
        class ParameterList:
            pass

        operation: Operation = Operation('exit', description='Exit Application', parameter_list=[])


OPERATION_LIST = [
    OperationList.Append.operation,
    OperationList.Chart.operation,
    OperationList.Help.operation,
    OperationList.Open.operation,
    OperationList.Reload.operation,
    OperationList.Save.operation,
    OperationList.Sync.operation,
    OperationList.View.operation,
    OperationList.Exit.operation,
]
