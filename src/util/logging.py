"""
    `src/util/logging.py`
"""


def error(message: str, end: str='\n', start: str=str()) -> None:
    """ Display error message """
    print(start, end=str())
    print('[ERROR]', message, end=end)


def log(message: str, end: str='\n', start: str=str()) -> None:
    """ Display log message """
    print(start, end=str())
    print('[LOG]', message, end=end)


def notice(message: str, end: str='\n', start: str=str()) -> None:
    """ Display notice message """
    print(start, end=str())
    print('[NOTICE]', message, end=end)
