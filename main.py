"""
    `main.py`
"""

from core.base.app import ApplicationBase
from progress_tracker.app import ProgressTrackerApplication


def main() -> None:
    """ Main function """
    application: ApplicationBase = ProgressTrackerApplication()
    application.setup()
    application.run()


if __name__ == '__main__':
    main()
