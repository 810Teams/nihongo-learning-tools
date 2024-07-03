"""
    `nihongo_flashcard_visualizer/settings.py`
"""

# Style Settings

DEFAULT_STYLE = 'DarkStyle'

# Nihongo Database Settings

NIHONGO_BACKUP_PATH = '/Users/teerapat/Library/Mobile Documents/com~apple~CloudDocs/Documents/Backups/Nihongo Backups/'

# Chart Settings

DEFAULT_DAYS = 90
DEFAULT_INCORRECT_PROBABILITY = 0.05
DEFAULT_MAX_Y_LABELS = 15
LEARN_PATTERN_LIST = [
    ('Never Study', [0]),
    ('10 Per Day', [10]),
    ('20 Per Day', [20]),
]
