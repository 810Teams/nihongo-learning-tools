"""
    `progress_tracker/custom/append.py`
"""

from core.util.logging import error


def custom_append_head(data: str, custom_id: int) -> list[int]:
    """ Custom Append Head Function """
    try:
        return eval('custom_append_{}(data)'.format(custom_id))
    except (NameError, SyntaxError):
        error('Invalid custom function error in \'custom_append.py\'.')


def custom_append_1(data: str) -> list[int]:
    """ Custom Append Function #1 """
    data = [[int(j) for j in i.split('-')] for i in data.strip().split(',')]
    return [(i[0] - 1) * 16 + i[1] - 1 for i in data]


def custom_append_2(data: str) -> list[int]:
    """ Custom Append Function #2 """
    # Your custom code here!
    # Don't forget to return calculated value
    pass


def custom_append_3(data: str) -> list[int]:
    """ Custom Append Function #3 """
    # Your custom code here!
    # Don't forget to return calculated value
    pass


def custom_append_4(data: str) -> list[int]:
    """ Custom Append Function #4 """
    # Your custom code here!
    # Don't forget to return calculated value
    pass


def custom_append_5(data: str) -> list[int]:
    """ Custom Append Function #5 """
    # Your custom code here!
    # Don't forget to return calculated value
    pass
