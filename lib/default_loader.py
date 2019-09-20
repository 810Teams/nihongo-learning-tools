'''
    `default_loader.py`
    @author 810Teams
'''


def load_default_storage():
    ''' Function: Load default storage '''
    try:
        name = list(open('DEFAULT_STORAGE.txt'))[0].replace('\n', '').strip()
        return name
    except FileNotFoundError:
        return None


def load_default_style():
    ''' Function: Load default style '''
    try:
        name = [i.replace('\n', '').strip()
                for i in list(open('DEFAULT_STYLE.txt'))][0]
        return name
    except FileNotFoundError:
        return None
