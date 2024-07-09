"""
    `core/util/logging.py`
"""

def error(*messages: tuple[str], end: str='\n', sep: str=' ', display: bool=True) -> None:
    """ Display error message """
    _title_print('ERROR', messages=messages, end=end, sep=sep, display=display)


def log(*messages: tuple[str], end: str='\n', sep: str=' ', display: bool=True) -> None:
    """ Display log message """
    _title_print('LOG', messages=messages, end=end, sep=sep, display=display)


def notice(*messages: tuple[str], end: str='\n', sep: str=' ', display: bool=True) -> None:
    """ Display notice message """
    _title_print('NOTICE', messages=messages, end=end, sep=sep, display=display)


def _title_print(title: str, messages: tuple[str], end: str='\n', sep: str=' ', display: bool=True) -> None:
    if display:
        print('[{}]'.format(title), sep.join(messages), end=end)
