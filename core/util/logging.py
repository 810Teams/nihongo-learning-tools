"""
    `core/util/logging.py`
"""


def error(message: str, end: str='\n', start: str=str(), display: bool=True) -> None:
    """ Display error message """
    if display:
        print(start, end=str())
        print('[ERROR]', message, end=end)


def log(message: str, end: str='\n', start: str=str(), display: bool=True) -> None:
    """ Display log message """
    if display:
        print(start, end=str())
        print('[LOG]', message, end=end)


def notice(message: str, end: str='\n', start: str=str(), display: bool=True) -> None:
    """ Display notice message """
    if display:
        print(start, end=str())
        print('[NOTICE]', message, end=end)
