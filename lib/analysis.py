'''
    `analysis.py`
'''

from datetime import datetime
from datetime import timedelta
import numpy
import pandas
import pygal
from math import ceil
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
from lib.utils import error, notice, average


def analysis(df, style='DefaultStyle'):
    ''' Function: Analysis '''
    data = numpy.array(df).tolist()
    data = clean(data)

    # Analysis
    try:
        analysis_kanji_total(data, style=eval(style), data_gap=10)
        analysis_kanji_development(
            data, chart_type='total default', style=eval(style), data_gap=20)
        analysis_kanji_development(
            data, chart_type='total stacked', style=eval(style), data_gap=50)
        analysis_kanji_development(
            data, chart_type='rate default',  style=eval(style), data_gap=1)
        analysis_kanji_development(
            data, chart_type='rate stacked',  style=eval(style), data_gap=2)
        analysis_kanji_development(
            data, chart_type='rate default average', style=eval(style), data_gap=1)
        analysis_kanji_development(
            data, chart_type='rate stacked average', style=eval(style), data_gap=2)
    except (NameError, SyntaxError):
        error('Invalid style name found. Aborting chart creation process.')


def clean(data):
    ''' Function: Clean Data '''
    def add_day_to_date(date_string, days): return (str(datetime.strptime(
        date_string, '%Y-%m-%d') + timedelta(days=days)).split()[0])

    # Step 1 - Sort
    data.sort(key=lambda i: i[0])

    # Step 2 - Date Formatting
    data = [[i[0].split()[0]] + [j for j in i[1:]] for i in data]

    # Step 3 - Remove Date Duplications
    data = [data[i] for i in range(
        len(data) - 1) if data[i][0] != data[i + 1][0]] + [data[-1]]

    # Step 4 - Add Missing Dates
    missing_dates = list()
    start_date = data[0][0]
    end_date = data[-1][0]

    while start_date != end_date:
        if start_date not in [i[0] for i in data]:
            select = [i for i in data if i[0] ==
                      add_day_to_date(start_date, -1)][0]
            missing_dates.append([start_date] + select[1:])
        start_date = add_day_to_date(start_date, 1)
        data += missing_dates
        missing_dates = []

    # Step 5 - Sort Again
    data.sort(key=lambda i: i[0])

    # Step 6 - Return
    return data


def analysis_kanji_total(data, style=DefaultStyle, data_gap=10):
    ''' Function: Kanji Total Analysis '''
    chart = pygal.Bar()

    # Chart Data
    columns = 'N5', 'N4', 'N3', 'N2', 'N1', '-'
    for i in range(len(columns)):
        chart.add(columns[i], data[-1][i + 1])

    # Chart Titles
    chart.title = 'Kanji Totals'
    chart.x_title = 'Kanji Level'
    chart.y_title = 'Kanji Amount'

    # Chart Labels
    chart.y_labels = range(
        0, max([int(i) for i in data[-1][1:]]) + data_gap, data_gap)

    # Chart Legends
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 6
    chart.legend_box_size = 16

    # Chart Render
    chart.style = style
    chart.render_to_file('charts/kanji_total.svg')

    # Notice
    notice('Chart \'kanji_total\' successfully exported.')


def analysis_kanji_development(data, chart_type='total default', style=DefaultStyle, data_gap=25):
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
    columns = 'N5', 'N4', 'N3', 'N2', 'N1', '-'
    if 'total' in chart_type:
        for i in range(len(columns)):
            chart.add(columns[i], [j[i + 1] for j in data])

    elif 'rate' in chart_type:
        data_rate = [[data[i][j] - data[i - 1][j]
                      for i in range(1, len(data))] for j in range(1, 7)]
        if 'average' not in chart_type:
            for i in range(len(columns)):
                chart.add(columns[i], data_rate[i])
        else:
            for i in range(len(columns)):
                chart.add(columns[i], [average(data_rate[i][0:j + 1])
                                       for j in range(len(data_rate[i]))])

    # Chart Titles
    chart.title = 'Kanji Development'

    if 'rate' in chart_type:
        chart.title += ' Rate'
    if 'stacked' in chart_type:
        chart.title += ' (Stacked)'
    if 'average' in chart_type:
        chart.title = chart.title.replace(
            'Kanji Development', 'Kanji Average Development')

    chart.x_title = 'Date'
    chart.y_title = 'Kanji Amount'

    # Chart Labels
    if 'total' in chart_type:
        chart.x_labels = [i[0] for i in data]
    elif 'rate' in chart_type:
        chart.x_labels = [i[0] for i in data[1:]]
    chart.x_label_rotation = 20
    chart.x_labels_major_count = 7
    chart.truncate_label = -1
    chart.show_minor_x_labels = False

    if chart_type == 'total default':
        chart.y_labels = range(
            0, max([i for i in data[-1][1:]]) + data_gap, data_gap)
    elif chart_type == 'total stacked':
        chart.y_labels = range(
            0, sum([i for i in data[-1][1:]]) + data_gap, data_gap)
    elif chart_type == 'rate default':
        chart.y_labels = range(0, max([max([data[i][j] - data[i - 1][j] for i in range(
            1, len(data))]) for j in range(1, 7)]) + data_gap, data_gap)
    elif chart_type == 'rate stacked':
        data_rate = [[data[i][j] - data[i - 1][j]
                      for i in range(1, len(data))] for j in range(1, 7)]
        chart.y_labels = range(0, max([sum([data_rate[i][j] for i in range(
            len(data_rate))]) for j in range(len(data_rate[0]))]) + data_gap, data_gap)
    elif chart_type == 'rate default average':
        data_rate = [[data[i][j] - data[i - 1][j]
                      for i in range(1, len(data))] for j in range(1, 7)]
        data_average = [[average(data_rate[j][0:i + 1])
                         for i in range(len(data_rate[0]))] for j in range(len(data_rate))]
        chart.y_labels = range(
            0, ceil(max([max(i) for i in data_average])) + data_gap, data_gap)
    elif chart_type == 'rate stacked average':
        data_rate = [[data[i][j] - data[i - 1][j]
                      for i in range(1, len(data))] for j in range(1, 7)]
        data_average = [[average(data_rate[j][0:i + 1])
                         for i in range(len(data_rate[0]))] for j in range(len(data_rate))]
        chart.y_labels = range(0, ceil(max([sum([data_average[i][j] for i in range(
            len(data_average))]) for j in range(len(data_average[0]))])) + data_gap, data_gap)

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

    file_name = 'kanji_development'
    if 'total' in chart_type:
        file_name += '_total'
    if 'rate' in chart_type:
        file_name += '_rate'
    if 'stacked' in chart_type:
        file_name += '_stacked'
    if 'average' in chart_type:
        file_name = file_name.replace('kanji_', 'kanji_average_')
    chart.render_to_file('charts/' + file_name + '.svg')

    # Notice
    notice('Chart \'{}\' successfully exported.'.format(file_name))
