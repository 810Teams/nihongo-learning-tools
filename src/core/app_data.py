"""
    `src/app_data.py`
"""

from src.model.operation import Operation
from src.model.parameter import Parameter


APP_NAME = 'Progress Tracker Application'
AUTHOR = '810Teams'
VERSION = 'v2.0.0'

SUPPORTED_STYLES = (
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

OPERATION_LIST = [
    Operation('append', code='a', value_type=str, description='Append Data', parameter_list=[
        Parameter('-add', description='Add mode'),
        Parameter('-cus', value_type=int, description='Custom written method')
    ]),
    Operation('chart', code='c', description='Create Charts', parameter_list=[
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
    Operation('reload', code='r', description='Reload Storage', parameter_list=[]),
    Operation('save', code='s', description='Save Storage', parameter_list=[]),
    Operation('view', code='v', description='View Storage', parameter_list=[
        Parameter('-open', 'Open')
    ]),
    Operation('exit', code='x', description='Exit Application', parameter_list=[]),
]
