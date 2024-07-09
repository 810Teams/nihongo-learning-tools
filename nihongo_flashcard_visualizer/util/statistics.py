"""
    `nihongo_flashcard_visualizer/util/statistics.py`
"""

def progress_coverage(raw_data: list[int]) -> float:
    """ Function: Calculates progress coverage on current learned words """
    raw_data_copy = [i + 3 for i in raw_data]
    return sum(raw_data_copy) / (15 * len(raw_data_copy))
