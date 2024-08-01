"""
    `main.py`
"""

import os

from core.base.app_base import ApplicationBase
from core.settings import ENABLE_PYCLEAN
from core.util.logging import error
from nihongo_flashcard_visualizer.app.nihongo_flashcard_visualizer_app import NihongoFlashcardVisualizerApplication
from progress_tracker.app.progress_tracker_app import ProgressTrackerApplication


INSTALLED_APPLICATIONS: list[ApplicationBase] = [
    ProgressTrackerApplication('PROGRESS_TRACKER'),
    NihongoFlashcardVisualizerApplication('NIHONGO_FLASHCARD_VISUALIZER'),
]


def main() -> None:
    """ Main function """
    index: int = 0
    try:
        while True:
            INSTALLED_APPLICATIONS[index].setup()
            INSTALLED_APPLICATIONS[index].start()
            index += 1
            index %= len(INSTALLED_APPLICATIONS)
    except Exception:
        error('Unexpected error occured, forcing the application to close.')
        if ENABLE_PYCLEAN:
            print()
            os.system('pyclean .')
            print()


if __name__ == '__main__':
    main()
