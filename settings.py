"""
    `settings.py`
"""


# Storage Settings

DEFAULT_STORAGE = 'kanji'


# Style Settings

DEFAULT_AVERAGE_RANGE = None
DEFAULT_DAYS = 0
DEFAULT_DOTS_COUNT = 101
DEFAULT_MAX_Y_LABELS = 15
DEFAULT_STYLE = 'DarkStyle'
DEFAULT_X_LABEL = 'date'

BASE_DOTS_SIZE = 2.25
MAX_DOTS_SIZE_RETAIN = 45
SHRINK_FACTOR = 2.5


# Backup Settings

ENABLE_BACKUP = True
BACKUP_PATH_LIST = [
    'C:/Users/teera/iCloudDrive/Documents/Dataset Backups/',
    '/Users/teerapat/Library/Mobile Documents/com~apple~CloudDocs/Documents/Backups/Dataset Backups/',
]
BACKUP_TO_ONLY_FIRST_PATH = False
LOAD_BACKUP_PATH_LIST = [
    'C:/Users/teera/iCloudDrive/Documents/Dataset Backups/',
    '/Users/teerapat/Library/Mobile Documents/com~apple~CloudDocs/Documents/Backups/Dataset Backups/',
]
