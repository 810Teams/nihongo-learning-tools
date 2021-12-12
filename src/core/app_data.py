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
    Operation('append', value_type=str, description='Append Data', parameter_list=[
        Parameter('-custom', value_type=int, description='Custom written method'),
        Parameter('--add', description='Add mode')
    ]),
    Operation('chart', description='Create Charts', parameter_list=[
        Parameter('-average-range', value_type=int, description='Average (Default: All)'),
        Parameter('-days', value_type=int, description='Duration (Default: All)'),
        Parameter('-dots-count', value_type=int, description='Maximum dot count (Default: 101)'),
        Parameter('-max-y', value_type=int, description='Maximum y-labels (Default: 15)'),
        Parameter('-style', value_type=str, description='Style'),
        Parameter('-x-label', value_type=str, description='X-label type (Default: date) (Available: [date,count,both])'),
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
