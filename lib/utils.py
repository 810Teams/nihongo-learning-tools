'''
    `utils.py`
'''


def error(message):
    ''' Display error message '''
    print('[ERROR]', message)


def log(message):
    ''' Display log message '''
    print('[LOG]', message)


def notice(message):
    ''' Display notice message '''
    print('[NOTICE]', message)


def kanji_calculate(current_page, current_line):
    ''' Function: Calculate total learned kanjis from current page and line of Notability app '''
    return (current_page - 1) * 16 + current_line - 1


def average(data):
    ''' Function: Returns average value of the list '''
    return sum(data)/len(data)
