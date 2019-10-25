'''
    `custom_append.py`
'''

from src.utils import error


def custom_append_head(args, custom_id):
    ''' Custom Append Head Function '''
    try:
        return eval('custom_append_{}(args)'.format(custom_id))
    except (NameError, SyntaxError):
        error('Invalid custom function error in \'custom_append.py\'.')


def custom_append_1(args):
    ''' Custom Append Function #1 '''
    return (args[0] - 1) * 16 + args[1] - 1


def custom_append_2(args):
    ''' Custom Append Function #2 '''
    # Your custom code here!
    # Don't forget to return calculated value


def custom_append_3(args):
    ''' Custom Append Function #3 '''
    # Your custom code here!
    # Don't forget to return calculated value


def custom_append_4(args):
    ''' Custom Append Function #4 '''
    # Your custom code here!
    # Don't forget to return calculated value


def custom_append_5(args):
    ''' Custom Append Function #5 '''
    # Your custom code here!
    # Don't forget to return calculated value

