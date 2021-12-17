"""
    `src/app_data.py`
"""

from settings import DEFAULT_AVERAGE_RANGE, DEFAULT_DAYS, DEFAULT_DOTS_COUNT, DEFAULT_MAX_Y_LABELS, DEFAULT_STYLE, DEFAULT_X_LABEL
from src.model.operation import Operation
from src.model.parameter import Parameter


APP_NAME = 'Progress Tracker Application'
AUTHOR = '810Teams'
VERSION = 'v2.1.0'

OPERATION_LIST = [
    Operation('append', value_type=str, description='Append Data', parameter_list=[
        Parameter('-custom', value_type=int, description='Custom written method'),
        Parameter('--add', description='Add mode')
    ]),
    Operation('chart', description='Create Charts', parameter_list=[
        Parameter('-average-range', value_type=int, description='Average range (Default: {})'.format(DEFAULT_AVERAGE_RANGE)),
        Parameter('-days', value_type=int, description='Duration in days (Default: {})'.format(DEFAULT_DAYS)),
        Parameter('-dots-count', value_type=int, description='Maximum dot count (Default: {})'.format(DEFAULT_DOTS_COUNT)),
        Parameter('-max-y', value_type=int, description='Maximum y-labels (Default: {})'.format(DEFAULT_MAX_Y_LABELS)),
        Parameter('-style', value_type=str, description='Style (Default: {})'.format(DEFAULT_STYLE)),
        Parameter('-x-label', value_type=str, description='X-label type (Default: {}) (Available: [date, count, both])'.format(DEFAULT_X_LABEL)),
        Parameter('--allow-float', description='Allow floating points'),
        Parameter('--dynamic', description='Dynamic Fill'),
        Parameter('--open', description='Open'),
        Parameter('--open-only', description='Open Only'),
        Parameter('--today', description='Today')
    ]),
    Operation('reload', description='Reload Storage', parameter_list=[]),
    Operation('save', description='Save Storage', parameter_list=[]),
    Operation('view', description='View Storage', parameter_list=[]),
    Operation('exit', description='Exit Application', parameter_list=[]),
]
