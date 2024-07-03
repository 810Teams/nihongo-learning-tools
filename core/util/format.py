"""
    `core/util/format.py`
"""

def path(*path_segment_list: tuple[str]) -> str:
    """ Function: Format path """
    path_segment_list: list[str] = [segment.strip() for segment in path_segment_list if segment.strip() != str()]
    joined_path: str = '/'.join(path_segment_list)

    while '//' in joined_path:
        joined_path = joined_path.replace('//', '/')

    return joined_path
