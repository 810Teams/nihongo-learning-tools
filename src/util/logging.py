"""
    `src/util/logging.py`
"""


from settings import SHOW_LOGS


def error(message, end='\n', start=str()):
    """ Display error message """
    if SHOW_LOGS:
        print(start, end=str())
        print('[ERROR]', message, end=end)


def log(message, end='\n', start=str()):
    """ Display log message """
    if SHOW_LOGS:
        print(start, end=str())
        print('[LOG]', message, end=end)


def notice(message, end='\n', start=str()):
    """ Display notice message """
    if SHOW_LOGS:
        print(start, end=str())
        print('[NOTICE]', message, end=end)
