'''
    `analysis.py`
'''

from datetime import datetime
from datetime import timedelta
from math import ceil, floor
from pygal.style import DefaultStyle
from pygal.style import DarkStyle
from pygal.style import NeonStyle
from pygal.style import DarkSolarizedStyle
from pygal.style import LightSolarizedStyle
from pygal.style import LightStyle
from pygal.style import CleanStyle
from pygal.style import RedBlueStyle
from pygal.style import DarkColorizedStyle
from pygal.style import LightColorizedStyle
from pygal.style import TurquoiseStyle
from pygal.style import LightGreenStyle
from pygal.style import DarkGreenStyle
from pygal.style import DarkGreenBlueStyle
from pygal.style import BlueStyle
from src.utils import error
from src.utils import notice
from src.utils import average
from time import perf_counter

import numpy
import pandas
import pygal

NAME = str()
COLUMNS = list()


def analysis(storage_main, allow_float=False, average_range=None, duration=0, is_dynamic=False, max_y_labels=15, style='DefaultStyle', is_today=False):
    ''' Function: Analysis '''
    time_start = perf_counter()

    global NAME, COLUMNS
    NAME = storage_main.name
    COLUMNS = storage_main.storage.columns[1:]

    data = clean(numpy.array(storage_main.storage).tolist())

    if not validate_arguments(data, average_range=average_range, duration=duration, is_dynamic=is_dynamic, max_y_labels=max_y_labels, style=style, is_today=is_today):
        return
    
    data = manipulate(data, duration=duration, is_dynamic=is_dynamic, is_today=is_today)

    # Analysis
    try:
        style = eval(style)
    except (NameError, SyntaxError):
        error('Invalid style name. \'DefaultStyle\' will be used instead.')
        style = DefaultStyle
    
    render_chart_total(data, allow_float=allow_float, max_y_labels=max_y_labels, style=style)
    render_chart_development(data, allow_float=allow_float, chart_type='total default', max_y_labels=max_y_labels, style=style)
    render_chart_development(data, allow_float=allow_float, chart_type='total stacked', max_y_labels=max_y_labels, style=style)
    render_chart_development(data, allow_float=allow_float, chart_type='rate default',  max_y_labels=max_y_labels, style=style)
    render_chart_development(data, allow_float=allow_float, chart_type='rate stacked',  max_y_labels=max_y_labels, style=style)
    render_chart_development(data, allow_float=allow_float, average_range=average_range, chart_type='rate default average', max_y_labels=max_y_labels, style=style)
    render_chart_development(data,allow_float=allow_float,  average_range=average_range, chart_type='rate stacked average', max_y_labels=max_y_labels, style=style)
    notice('Total time spent rendering charts is {:.2f} seconds.'.format(perf_counter() - time_start))


def clean(data):
    ''' Function: Clean Data '''
    # Step 1 - Sort
    data.sort(key=lambda i: i[0])

    # Step 2 - Date Formatting
    data = [[i[0].split()[0]] + i[1:] for i in data]

    # Step 3 - Remove Date Duplications
    data = [data[i] for i in range(len(data) - 1) if data[i][0] != data[i + 1][0]] + [data[-1]]

    # Step 4 - Return
    return data


def manipulate(data, duration=0, is_dynamic=False, is_today=False):
    ''' Function: Manipulate Data '''
    # Step 1 - Sort
    data.sort(key=lambda i: i[0])

    # Step 2 - Add Missing Dates
    if is_dynamic:
        data = dynamic_fill(data)
    else:
        data = static_fill(data)

    # Step 3 - Sort Again
    data.sort(key=lambda i: i[0])

    # Step 4 - Add Until Today
    if is_today:
        data = today_fill(data)

    # Step 5 - Time Filtering
    data = data[-1 * duration:]

    # Step 6 - Return
    return data


def validate_arguments(data, average_range=None, duration=0, is_dynamic=False, max_y_labels=15, style='DefaultStyle', is_today=False):
    ''' Function: Validates arguments '''
    # Step 1: -average argument
    if average_range == None:
        pass
    elif not (1 <= average_range <= len(data) - 1):
        error('Average range must be an integer from {} to {}.'.format(1, len(data) - 1))
        error('Aborting chart creation process.')
        return False
    
    # Step 2: -duration argument
    if not (-len(data) + 2 <= duration <= len(data) and duration != 1):
        error('Duration must be an integer from {} to {}, and not 1.'.format(-len(data) + 2, len(data)))
        error('Aborting chart creation process.')
        return False
    
    return True


