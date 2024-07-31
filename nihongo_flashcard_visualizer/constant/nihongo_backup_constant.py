"""
    `nihongo_flashcard_visualzer/constant/nihongo_backup_constants.py`
"""

class NihongoBackupConstant:
    TABLE_NAME: str = 'ZFLASHCARD'

    class Columns:
        PROGRESS: str = 'ZPROGRESS'
        STATUS: str = 'ZSTATUSASINT'
        KANJI_TEXT: str = 'ZKANJITEXT'
