"""
    `src/service/render.py`
"""

from pygal.style import DefaultStyle

from datetime import datetime
from datetime import timedelta
from math import ceil, floor
from time import perf_counter

from src.model.storage import Storage
from src.util.logging import error
from src.util.logging import notice
from src.util.calculation import average

import numpy
import pygal

from src.util.transform import transpose


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
        allow_float=False,
        average_range=None,
        days=0,
        is_dynamic=False,
        is_today=False,
        max_dots=100,
        max_y_labels=15,
        style='DefaultStyle',
        x_label='date'
    ):
        """ Function: Analysis """
        # Data Preparation
        time_start = perf_counter()
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
                max_dots=max_dots,
                max_y_labels=max_y_labels,
                style=style,
                x_label=x_label
            )

        # Report
        notice('Total time spent rendering charts is {:.2f} seconds.'.format(perf_counter() - time_start))


    def clean(self, data):
        """ Function: Clean Data """
        # Step 1 - Sort
        data.sort(key=lambda i: i[0])

        # Step 2 - Date Formatting
        data = [[i[0].split()[0]] + i[1:] for i in data]

        # Step 3 - Remove Date Duplications
        data = [data[i] for i in range(len(data) - 1) if data[i][0] != data[i + 1][0]] + [data[-1]]

        # Step 4 - Return
        return data


    def manipulate(self, data, days=0, is_dynamic=False, is_today=False):
        """ Function: Manipulate Data """
        # Step 1 - Sort
        data.sort(key=lambda i: i[0])

        # Step 2 - Add Missing Dates
        if is_dynamic:
            data = self.dynamic_fill(data)
        else:
            data = self.static_fill(data)

        # Step 3 - Sort Again
        data.sort(key=lambda i: i[0])

        # Step 4 - Add Until Today
        if is_today:
            data = self.today_fill(data)

        # Step 5 - Time Filtering
        data = data[-1 * days:]

        # Step 6 - Return
        return data


    def validate_arguments(self, data, average_range=None, days=0):
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


    def add_day_to_date(self, date_string, days):
        """ Function: Add days to date """
        return str(datetime.strptime(date_string, '%Y-%m-%d') + timedelta(days=days)).split()[0]


    def static_fill(self, data):
        """ Function: Fill missing data statically """
        missing_dates = list()
        start_date = data[0][0]
        end_date = data[-1][0]

        # Step 1: Fill missing gaps
        while start_date != end_date:
            if start_date not in [i[0] for i in data]:
                select = [i for i in data if i[0] == self.add_day_to_date(start_date, -1)][0]
                missing_dates.append([start_date] + select[1:])
            start_date = self.add_day_to_date(start_date, 1)
            data += missing_dates
            missing_dates = []

        # Step 2: Return
        return data


    def dynamic_fill(self, data):
        """ Function: Fill missing data dynamically """
        missing_dates = [list()]
        start_date = data[0][0]
        end_date = data[-1][0]

        # Step 1: Determines missing dates
        while start_date != end_date:
            if start_date not in [i[0] for i in data]:
                missing_dates[-1].append(start_date)
            elif len(missing_dates[-1]) > 0:
                missing_dates.append(list())
            start_date = self.add_day_to_date(start_date, 1)

        if len(missing_dates[-1]) == 0:
            missing_dates = missing_dates[:-1]

        # Step 2: Pinpoint
        for i in range(len(missing_dates)):
            data_start = [j for j in data if j[0] == self.add_day_to_date(missing_dates[i][0], -1)][0]
            data_end   = [j for j in data if j[0] == self.add_day_to_date(missing_dates[i][-1], 1)][0]

            for j in range(len(missing_dates[i])):
                missing_dates[i][j] = [missing_dates[i][j]]
                for k in range(1, len(data_start)):
                    missing_dates[i][j].append(data_start[k] + int((j + 1)/(len(missing_dates[i]) + 1) * (data_end[k] - data_start[k])))

        # Step 3: Append
        for i in missing_dates:
            for j in i:
                data.append(j)

        # Step 4: Return
        return data


    def today_fill(self, data):
        """ Function: Fill date until today """
        today = str(datetime.now())
        today = today[0:len(today)-7].split()[0]

        while data[-1][0].split()[0] != today:
            data_copy = [i for i in data[-1]]
            data.append(data_copy)
            data[-1][0] = self.add_day_to_date(data[-1][0], 1)

        return data


    def render_chart_total(self, data, allow_float=False, max_y_labels=15, style=DefaultStyle):
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
        data,
        allow_float=False,
        average_range=None,
        chart_type='total default',
        max_dots=100,
        max_y_labels=15,
        style=DefaultStyle,
        x_label='date'
    ):
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
        dots_every = 1
        while len(data)/dots_every > max_dots:
            dots_every += 1

        get_dot_data = lambda _value, _i, _len: {
            'value': _value,
            'node': {
                'r': (_i % dots_every == 0 or _i == _len - 1) * 2
            }
        }
        get_dot_data_list = lambda _data: [
            get_dot_data(_data[i], i, len(_data)) for i in range(len(_data))
        ]

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


    def calculate_y_labels(self, data_min, data_max, allow_float=False, max_y_labels=15):
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