def add_day_to_date(date_string, days):
    ''' Function: Add days to date '''
    return str(datetime.strptime(date_string, '%Y-%m-%d') + timedelta(days=days)).split()[0]


def static_fill(data):
    ''' Function: Fill missing data statically '''
    missing_dates = list()
    start_date = data[0][0]
    end_date = data[-1][0]

    # Step 1: Fill missing gaps
    while start_date != end_date:
        if start_date not in [i[0] for i in data]:
            select = [i for i in data if i[0] == add_day_to_date(start_date, -1)][0]
            missing_dates.append([start_date] + select[1:])
        start_date = add_day_to_date(start_date, 1)
        data += missing_dates
        missing_dates = []
    
    # Step 2: Return
    return data


def dynamic_fill(data):
    ''' Function: Fill missing data dynamically '''
    missing_dates = [list()]
    start_date = data[0][0]
    end_date = data[-1][0]
    
    # Step 1: Determines missing dates
    while start_date != end_date:
        if start_date not in [i[0] for i in data]:
            missing_dates[-1].append(start_date)
        elif len(missing_dates[-1]) > 0:
            missing_dates.append(list())
        start_date = add_day_to_date(start_date, 1)
    
    if len(missing_dates[-1]) == 0:
        missing_dates = missing_dates[:-1]

    # Step 2: Pinpoint
    for i in range(len(missing_dates)):
        data_start = [j for j in data if j[0] == add_day_to_date(missing_dates[i][0], -1)][0]
        data_end   = [j for j in data if j[0] == add_day_to_date(missing_dates[i][-1], 1)][0]

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


def today_fill(data):
    ''' Function: Fill date until today '''
    today = str(datetime.now())
    today = today[0:len(today)-7].split()[0]

    while data[-1][0].split()[0] != today:
        data.append([i for i in data[-1]]) # NOTE: Uses list comprehension to prevent references
        data[-1][0] = add_day_to_date(data[-1][0], 1)

    return data


