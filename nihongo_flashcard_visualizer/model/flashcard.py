"""
    `nihongo_flashcard_visualizer/error/flashcard_data.py`
"""

from random import choices

from nihongo_flashcard_visualizer.error.flashcard_error import FlashcardError


class Flashcard:
    PROGRESS_DAY_LIST = (1, 2, 3, 7, 14, 21, 30, 60, 90, 180, 270, 360, None)

    def __init__(self, progress: int=0, days: int=None) -> None:
        self.progress: int = progress
        self.days: int = days

        if days == None:
            self.days = Flashcard.PROGRESS_DAY_LIST[progress]

        if not self._validate():
            raise FlashcardError

    def count(self) -> None:
        """ Method: Countdown flashcard next review days by one """
        if self.progress == 12:
            raise FlashcardError

        if self.days >= 1:
            self.days -= 1

    def review(self, correct_p: float=1.0) -> None:
        """ Method: Review flashcard """
        is_correct: bool = choices([False, True], [1 - correct_p, correct_p])[0]

        if self.days == 0 and self.progress < 12:
            if is_correct:
                self.progress += 1
            elif not is_correct and self.progress > 0:
                self.progress -= 1
            self.days = Flashcard.PROGRESS_DAY_LIST[self.progress]
        else:
            raise FlashcardError

    def _validate(self) -> bool:
        """ Private Method: Validate flashcard validity """
        if self.progress < 0 or self.progress >= len(Flashcard.PROGRESS_DAY_LIST):
            # Case: Progress out of range
            return False
        elif self.progress == len(Flashcard.PROGRESS_DAY_LIST) - 1 and self.days is not None:
            # Case: Max progress but days until next review remains
            return False
        elif self.days is not None and self.days > Flashcard.PROGRESS_DAY_LIST[self.progress]:
            # Case: Days until next review exceeds the cap
            return False
        return True
