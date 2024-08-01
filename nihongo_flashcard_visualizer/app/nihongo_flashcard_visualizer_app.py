"""
    `nihongo_flashcard_visualizer/app/nihongo_flashcard_visualizer_app.py`
"""

from core.base.app_base import ApplicationBase
from nihongo_flashcard_visualizer.constant.app_data import *
from nihongo_flashcard_visualizer.service.operation_service import OperationService


class NihongoFlashcardVisualizerApplication(ApplicationBase):
    def __init__(self) -> None:
        super().__init__(APP_ID)

    def setup(self) -> None:
        """ Method: Verify required folder paths and set up folders if not exist """
        super().setup(folder_path_list=[CHART_BASE_PATH, DATABASE_BASE_PATH])

    def start(self) -> None:
        """ Method: Run the application """
        super()._display_app_title(APP_NAME, AUTHOR, VERSION)
        self.operation_service = OperationService()
        return super().start()
