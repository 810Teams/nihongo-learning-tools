'''
    `utils.py`
'''


def error(message, show=True, end='\n'):
    ''' Display error message '''
    if show:
        print('[ERROR]', message, end=end)


def log(message, show=True, end='\n'):
    ''' Display log message '''
    if show:
        print('[LOG]', message, end=end)


def notice(message, show=True, end='\n'):
    ''' Display notice message '''
    if show:
        print('[NOTICE]', message, end=end)


def kanji_calculate(current_page, current_line):
    ''' Function: Calculate total learned kanjis from current page and line of Notability app '''
    return (current_page - 1) * 16 + current_line - 1


def average(data):
    ''' Function: Returns average value of the list '''
    return sum(data)/len(data)