def render_chart_total(data, allow_float=False, max_y_labels=15, style=DefaultStyle):
    ''' Function: Kanji Total Analysis '''
    chart = pygal.Bar()

    # Chart Data
    for i in range(len(COLUMNS)):
        chart.add(COLUMNS[i], data[-1][i + 1])

    # Chart Titles
    chart.title = '{} Totals'.format(NAME.capitalize())
    chart.y_title = 'Amount'

    # Chart Labels
    chart.y_labels = calculate_y_labels(
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
    chart.render_to_file('charts/{}_total.svg'.format(NAME.lower()))

    # Notice
    notice('Chart \'{}_total\' successfully exported.'.format(NAME.lower()))


def render_chart_development(data, allow_float=False, average_range=None, chart_type='total default',  max_y_labels=15, style=DefaultStyle):
    ''' Function: Kanji Development Analysis '''
    # Chart Type Check
    chart_types = {
        'total default': 110,
        'total stacked': 120,
        'rate default': 210,
        'rate stacked': 220,
        'rate default average': 211,
        'rate stacked average': 221
    }

    if chart_type not in chart_types:
        error('Invalid chart type found. Aborting chart creation process.')
        return

    # Chart Creation
    if 'default' in chart_type:
        chart = pygal.Line()
    elif 'stacked' in chart_type:
        chart = pygal.StackedLine()

    # Chart Data
    if 'total' in chart_type:
        for i in range(len(COLUMNS)):
            chart.add(COLUMNS[i], [j[i + 1] for j in data])
    elif 'rate' in chart_type:
        data_rate = [[data[i][j] - data[i - 1][j] for i in range(1, len(data))] for j in range(1, len(COLUMNS) + 1)]
        if 'average' not in chart_type:
            for i in range(len(COLUMNS)):
                chart.add(COLUMNS[i], data_rate[i])
        else:
            data_average = list()
            for i in range(len(COLUMNS)):
                temp = list()

                for j in range(len(data_rate[i])):
                    if average_range == None:
                        temp.append(round(average(data_rate[i][0:j + 1]), 2))
                    elif 1 <= average_range <= len(data_rate[i]):
                        if j < average_range:
                            temp.append(round(average(data_rate[i][0:j + 1]), 2))
                        elif average_range <= j:
                            temp.append(round(average(data_rate[i][j - average_range + 1:j + 1]), 2))

                chart.add(COLUMNS[i], temp)
                data_average.append(temp)

    # Chart Titles
    chart.title = '{} Development'.format(NAME.capitalize())

    if 'rate' in chart_type:
        chart.title += ' Rate'
    if 'stacked' in chart_type:
        chart.title += ' (Stacked)'
    if 'average' in chart_type:
        chart.title = chart.title.replace(' Development', ' Average Development')

    chart.x_title = 'Date'
    chart.y_title = 'Amount'

    # Chart Labels
    if 'total' in chart_type:
        chart.x_labels = [i[0] for i in data]
    elif 'rate' in chart_type:
        chart.x_labels = [i[0] for i in data[1:]]
    chart.x_label_rotation = 20
    chart.x_labels_major_every = len(data) // 7 + (len(data) < 7)
    chart.truncate_label = -1
    chart.show_minor_x_labels = False

    if chart_type == 'total default':
        # data_max = max([i for i in data[-1][1:]])
        data_max = max([max([j for j in i[1:]]) for i in data])
        data_min = min([min([j for j in i[1:]]) for i in data])
    elif chart_type == 'total stacked':
        data_max = max([sum([j for j in i[1:]]) for i in data])
        data_min = min([sum([j for j in i[1:]]) for i in data])
    elif chart_type == 'rate default':
        data_max = max([max([data[i][j] - data[i - 1][j] for i in range(1, len(data))]) for j in range(1, len(COLUMNS) + 1)])
        data_min = min([min([data[i][j] - data[i - 1][j] for i in range(1, len(data))]) for j in range(1, len(COLUMNS) + 1)])
    elif chart_type == 'rate stacked':
        data_max = max([sum([data_rate[i][j] for i in range(len(data_rate))]) for j in range(len(data_rate[0]))])
        data_min = min([sum([data_rate[i][j] for i in range(len(data_rate))]) for j in range(len(data_rate[0]))])
    elif chart_type == 'rate default average':
        data_max = ceil(max([max(i) for i in data_average]))
        data_min = floor(min([min(i) for i in data_average]))
    elif chart_type == 'rate stacked average':
        data_max = ceil(max([sum([data_average[i][j] for i in range(len(data_average))]) for j in range(len(data_average[0]))]))
        data_min = floor(min([sum([data_average[i][j] for i in range(len(data_average))]) for j in range(len(data_average[0]))]))

    chart.y_labels = calculate_y_labels(data_min, data_max, allow_float=allow_float, max_y_labels=max_y_labels)

    # Chart Legends
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 6
    chart.legend_box_size = 16

    # Chart Interpolations
    if 'total' in chart_type or 'average' in chart_type:
        chart.interpolate = 'cubic'

    # Chart Render
    chart.style = style
    if 'default' in chart_type:
        chart.dots_size = 2.5
        chart.fill = False
        chart.stroke_style = {
            'width': 3,
            'linecap': 'round',
            'linejoin': 'round'
        }
    elif 'stacked' in chart_type:
        chart.dots_size = 1.5
        chart.fill = True

    file_name = '{}_development'.format(NAME.lower())
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


def calculate_y_labels(data_min, data_max, allow_float=False, max_y_labels=15):
    ''' Function: Calculate '''
    preset = 1, 2, 5
    data_range = list(range(0, data_min - 1, -1)) + list(range(0, data_max + 1, 1))
    i = 0

    while len(data_range) > max_y_labels:
        data_range = list(range(0, data_min - preset[i % 3] * 10**(i // 3), -1 * preset[i % 3] * 10**(i // 3)))
        data_range += list(range(0, data_max + preset[i % 3] * 10**(i // 3), preset[i % 3] * 10**(i // 3)))
        i += 1
        
    data_range.sort()

    if allow_float:
        if data_range[1] - data_range[0] == 1 and len(data_range)*2 - 1 < max_y_labels:
            data_range = sorted(data_range + [i + 0.5 for i in data_range if i + 0.5 <= data_max])
        if data_range[1] - data_range[0] == 0.5 and len(data_range)*2 - 1 < max_y_labels:
            data_range = sorted(data_range + [i + 0.25 for i in data_range if i + 0.25 <= data_max])  

    return data_range
