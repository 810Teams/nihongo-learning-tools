"""
    `core/settings.py`
"""

from core.base.app_base import ApplicationBase
from nihongo_flashcard_visualizer.app.nihongo_flashcard_visualizer_app import NihongoFlashcardVisualizerApplication
from progress_tracker.app.progress_tracker_app import ProgressTrackerApplication

# Application Settings

INSTALLED_APPLICATIONS: list[ApplicationBase] = [
    ProgressTrackerApplication(),
    NihongoFlashcardVisualizerApplication(),
]
