"""
    `src/service/render_service.py`
"""

from pandas.core.indexes import base
from pygal.style import DefaultStyle, Style

from datetime import datetime
from math import ceil, floor

from src.model.storage import Storage
from src.util.logging import error
from src.util.logging import notice
from src.util.calculation import average, add_day_to_date
from src.util.transform import transpose
from src.util.reader import contains_row_for_date, copy_list, find_row_by_date, is_empty, is_nan

import numpy
import pygal


class RenderService():
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.CHART_TYPE_LIST = [
            'total default', 'total stacked',
            'rate default', 'rate stacked',
            'rate default average', 'rate stacked average'
        ]

    def render_all(
        self,
        allow_float: bool=False,
        average_range: int=None,
        days: int=0,
        dots_count: int=100,
        is_dynamic: bool=False,
        is_today: bool=False,
        max_y_labels: int=15,
        style: str='DefaultStyle',
        x_label: str='date'
    ) -> None:
        """ Function: Analysis """
        # Data Preparation
        data = self.clean(numpy.array(self.storage.data).tolist())
        data = self.manipulate(data, days=days, is_dynamic=is_dynamic, is_today=is_today)

        # Arguments Validation
        if not self.validate_arguments(data, average_range=average_range, days=days):
            return

        # Style Loading
        try:
            exec('from pygal.style import {}'.format(style))
            style = eval(style)
        except (NameError, SyntaxError, ImportError):
            error('Invalid style name. \'DefaultStyle\' will be used instead.', start='\n')
            style = DefaultStyle

        # Rendering
        self.render_chart_total(data, allow_float=allow_float, max_y_labels=max_y_labels, style=style)
        for chart_type in self.CHART_TYPE_LIST:
            self.render_chart_development(
                data,
                allow_float=allow_float,
                average_range=average_range,
                chart_type=chart_type,
                dots_count=dots_count,
                max_y_labels=max_y_labels,
                style=style,
                x_label=x_label
            )


    def validate_arguments(self, data: list, average_range: int=None, days: int=0) -> bool:
        """ Function: Validates arguments which depends on the length of cleaned data """
        # Step 1: -average argument
        if average_range != None and not (1 <= average_range <= len(data) - 1):
            error('Average range must be an integer from {} to {}.'.format(1, len(data) - 1))
            error('Aborting chart creation process.')
            return False

        # Step 2: -duration argument
        if not (-len(data) + 2 <= days <= len(data) and days != 1):
            error('Duration must be an integer from {} to {}, and not 1.'.format(-len(data) + 2, len(data)))
            error('Aborting chart creation process.')
            return False

        return True


    def clean(self, data: list) -> list:
        """ Function: Clean Data """
        # Step 1 - Sort
        data.sort(key=lambda i: i[0])

        # Step 2 - Date Formatting
        data = [[i[0].split()[0]] + i[1:] for i in data]

        # Step 3 - Remove Date Duplications
        data = [data[i] for i in range(len(data) - 1) if data[i][0] != data[i + 1][0]] + [data[-1]]

        # Step 4 - Return
        return data


    def manipulate(self, data: list, days: int=0, is_dynamic: bool=False, is_today: bool=False) -> list:
        """ Function: Manipulate data """
        # Step 1 - Sort
        data.sort(key=lambda i: i[0])

        # Step 2 - Fill Missing Data
        data = self.fill_missing_data(data, is_dynamic=is_dynamic)

        # Step 3 - Sort Again
        data.sort(key=lambda i: i[0])

        # Step 4 - Add Until Today
        if is_today:
            data = self.today_fill(data)

        # Step 5 - Time Filtering
        data = data[-1 * days:]

        # Step 6 - Return
        return data


    def fill_missing_data(self, data: list, is_dynamic: bool=False) -> list:
        """ Function: Fill missing data """
        # Step 1: Add empty rows for missing dates
        data_new = copy_list(data)
        start_date = data_new[0][0]
        end_date = data_new[-1][0]

        while start_date != end_date:
            if not contains_row_for_date(data_new, start_date):
                data_new.append([start_date] + [None for _ in range(len(data_new[0]) - 1)])
            start_date = add_day_to_date(start_date, days=1)

        data_new.sort(key=lambda i: i[0])

        # Step 2: Fill for each column
        for col in range(1, len(data[0])):
            column_transpose = [i[col] for i in data_new]
            column_transpose = self.fill_missing_data_in_column(column_transpose, is_dynamic=is_dynamic)

            for i in range(len(column_transpose)):
                data_new[i][col] = column_transpose[i]

        # Step 3: Return
        return data_new


    def fill_missing_data_in_column(self, data: list, is_dynamic: bool=False) -> list:
        # Step 1: Determine missing indexes, store in groups
        missing_index_list = [list()]

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


    def today_fill(self, data: list) -> list:
        """ Function: Fill date until today """
        today = str(datetime.now())
        today = today[0:len(today)-7].split()[0]

        while data[-1][0].split()[0] != today:
            data_copy = [i for i in data[-1]]
            data.append(data_copy)
            data[-1][0] = add_day_to_date(data[-1][0], days=1)

        return data


    def render_chart_total(self, data: list, allow_float: bool=False, max_y_labels: int=15, style: Style=DefaultStyle) -> None:
        """ Function: Kanji Total Analysis """
        chart = pygal.Bar()

        # Chart Data
        for i in range(len(self.storage.get_columns())):
            chart.add(self.storage.get_columns()[i], data[-1][i + 1])

        # Chart Titles
        chart.title = '{} Totals'.format(self.storage.name.capitalize())
        chart.y_title = 'Amount'

        # Chart Labels
        chart.y_labels = self.calculate_y_labels(
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
        chart.style = style
        chart.render_to_file('charts/{}_total.svg'.format(self.storage.name.lower()))

        # Notice
        notice('Chart \'{}_total\' successfully exported.'.format(self.storage.name.lower()))


    def render_chart_development(
        self,
        data: list,
        allow_float: bool=False,
        average_range: int=None,
        chart_type: str='total default',
        dots_count: int=100,
        max_y_labels: int=15,
        style: Style=DefaultStyle,
        x_label: str='date'
    ) -> None:
        """ Function: Kanji Development Analysis """
        # Chart Type Check
        if chart_type not in self.CHART_TYPE_LIST:
            error('Invalid chart type found. Aborting chart creation process.', start='\n')
            return

        # Chart Initiation
        if 'default' in chart_type:
            chart = pygal.Line()
        elif 'stacked' in chart_type:
            chart = pygal.StackedLine()

        # Chart Data
        get_dot_data_list = lambda _data: [self.get_dot_data(_data, i, dots_count=dots_count) for i in range(len(_data))]
        columns = self.storage.get_columns()

        if 'total' in chart_type:
            for i in range(len(columns)):
                chart.add(columns[i], get_dot_data_list(transpose(data)[1:][i]))

        elif 'rate' in chart_type:
            data_rate = [[data[i][j] - data[i - 1][j] for i in range(1, len(data))] for j in range(1, len(columns) + 1)]

            if 'average' not in chart_type:
                for i in range(len(columns)):
                    chart.add(columns[i], get_dot_data_list(data_rate[i]))
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

                    chart.add(columns[i], get_dot_data_list(temp))
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

        chart.y_labels = self.calculate_y_labels(data_min, data_max, allow_float=allow_float, max_y_labels=max_y_labels)

        # Chart Legends
        chart.legend_at_bottom = True
        chart.legend_at_bottom_columns = 6
        chart.legend_box_size = 16

        # Chart Style
        chart.style = style
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
        chart.render_to_file('charts/' + file_name + '.svg')

        # Notice
        notice('Chart \'{}\' successfully exported.'.format(file_name))


    def calculate_y_labels(self, data_min, data_max, allow_float: bool=False, max_y_labels: int=15) -> list:
        """ Function: Calculate """
        data_min = floor(data_min)
        data_max = ceil(data_max)

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


    def get_dot_visibility(self, index: int, data_length: int, dots_count: int=101) -> bool:
        return floor(index % ((data_length - 1) / (dots_count - 1))) == 0 or index == data_length - 1


    def calculate_dot_size(self, dots_count: int=101, base_dots_size: float=2.5, shrink_start: int=45, factor: float=2.5) -> float:
        # `dots_count`: The dots count displayed on the charts
        # `base_dots_size`: The base dots size
        # `shrink_start`: The maximum dots count that will retain the base dot size
        # `factor`: The closer to 1, the slower the dots start shinking. If at 1, dots will never shrink.
        return base_dots_size * ((shrink_start + max(0, dots_count - shrink_start) / factor) / max(shrink_start, dots_count))


    def get_dot_data(self, data: list, index: int, dots_count: int=101) -> dict:
        return {
            'value': data[index],
            'node': {
                'r': self.get_dot_visibility(index, len(data), dots_count) * self.calculate_dot_size(dots_count)
            }
        }
