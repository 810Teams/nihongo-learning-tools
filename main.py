"""
    `main.py`
"""

import os

from core.util.logging import error
from core.settings import INSTALLED_APPLICATIONS
from settings import ENABLE_PYCLEAN


def main() -> None:
    """ Main function """
    index: int = 0
    try:
        while True:
            INSTALLED_APPLICATIONS[index].setup()
            INSTALLED_APPLICATIONS[index].start()
            index += 1
            index %= len(INSTALLED_APPLICATIONS)
    except RuntimeError:
        print()
        error('Unexpected error occured, forcing the application to close.')
        error('Please contact application developer for further investigation.')
        if ENABLE_PYCLEAN:
            print()
            os.system('pyclean .')
            print()


if __name__ == '__main__':
    main()
