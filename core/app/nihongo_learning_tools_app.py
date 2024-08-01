"""
    `core/app/nihongo_learning_tools_app.py`
"""

import os

from core.base.app_base import ApplicationBase
from core.service.cache_service import CacheService
from core.settings import ENABLE_PYCLEAN
from core.util.logging import error
from nihongo_flashcard_visualizer.app.nihongo_flashcard_visualizer_app import NihongoFlashcardVisualizerApplication
from progress_tracker.app.progress_tracker_app import ProgressTrackerApplication


class NihongoLearningToolsApplication:
    def __init__(self) -> None:
        self.cache_service: CacheService = CacheService()
        self.installed_applications: list[ApplicationBase] = [
            ProgressTrackerApplication(),
            NihongoFlashcardVisualizerApplication(),
        ]

    def start(self) -> None:
        index: int = self._get_app_index(self.cache_service.get_last_used_app())

        try:
            while True:
                self.cache_service.set_last_used_app(self.installed_applications[index].application_id)
                self.installed_applications[index].setup()
                self.installed_applications[index].start()
                index = (index + 1) % len(self.installed_applications)

        except Exception:
            error('Unexpected error occured, forcing the application to close.')
            if ENABLE_PYCLEAN:
                print()
                os.system('pyclean .')
                exit()

    def _get_app_index(self, application_id: str) -> int:
        for i in range(len(self.installed_applications)):
            if self.installed_applications[i].application_id == application_id:
                return i
        return 0
