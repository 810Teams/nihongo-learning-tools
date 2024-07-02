"""
    `core/util/reader.py`
"""


def convert_csv_to_list(value: str, value_type: type=str, replace_null: str=str()) -> list:
    """ Function: Convert CSV to list """
    converted_list = [i.replace(' ', str()) for i in value.split(',')]

    for i in range(len(converted_list)):
        if (converted_list[i] == str()):
            converted_list[i] = replace_null
        else:
            converted_list[i] = value_type(converted_list[i])

    return converted_list


def contains_row_for_date(data: list, date: str) -> bool:
    """ Function: Verify if row with specified date already exist """
    filtered_data = [i for i in data if i[0] == date]

    return len(filtered_data) > 0


def find_row_by_date(data: list, date: str, use_index: int=-1) -> list:
    """ Function: Find row with specified date """
    filtered_data = [i for i in data if i[0] == date]

    try:
        return filtered_data[use_index]
    except IndexError:
        return None


def is_nan(value) -> bool:
    """ Function: Check if NaN """
    return value != value


def contains_nan(row: list) -> bool:
    """ Function: Check if contains NaN """
    for i in row:
        if is_nan(i):
            return True
    return False


def is_empty(value: any) -> bool:
    """ Function: Check if empty value """
    try:
        return value == str() or value is None or is_nan(value)
    except TypeError:
        return True


def copy_list(value: list) -> list:
    """ Function: Copy list without reference """
    return [i for i in value]
