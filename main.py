"""
    `main.py`
"""

from core.app.nihongo_learning_tools_app import NihongoLearningToolsApplication


def main() -> None:
    """ Main function """
    app: NihongoLearningToolsApplication = NihongoLearningToolsApplication()
    app.start()


if __name__ == '__main__':
    main()
