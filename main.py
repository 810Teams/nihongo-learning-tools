"""
    `main.py`
"""

from progress_tracker.app import ProgressTrackerApplication


def main() -> None:
    """ Main function """
    application = ProgressTrackerApplication()
    application.setup()
    application.run()


main()
