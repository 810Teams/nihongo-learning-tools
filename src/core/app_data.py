"""
    `src/core/app_data.py`
"""

from settings import DEFAULT_AVERAGE_RANGE, DEFAULT_DAYS, DEFAULT_DOTS_COUNT, DEFAULT_MAX_Y_LABELS, DEFAULT_STYLE, DEFAULT_X_LABEL
from src.model.operation import Operation
from src.model.parameter import Parameter


APP_NAME = 'Progress Tracker Application'
AUTHOR = '810Teams'
VERSION = 'v3.0.0a'

STORAGE_BASE_PATH = 'data/'
STORAGE_FILE_EXTENSION = '.csv'
CHART_BASE_PATH = 'charts/'

VALUE_PARSING_ARGUMENT_IDENTIFIER = '-'
MODIFICATION_ARGUMENT_IDENTIFIER = '--'


class OperationList:
    class Append:
        class ParameterList:
            custom: Parameter = Parameter('-custom', value_type=int, description='Custom written method')
            add: Parameter = Parameter('--add', description='Add mode')
        
        operation = Operation = Operation('append', value_type=str, description='Append Data', parameter_list=[
            ParameterList.custom,
            ParameterList.add
        ])
    
    class Chart:
        class ParameterList:
            average_range: Parameter = Parameter('-average-range', value_type=int, description='Average range (Default: {})'.format(DEFAULT_AVERAGE_RANGE))
            days: Parameter = Parameter('-days', value_type=int, description='Duration in days (Default: {})'.format(DEFAULT_DAYS))
            dots_count: Parameter = Parameter('-dots-count', value_type=int, description='Maximum dot count (Default: {})'.format(DEFAULT_DOTS_COUNT))
            max_y: Parameter = Parameter('-max-y', value_type=int, description='Maximum y-labels (Default: {})'.format(DEFAULT_MAX_Y_LABELS))
            style: Parameter = Parameter('-style', value_type=str, description='Style (Default: {})'.format(DEFAULT_STYLE))
            x_label: Parameter = Parameter('-x-label', value_type=str, description='X-label type (Default: {}) (Available: [date, count, both])'.format(DEFAULT_X_LABEL))
            allow_float: Parameter = Parameter('--allow-float', description='Allow floating points')
            dynamic: Parameter = Parameter('--dynamic', description='Dynamic Fill')
            today: Parameter = Parameter('--today', description='Today')

        operation: Operation = Operation('chart', description='Create Charts', parameter_list=[
            ParameterList.average_range,
            ParameterList.days, 
            ParameterList.dots_count, 
            ParameterList.max_y,
            ParameterList.style, 
            ParameterList.x_label,
            ParameterList.allow_float,
            ParameterList.dynamic,
            ParameterList.today,
        ])
        
    class Reload:
        class ParameterList:
            pass

        operation: Operation = Operation('reload', description='Reload Storage', parameter_list=[])
    
    class Save:
        class ParameterList:
            pass

        operation: Operation = Operation('save', description='Save Storage', parameter_list=[])
    
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
    OperationList.Reload.operation,
    OperationList.Save.operation,
    OperationList.View.operation,
    OperationList.Exit.operation,
]
