"""
    `core/util/format.py`
"""

def path(*path_list: tuple[str]) -> str:
    """ Function: Format path """
    path_list = [p.strip() for p in path_list if p.strip() != str()]
    joined_path = '/'.join([p.strip('/') for p in path_list])

    while '//' in joined_path:
        joined_path = joined_path.replace('//', '/')

    return joined_path
