"""
    `progress_tracker/service/render_service.py`
"""

import pygal

from datetime import datetime
from math import ceil, floor
from time import perf_counter
from typing import Any

from core.base.render_service_base import RenderServiceBase
from core.util.format import path
from core.util.statistics import average
from core.util.logging import error, notice
from core.util.reader import copy_list
from core.util.validation import is_valid_style
from progress_tracker.constant.app_data import CHART_BASE_PATH, CHART_FILE_EXTENSION
from progress_tracker.model.storage import Storage
from progress_tracker.settings import *
from progress_tracker.util.calculation import add_day_to_date, compare_date
from progress_tracker.util.reader import contains_row_for_date, is_empty
from progress_tracker.util.transform import transpose


class RenderService(RenderServiceBase):
    def __init__(self, storage: Storage) -> None:
        self.storage: Storage = storage
        self.CHART_TYPE_LIST: list[str] = [
            'total default',
            'total stacked',
            'rate default',
            'rate stacked',
            'rate default average',
            'rate stacked average'
        ]

    def render_all(
        self,
        average_range: int=DEFAULT_AVERAGE_RANGE,
        days: int=DEFAULT_DAYS,
        dots_count: int=DEFAULT_DOTS_COUNT,
        max_y_labels: int=DEFAULT_MAX_Y_LABELS,
        style: str=DEFAULT_STYLE,
        x_label: str=DEFAULT_X_LABEL,
        allow_float: bool=False,
        is_dynamic: bool=False,
        is_today: bool=False,
    ) -> None:
        """ Method: Analysis """
        # Data Preparation
        data[list[list[Any]]] = self.storage.to_list()
        data = self._clean(data)
        data = self._fill_missing_data(data, is_dynamic=is_dynamic, is_today=is_today)

        # Arguments Validation (Pre-slice)
        if not self._validate_arguments_pre_slice(data, days=days, max_y_labels=max_y_labels, style=style, x_label=x_label):
            error('Aborting chart creation process.')
            return

        # Slice Data
        data = self._slice_data(data, days=days)

        # Arguments Manipulation
        dots_count = min(dots_count, len(data))
        if ceil(len(data)/2) < dots_count < len(data):
            dots_count = ceil(len(data)/2)
            notice('Dots count value is automatically set to {} to allow better-looking charts.'.format(dots_count), end=str())

        # Arguments Validation (Post-slice)
        if not self._validate_arguments_post_slice(data, average_range=average_range, dots_count=dots_count):
            error('Aborting chart creation process.')
            return

        # Rendering
        time_start = perf_counter()

        self._render_chart_total(data, allow_float=allow_float, max_y_labels=max_y_labels, style=style)
        for chart_type in self.CHART_TYPE_LIST:
            self._render_chart_development(
                data,
                allow_float=allow_float,
                average_range=average_range,
                chart_type=chart_type,
                dots_count=dots_count,
                max_y_labels=max_y_labels,
                style=style,
                x_label=x_label
            )

        notice('Total time spent rendering charts is {:.2f} seconds.'.format(perf_counter() - time_start))

    def _clean(self, data: list[list[Any]]) -> list[list[Any]]:
        """ Method: Clean Data """
        # Step 1 - Sort
        data.sort(key=lambda i: i[0])

        # Step 2 - Date Formatting
        data = [[i[0].split()[0]] + i[1:] for i in data]

        # Step 3 - Remove Date Duplications
        data = [data[i] for i in range(len(data) - 1) if data[i][0] != data[i + 1][0]] + [data[-1]]

        # Step 4 - Return
        return data

    def _fill_missing_data(self, data: list[list[Any]], is_dynamic: bool=False, is_today: bool=False) -> list[list[Any]]:
        """ Method: Fill missing data """
        # Step 1: Prepare data
        data_new = copy_list(data)
        data_new.sort(key=lambda i: i[0])

        # Step 2: Add empty rows for missing dates
        target_date: str = data_new[0][0]
        end_date: str = data_new[-1][0]

        while target_date != end_date:
            if not contains_row_for_date(data_new, target_date):
                data_new.append([target_date] + [None for _ in range(len(data_new[0]) - 1)])
            target_date = add_day_to_date(target_date, days=1)

        data_new.sort(key=lambda i: i[0])

        # Step 3: Fill for each column
        for col in range(1, len(data[0])):
            column_transpose = [i[col] for i in data_new]
            column_transpose = self._fill_missing_data_in_column(column_transpose, is_dynamic=is_dynamic)

            for i in range(len(column_transpose)):
                data_new[i][col] = column_transpose[i]

        # Step 4: Fill until today based on the most recent data
        if is_today:
            data_new = self._today_fill(data_new)

        # Step 5: Return
        return data_new

    def _fill_missing_data_in_column(self, data: list[list[Any]], is_dynamic: bool=False) -> list[list[Any]]:
        # Step 1: Determine missing indexes, store in groups
        missing_index_list: list[list[Any]] = [list()]

        for i in range(len(data)):
            if is_empty(data[i]):
                missing_index_list[-1].append(i)
            elif len(missing_index_list[-1]) > 0:
                missing_index_list.append(list())

        if len(missing_index_list[-1]) == 0:
            missing_index_list = missing_index_list[:-1]

        # Step 2: Fill
        filled_data = copy_list(data)

        for group in missing_index_list:
            start = group[0] - 1
            end = group[-1] + 1

            difference = (filled_data[end] - filled_data[start])
            increment = difference / (len(group) + 1)

            for index in range(len(group)):
                if is_dynamic:
                    filled_data[group[index]] = int(filled_data[start] + index * increment)
                else:
                    filled_data[group[index]] = filled_data[group[0] - 1]

        # Step 3: Return
        return filled_data

    def _today_fill(self, data: list[list[Any]]) -> list[list[Any]]:
        """ Method: Fill date until today """
        data_copy = [i for i in data]
        today = str(datetime.now().date())
        most_recent_date = lambda: data_copy[-1][0].split()[0]

        while compare_date(today, most_recent_date()) > 0:
            data_last_row = [i for i in data_copy[-1]]
            data_last_row[0] = add_day_to_date(data_last_row[0], days=1)
            data_copy.append(data_last_row)

        return data_copy

    def _validate_arguments_pre_slice(
        self,
        data: list[list[Any]],
        days: int=DEFAULT_DAYS,
        max_y_labels: int=DEFAULT_MAX_Y_LABELS,
        style: str=DEFAULT_STYLE,
        x_label: str=DEFAULT_X_LABEL
    ) -> bool:
        """ Method: Validates arguments which depends on the length of cleaned and filled data """
        # -days argument
        if not (-len(data) + 2 <= days <= len(data) and days not in (1, 2)):
            error('Days count must be an integer from {} to {}, and not 1 or 2.'.format(-len(data) + 2, len(data)))
            return False

        # -max-y-labels
        if not (max_y_labels >= 2):
            error('Maximum y labels must be an integer at least 2.')
            return False

        # -style argument
        if not is_valid_style(style):
            error('Invalid chart style.')
            return False

        # -x-label argument
        if x_label not in ('date', 'count', 'both'):
            error('X-label type must be either \'date\', \'count\', or \'both\'')
            return False

        return True

    def _slice_data(self, data: list[list[Any]], days: int=DEFAULT_DAYS) -> list[list[Any]]:
        """ Method: Slice data based on days count """
        return data[-1 * days:]

    def _validate_arguments_post_slice(self, data: list[list[Any]], average_range: int=DEFAULT_AVERAGE_RANGE, dots_count: int=DEFAULT_DOTS_COUNT) -> bool:
        """ Method: Validates arguments which depends on the length of sliced data """
        # -average argument
        if average_range != None and not (1 <= average_range <= len(data) - 1):
            error('Average range must be an integer from {} to {}.'.format(1, len(data) - 1))
            return False

        # -dots-count argument
        if not ((0 <= dots_count) and dots_count != 1):
            error('Dots count must be an integer at least {}, and not {}.'.format(0, 1))
            return False

        return True

    def _render_chart_total(self, data: list[list[Any]], max_y_labels: int=DEFAULT_MAX_Y_LABELS, style: str=DEFAULT_STYLE, allow_float: bool=False) -> None:
        """ Method: Total Analysis """
        chart = pygal.Bar()

        # Chart Data
        for i in range(len(self.storage.get_columns())):
            chart.add(self.storage.get_columns()[i], data[-1][i + 1])

        # Chart Titles
        chart.title = '{} Totals'.format(self.storage.name.capitalize())
        chart.y_title = 'Amount'

        # Chart Labels
        chart.y_labels = self._calculate_y_labels(
            min([min([j for j in i[1:]]) for i in data]),
            max([max([j for j in i[1:]]) for i in data]),
            allow_float=allow_float,
            max_y_labels=max_y_labels
        )

        # Chart Legends
        chart.legend_at_bottom = True
        chart.legend_at_bottom_columns = 6
        chart.legend_box_size = 16

        # Chart Render
        chart.style = self._get_style(style)
        chart.render_to_file(path(CHART_BASE_PATH, self.storage.name.lower() + '_total' + CHART_FILE_EXTENSION))

        # Notice
        self._notice_chart_export(self.storage.name.lower() + '_total')

    def _render_chart_development(
        self,
        data: list[list[Any]],
        chart_type: str='total default',
        average_range: int=DEFAULT_AVERAGE_RANGE,
        dots_count: int=DEFAULT_DOTS_COUNT,
        max_y_labels: int=DEFAULT_MAX_Y_LABELS,
        style: str=DEFAULT_STYLE,
        x_label: str=DEFAULT_X_LABEL,
        allow_float: bool=False,
    ) -> None:
        """ Method: Development Analysis """
        # Chart Type Check
        if chart_type not in self.CHART_TYPE_LIST:
            error('Invalid chart type found. Aborting chart creation process.')
            return

        # Chart Initiation
        if 'default' in chart_type:
            chart = pygal.Line()
        elif 'stacked' in chart_type:
            chart = pygal.StackedLine()

        # Chart Data
        columns = self.storage.get_columns()

        if 'total' in chart_type:
            for i in range(len(columns)):
                chart.add(
                    columns[i],
                    self._get_dot_data_list(transpose(data)[1:][i], dots_count=dots_count),
                    force_visible=False
                )

        elif 'rate' in chart_type:
            data_rate = [[data[i][j] - data[i - 1][j] for i in range(1, len(data))] for j in range(1, len(columns) + 1)]

            if 'average' not in chart_type:
                for i in range(len(columns)):
                    chart.add(
                        columns[i],
                        self._get_dot_data_list(data_rate[i], dots_count=dots_count, force_visible=True)
                    )
            else:
                data_average = list()
                for i in range(len(columns)):
                    temp = list()

                    for j in range(len(data_rate[i])):
                        if average_range == None:
                            temp.append(round(average(data_rate[i][0:j + 1]), 2))
                        elif 1 <= average_range <= len(data_rate[i]):
                            if j < average_range:
                                temp.append(round(average(data_rate[i][0:j + 1]), 2))
                            elif average_range <= j:
                                temp.append(round(average(data_rate[i][j - average_range + 1:j + 1]), 2))

                    chart.add(
                        columns[i],
                        self._get_dot_data_list(temp, dots_count=dots_count, force_visible=False)
                    )
                    data_average.append(temp)

        # Chart Titles
        chart.title = '{} Development'.format(self.storage.name.capitalize())

        if 'rate' in chart_type:
            chart.title += ' Rate'
        if 'stacked' in chart_type:
            chart.title += ' (Stacked)'
        if 'average' in chart_type:
            chart.title = chart.title.replace(' Development', ' Average Development')

        chart.x_title = 'Date'
        chart.y_title = 'Amount'

        # Chart Labels
        if x_label == 'date':
            if 'total' in chart_type:
                chart.x_labels = [i[0] for i in data]
            elif 'rate' in chart_type:
                chart.x_labels = [i[0] for i in data[1:]]
        elif x_label == 'count':
            if 'total' in chart_type:
                chart.x_labels = ['Day {}'.format(i + 1) for i in range(len(data))]
            elif 'rate' in chart_type:
                chart.x_labels = ['Day {}'.format(i + 2) for i in range(len(data[1:]))]
        elif x_label == 'both':
            if 'total' in chart_type:
                chart.x_labels = ['{} (Day {})'.format(data[i][0], i + 1) for i in range(len(data))]
            elif 'rate' in chart_type:
                chart.x_labels = ['{} (Day {})'.format(data[i + 1][0], i + 2) for i in range(len(data[1:]))]
        else:
            if 'total' in chart_type:
                chart.x_labels = [i[0] for i in data]
            elif 'rate' in chart_type:
                chart.x_labels = [i[0] for i in data[1:]]

        chart.x_label_rotation = 20
        chart.x_labels_major_count = 7 + (len(data) - 7) * (8 <= len(data) <= 10) - 1 * (11 <= len(data) <= 12)
        chart.truncate_label = -1
        chart.show_minor_x_labels = False

        if chart_type == 'total default':
            data_max = max([max([j for j in i[1:]]) for i in data])
            data_min = min([min([j for j in i[1:]]) for i in data])
        elif chart_type == 'total stacked':
            data_max = max([sum([j for j in i[1:]]) for i in data])
            data_min = min([sum([j for j in i[1:]]) for i in data])
        elif chart_type == 'rate default':
            data_max = max([max([data[i][j] - data[i - 1][j] for i in range(1, len(data))]) for j in range(1, len(self.storage.get_columns()) + 1)])
            data_min = min([min([data[i][j] - data[i - 1][j] for i in range(1, len(data))]) for j in range(1, len(self.storage.get_columns()) + 1)])
        elif chart_type == 'rate stacked':
            data_max = max([sum([data_rate[i][j] for i in range(len(data_rate))]) for j in range(len(data_rate[0]))])
            data_min = min([sum([data_rate[i][j] for i in range(len(data_rate))]) for j in range(len(data_rate[0]))])
        elif chart_type == 'rate default average':
            data_max = ceil(max([max(i) for i in data_average]))
            data_min = floor(min([min(i) for i in data_average]))
        elif chart_type == 'rate stacked average':
            data_max = ceil(max([sum([data_average[i][j] for i in range(len(data_average))]) for j in range(len(data_average[0]))]))
            data_min = floor(min([sum([data_average[i][j] for i in range(len(data_average))]) for j in range(len(data_average[0]))]))

        chart.y_labels = self._calculate_y_labels(data_min, data_max, allow_float=allow_float, max_y_labels=max_y_labels)

        # Chart Legends
        chart.legend_at_bottom = True
        chart.legend_at_bottom_columns = 6
        chart.legend_box_size = 16

        # Chart Style
        chart.style = super()._get_style(style)
        if 'default' in chart_type:
            chart.fill = False
            chart.stroke_style = {
                'width': 2.5,
                'linecap': 'round',
                'linejoin': 'round'
            }
        elif 'stacked' in chart_type:
            chart.fill = True

        # Chart Render
        file_name = '{}_development'.format(self.storage.name.lower())
        if 'total' in chart_type:
            file_name += '_total'
        if 'rate' in chart_type:
            file_name += '_rate'
        if 'stacked' in chart_type:
            file_name += '_stacked'
        if 'average' in chart_type:
            file_name = file_name.replace('_development', '_average_development')
        chart.render_to_file(path(CHART_BASE_PATH, file_name + CHART_FILE_EXTENSION))

        # Notice
        self._notice_chart_export(file_name)

    def _calculate_y_labels(self, data_min: float, data_max: float, max_y_labels: int=DEFAULT_MAX_Y_LABELS, allow_float: bool=False) -> list:
        """ Method: Calculate y-labels """
        data_min: int = floor(data_min)
        data_max: int = ceil(data_max)

        if allow_float:
            data_min *= 100
            data_max *= 100

        preset = 1, 2, 5
        data_range = list(range(0, data_min - 1, -1)) + list(range(0, data_max + 1, 1))
        i = 0

        while len(data_range) > max_y_labels:
            data_range = list(range(0, data_min - preset[i % 3] * 10**(i // 3), -1 * preset[i % 3] * 10**(i // 3)))
            data_range += list(range(0, data_max + preset[i % 3] * 10**(i // 3), preset[i % 3] * 10**(i // 3)))
            i += 1

        data_range.sort()

        if allow_float:
            data_range = [i/100 for i in data_range]

        return data_range

    def _get_dot_data_list(self, data: list[list[Any]], dots_count: int=DEFAULT_DOTS_COUNT, force_visible: bool=False, visible_at_zero: bool=True) -> list:
        """ Method: Get a list of dot node data based on data and dots count """
        return [self._get_dot_data(data, i, dots_count=dots_count, force_visible=force_visible, visible_at_zero=visible_at_zero) for i in range(len(data))]

    def _get_dot_data(self, data: list[list[Any]], index: int, dots_count: int=DEFAULT_DOTS_COUNT, force_visible: bool=False, visible_at_zero: bool=True) -> dict:
        """ Method: Get dot node data for adding into chart based on actual data, index, and dots count """
        if force_visible:
            dot_visibility = True
            dot_size = self._calculate_dot_size(len(data))
        else:
            dot_visibility = self._get_dot_visibility(index, len(data), dots_count)
            dot_size = self._calculate_dot_size(dots_count)

        if not visible_at_zero and data[index] == 0:
            dot_visibility = False

        return {'value': data[index], 'node': {'r': dot_visibility * dot_size}}

    def _get_dot_visibility(self, index: int, data_length: int, dots_count: int=DEFAULT_DOTS_COUNT) -> bool:
        """ Method: Calculate dot visibility based on index, data length, and desired dots count """
        if dots_count < 2:
            return False

        is_right_step = floor(index % ((data_length - 1) / (dots_count - 1))) == 0
        is_last_index = index == data_length - 1

        return is_right_step or is_last_index

    def _calculate_dot_size(self, dots_count: int=DEFAULT_DOTS_COUNT) -> float:
        """ Method: Calculate dot size based on dots count """
        weight = MAX_DOTS_SIZE_RETAIN + max(0, dots_count - MAX_DOTS_SIZE_RETAIN) / SHRINK_FACTOR
        margin = max(MAX_DOTS_SIZE_RETAIN, dots_count)

        return (weight / margin) * BASE_DOTS_SIZE
