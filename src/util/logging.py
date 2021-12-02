"""
    `src/util/logging.py`
"""


from settings import SHOW_LOGS


def error(message, end='\n'):
    """ Display error message """
    if SHOW_LOGS:
        print('[ERROR]', message, end=end)


def log(message, end='\n'):
    """ Display log message """
    if SHOW_LOGS:
        print('[LOG]', message, end=end)


def notice(message, end='\n'):
    """ Display notice message """
    if SHOW_LOGS:
        print('[NOTICE]', message, end=end)
