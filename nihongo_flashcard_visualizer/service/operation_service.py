"""
    `nihongo_flashcard_visualizer/service/operation_service.py`
"""

from core.base.operation_service_base import OperationServiceBase
from core.model.command import Command
from core.util.format import path
from core.util.logging import notice
from core.util.statistics import average, median, standard_dev
from nihongo_flashcard_visualizer.constant.app_data import *
from nihongo_flashcard_visualizer.constant.flashcard_type import FlashcardType
from nihongo_flashcard_visualizer.model.nihongo_backup import NihongoBackup
from nihongo_flashcard_visualizer.service.render_service import RenderService
from nihongo_flashcard_visualizer.settings import *
from nihongo_flashcard_visualizer.util.format import level_format
from nihongo_flashcard_visualizer.util.statistics import progress_coverage


class OperationService(OperationServiceBase):
    def __init__(self) -> None:
        super().__init__(OPERATION_LIST)
        self.render_service: RenderService = RenderService()
        self.nihongo_backup: NihongoBackup = NihongoBackup()

    def _operate_chart(self, command: Command) -> None:
        """ Function: Create Charts """
        parameter_list = OperationList.Chart.ParameterList

        if command.contains_argument(parameter_list.open_only.name):
            notice('Opening chart files.')
            super()._open_file(path(CHART_BASE_PATH, '*'))
            return

        self.render_service.render_all(
            self.nihongo_backup.get_counted_flashcard_progress(),
            days=super()._get_argument_value(command, parameter_list.days),
            incorrect_p=super()._get_argument_value(command, parameter_list.incorrect_probability),
            max_y_labels=super()._get_argument_value(command, parameter_list.max_y),
            no_dot_shrink=not command.contains_argument(parameter_list.no_dot_shrink.name),
            show_correlation=command.contains_argument(parameter_list.show_correlation.name),
            simulation_mode=command.contains_argument(parameter_list.simulation_mode.name),
            style=super()._get_argument_value(command, parameter_list.style)
        )

        if command.contains_argument(parameter_list.open.name):
            notice('Opening chart files.')
            super()._open_file(path(CHART_BASE_PATH, '*'))

    def _operate_extract(self, command: Command) -> None:
        """ Function: Extract Nihongo Database """
        self.nihongo_backup.extract()

    def _operate_stat(self, command: Command) -> None:
        """ Function: View Statistics """
        raw_data: dict[str, list[int]] = self.nihongo_backup.get_uncounted_flashcard_process()

        i = 0
        for flashcard_type in (FlashcardType.WORD, FlashcardType.KANJI):
            print(' - {} Statistics -'.format(flashcard_type.capitalize()))
            print('   Total: {}'.format(len(raw_data[flashcard_type])))
            print('   Median: {}'.format(level_format(median(raw_data[flashcard_type]), initial_level=1, remainder=True)))
            print('   Average: {}'.format(level_format(average(raw_data[flashcard_type]), initial_level=1, remainder=True)))
            print('   Standard Deviation: {}'.format(level_format(standard_dev(raw_data[flashcard_type]), initial_level=0, remainder=True)))
            print('   Progress Coverage: {:.2f}%'.format(progress_coverage(raw_data[flashcard_type]) * 100))

            if i + 1 < 2:
                print()
                i += 1
