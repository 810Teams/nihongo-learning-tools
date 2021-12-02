"""
    `custom/append.py`
"""

from src.util.logging import error


def custom_append_head(data, custom_id):
    """ Custom Append Head Function """
    try:
        return eval('custom_append_{}(data)'.format(custom_id))
    except (NameError, SyntaxError):
        error('Invalid custom function error in \'custom_append.py\'.')


def custom_append_1(data):
    """ Custom Append Function #1 """
    data = [[int(j) for j in i.split()] for i in data.strip().split(',')]
    return [(i[0] - 1) * 16 + i[1] - 1 for i in data]


def custom_append_2(data):
    """ Custom Append Function #2 """
    # Your custom code here!
    # Don't forget to return calculated value


def custom_append_3(data):
    """ Custom Append Function #3 """
    # Your custom code here!
    # Don't forget to return calculated value


def custom_append_4(data):
    """ Custom Append Function #4 """
    # Your custom code here!
    # Don't forget to return calculated value


def custom_append_5(data):
    """ Custom Append Function #5 """
    # Your custom code here!
    # Don't forget to return calculated value
