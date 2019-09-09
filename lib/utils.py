'''
    `utils.py`
    @author 810Teams
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
