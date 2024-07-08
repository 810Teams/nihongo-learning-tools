"""
    `main.py`
"""

from core.settings import INSTALLED_APPLICATIONS


def main() -> None:
    """ Main function """
    index: int = 0
    while True:
        INSTALLED_APPLICATIONS[index].start()
        index += 1
        index %= len(INSTALLED_APPLICATIONS)


if __name__ == '__main__':
    main()
