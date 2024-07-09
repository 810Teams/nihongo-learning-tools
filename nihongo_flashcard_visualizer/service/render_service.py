"""
    `nihongo_flashcard_visualizer/service/render_service.py`
"""

import numpy
import pygal

from math import ceil, floor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from time import perf_counter

from core.base.render_service_base import RenderServiceBase
from core.util.format import path
from core.util.logging import notice
from core.util.reader import copy_list
from nihongo_flashcard_visualizer.constant.app_data import *
from nihongo_flashcard_visualizer.constant.estimated_progress_type import EstimatedProgressType
from nihongo_flashcard_visualizer.constant.flashcard_type import FlashcardType
from nihongo_flashcard_visualizer.model.flashcard import Flashcard
from nihongo_flashcard_visualizer.settings import *


class RenderService(RenderServiceBase):
    def __init__(self) -> None:
        super().__init__()

    def render_all(
        self,
        data: dict,
        days: int=60,
        no_dot_shrink: bool=True,
        incorrect_p: float=0.0,
        max_y_labels: int=15,
        show_correlation: bool=False,
        simulation_mode: bool=False,
        style: str=DEFAULT_STYLE
    ) -> None:
        """ Function: Renders the chart """
        time_start: float = perf_counter()

        self._render_by_level(data, days=days, max_y_labels=max_y_labels, simulation_mode=simulation_mode, style=self._get_style(style))
        self._render_estimated(data, days=days, no_dot_shrink=no_dot_shrink, incorrect_p=incorrect_p, max_y_labels=max_y_labels, show_correlation=show_correlation, simulation_mode=simulation_mode, style=self._get_style(style))
        self._render_progress(data, days=days, simulation_mode=simulation_mode, style=self._get_style(style))

        notice('Total time spent rendering charts is {:.2f} seconds.'.format(perf_counter() - time_start))

    def _render_by_level(
            self,
            data: dict[str, list],
            days: int=60,
            max_y_labels: int=15,
            simulation_mode: bool=False,
            style: str=DEFAULT_STYLE
        ):
        """ Function: Renders the words and kanji by level chart """
        chart: pygal.HorizontalStackedBar = pygal.HorizontalStackedBar()

        # Chart Data
        data_word = [i for i in data[FlashcardType.WORD]]
        data_kanji = [i for i in data[FlashcardType.KANJI]]
        if simulation_mode:
            data_word = self._get_estimated([0 for _ in range(13)], days=days, learn_pattern=[10], result=EstimatedProgressType.VOCABULARY)[-1]

        chart.add('Words', [{'value': i, 'label': '{:.2f}%'.format(i / (sum(data_word) + (sum(data_word) == 0)) * 100)} for i in data_word])
        chart.add('Kanjis', [{'value': i, 'label': '{:.2f}%'.format(i / (sum(data_kanji) + (sum(data_kanji) == 0)) * 100)} for i in data_kanji])

        # Chart Titles
        chart.title = 'Learned Words & Kanjis by Level'

        # Chart Labels
        chart.x_labels = ['{}-{}'.format(i // 3 + 1, i % 3) for i in range(len(data_word))]
        chart.y_labels = self._get_y_labels(0, max(data[FlashcardType.ANY]), max_y_labels=max_y_labels)

        # Chart Legends
        chart.show_legend = True
        chart.legend_at_bottom = False
        chart.legend_box_size = 15

        # Chart Render
        chart.style = style
        chart.render_to_file(path(CHART_BASE_PATH, 'by_level' + CHART_FILE_EXTENSION))

        # Notice
        self._notice_chart_export('by_level')

    def _render_estimated(
        self,
        data: dict,
        days: int=60,
        no_dot_shrink: bool=True,
        incorrect_p: float=0.0,
        max_y_labels: int=15,
        show_correlation: bool=False,
        simulation_mode: bool=False,
        style: str=DEFAULT_STYLE
    ):
        """ Function: Renders the estimated flashcards per day chart """
        chart: pygal.Line = pygal.Line()

        # Chart Data
        data_copy = [i for i in data[FlashcardType.ANY]]
        if simulation_mode:
            data_copy = [0 for _ in range(13)]

        estimated_list = list()

        for i, j in LEARN_PATTERN_LIST:
            estimated_list.append([sum(k) for k in self._get_estimated(data_copy, days=days, incorrect_p=incorrect_p, learn_pattern=j, result=EstimatedProgressType.REVIEW)])
            chart.add(i, [None] + estimated_list[-1], allow_interruptions=True, stroke=True)

        # Correlation
        for i in range(len(estimated_list) * show_correlation):
            x = numpy.array([[j] for j in range(1, len(estimated_list[i]) + 1)])
            y = numpy.array(estimated_list[i])

            poly_f = PolynomialFeatures(degree = 3)
            x = poly_f.fit_transform(x)

            regressor = LinearRegression()
            regressor.fit(x, y)

            chart.add('Correllation-{}'.format(LEARN_PATTERN_LIST[i][0].split()[0]), [None] + regressor.predict(x).tolist(), stroke_style={'width': 5}, show_dots=False)

        # Chart Titles
        chart.title = 'Estimated Flashcards Per Day'
        chart.x_title = 'Days'

        # Chart Labels
        chart.x_labels = [i for i in range(0, days + 1)]
        chart.x_labels_major_count = 8
        chart.show_minor_x_labels = False

        chart.y_labels = self._get_y_labels(
            min([min([j for j in i]) for i in estimated_list]),
            max([max([j for j in i]) for i in estimated_list]),
            max_y_labels=max_y_labels,
            skip=True
        )

        chart.truncate_label = -1

        # Chart Legends
        chart.show_legend = True
        chart.legend_at_bottom = True
        chart.legend_box_size = 15

        # Chart Render
        chart.style = style
        chart.dots_size = 2.5

        if no_dot_shrink:
            bp = 60     # Data amount which dots started shrinking
            factor = 3  # Closer to 1, slower the dots shart shinking. If at 1, dots will never shrink.
            chart.dots_size = 2.5 * ((bp + max(0, days - bp) / factor) / max(bp, days))

        chart.render_to_file(path(CHART_BASE_PATH, 'estimated' + CHART_FILE_EXTENSION))

        # Notice
        self._notice_chart_export('estimated')

    def _render_progress(self, data: dict, days: int=DEFAULT_DAYS, simulation_mode: bool=False, style: str=DEFAULT_STYLE):
        """ Function: Renders the progress chart """
        chart: pygal.Histogram = pygal.Histogram()

        # Chart Data
        data_copy = [i for i in data['word']]
        if simulation_mode:
            data_copy = self._get_estimated([0 for _ in range(13)], days=days, learn_pattern=[10], result=EstimatedProgressType.VOCABULARY)[-1]

        for i in range(0, 13, 3):
            chart.add(
                'Level {:.0f}'.format(i//3 + 1),
                [{
                    'value': (round((i + j) / 3 + 1, 2), sum(data_copy[:i + j + 1]) - data_copy[i + j], sum(data_copy[:i + j + 1])),
                    'label': '{:.2f}%'.format(data_copy[i + j] / (sum(data_copy) + (sum(data_copy) == 0)) * 100)
                } for j in range(len(data_copy[i:i + 3]))],
                formatter=lambda x: '{}'.format(x[2] - x[1])
            )

        # Chart Titles
        chart.title = 'Word Progress'
        chart.x_title = 'Words'

        # Chart Labels
        chart.x_labels = range(1, sum(data_copy) + 1)
        chart.x_labels_major_count = 8
        chart.show_minor_x_labels = False
        chart.y_labels = [0, 1, 2, 3, 4, 5]
        chart.truncate_label = -1

        # Chart Legends
        chart.show_legend = True
        chart.legend_at_bottom = False
        chart.legend_box_size = 15

        # Chart Render
        chart.style = style
        chart.dots_size = 2
        chart.render_to_file(path(CHART_BASE_PATH, 'progress' + CHART_FILE_EXTENSION))

        # Notice
        self._notice_chart_export('progress')

    def _get_y_labels( self, data_min: float, data_max: float, max_y_labels: int=DEFAULT_MAX_Y_LABELS, skip: bool=False) -> list[int]:
        """ Function: Calculates y labels of the chart """
        data_min = floor(data_min)
        data_max = ceil(data_max)

        preset = 1, 2, 5

        if not skip:
            data_range = list(range(0, data_min - 1, -1)) + list(range(0, data_max + 1, 1))
            i = 0

            while len(data_range) > max_y_labels:
                data_range = list(range(0, data_min - preset[i % 3] * 10 ** (i // 3), -1 * preset[i % 3] * 10 ** (i // 3)))
                data_range += list(range(0, data_max + preset[i % 3] * 10 ** (i // 3), preset[i % 3] * 10 ** (i // 3)))
                i += 1
        else:
            data_min = int(data_min/10) * 10
            data_range = list(range(data_min, data_max + 1, 1))
            i = 0

            while len(data_range) > max_y_labels:
                data_range = list(range(data_min, data_max + preset[i % 3] * 10 ** (i // 3), preset[i % 3] * 10 ** (i // 3)))
                i += 1

        data_range.sort()

        return data_range

    def _progress_coverage(self, progress_data: list[int]) -> float:
        """ Function: Calculates progress coverage on current learned words """
        progress_data_copy: list[int] = [i + 3 for i in progress_data]

        return sum(progress_data_copy) / (15 * len(progress_data_copy))

    def _get_estimated(
        self,
        data: list[int],
        days: int=DEFAULT_DAYS,
        incorrect_p: float=DEFAULT_INCORRECT_PROBABILITY,
        learn_pattern: list[int]=[0],
        result: str=EstimatedProgressType.REVIEW
    ) -> list[list[int]]:
        """ Function: Calculates estimated flashcards per day """
        # Step 1: Data preparation
        data_copy: list[int] = copy_list(data) + (13 - len(data)) * [0]
        review_list: list[list[int]] = list()
        vocab_list: list[list[int]] = list()
        flashcard_list: list[Flashcard] = list()

        # Step 2: Data generation
        for i in range(len(data_copy)):
            for j in range(data_copy[i]):
                if Flashcard.PROGRESS_DAY_LIST[i] is not None:
                    flashcard_list.append(Flashcard(progress=i, days=ceil(Flashcard.PROGRESS_DAY_LIST[i] - Flashcard.PROGRESS_DAY_LIST[i]/data_copy[i] * j)))
                else:
                    flashcard_list.append(Flashcard(progress=i, days=None))

        # Step 3: Iteration (Days)
        for i in range(days):
            # Step 3.1
            review_list.append([0 for _ in range(12)])

            # Step 3.2
            for j in range(len(flashcard_list)):
                if flashcard_list[j].progress < 12:
                    flashcard_list[j].count()

            # Step 3.3
            for j in range(len(flashcard_list)):
                if flashcard_list[j].days == 0:
                    review_list[-1][flashcard_list[j].progress] += 1
                    flashcard_list[j].review(correct_p=1 - incorrect_p)

            # Step 3.4
            for i in range(learn_pattern[i % len(learn_pattern)]):
                flashcard_list.append(Flashcard(progress=0))

            # Step 3.5
            if result == EstimatedProgressType.VOCABULARY:
                vocab_list.append([[k.progress for k in flashcard_list].count(j) for j in range(13)])

        # Step 4: Return
        if result == EstimatedProgressType.REVIEW:
            return review_list
        elif result == EstimatedProgressType.VOCABULARY:
            return vocab_list
