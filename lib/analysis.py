'''
    `analysis.py`
    @author 810Teams
'''

from datetime import datetime
from datetime import timedelta
import numpy
import pandas
import pygal
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
from lib.utils import error, notice

def analysis(df, style='DefaultStyle'):
    ''' Function: Analysis '''
    data = numpy.array(df).tolist()
    data = clean(data)

    # Analysis
    try:
        analysis_kanji_total(data, style=eval(style))
        analysis_kanji_development(data, chart_type='total default', style=eval(style))
        analysis_kanji_development(data, chart_type='total stacked', style=eval(style))
        analysis_kanji_development(data, chart_type='rate default', style=eval(style))
        analysis_kanji_development(data, chart_type='rate stacked', style=eval(style))
    except NameError:
        error('Invalid style name found. Aborting chart creation process.')

def clean(data):
    ''' Function: Clean Data '''
    add_day_to_date = lambda date_string, days: (str(datetime.strptime(date_string, '%Y-%m-%d') + timedelta(days=days)).split()[0])

    # Step 1 - Sort
    data.sort(key=lambda i: i[0])

    # Step 2 - Date Formatting
    data = [[i[0].split()[0]] + [j for j in i[1:]] for i in data]

    # Step 3 - Remove Date Duplications
    data = [data[i] for i in range(len(data) - 1) if data[i][0] != data[i + 1][0]] + [data[-1]]

    # Step 4 - Add Missing Dates
    missing_dates = list()
    start_date = data[0][0]
    end_date = data[-1][0]

    while start_date != end_date:
        if start_date not in [i[0] for i in data]:
            select = [i for i in data if i[0] == add_day_to_date(start_date, -1)][0]
            missing_dates.append([start_date] + select[1:])
        start_date = add_day_to_date(start_date, 1)
    data += missing_dates

    # Step 5 - Sort Again
    data.sort(key=lambda i: i[0])

    # Step 6 - Return
    return data

def analysis_kanji_total(data, style=DefaultStyle):
    ''' Function: Bar Chart Analysis '''
    chart = pygal.Bar()

    # Chart Data
    chart.add('N5', data[-1][1])
    chart.add('N4', data[-1][2])
    chart.add('N3', data[-1][3])
    chart.add('N2', data[-1][4])
    chart.add('N1', data[-1][5])
    chart.add('-', data[-1][6])

    # Chart Titles
    chart.title = 'Kanji Totals'
    chart.x_title = 'Kanji Level'
    chart.y_title = 'Kanji Amount'

    # Chart Labels
    chart.y_labels = range(0, max([int(i) for i in data[-1][1:]]) + 10, 10)

    # Chart Legends
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 6
    chart.legend_box_size = 16

    # Chart Render
    chart.style = style
    chart.render_to_file('charts/kanji_total.svg')

    # Notice
    notice('Chart \'kanji_total\' successfully exported.')

def analysis_kanji_development(data, chart_type='total default', style=DefaultStyle):
    ''' Function: Line Chart Analysis '''
    # Chart Define
    chart_type = [i.lower() for i in chart_type.split()]
    if 'total' in chart_type and 'default' in chart_type:
        chart_type = 'total default'
    elif 'total' in chart_type and 'stacked' in chart_type:
        chart_type = 'total stacked'
    elif 'rate' in chart_type and 'default' in chart_type:
        chart_type = 'rate default'
    elif 'rate' in chart_type and 'stacked' in chart_type:
        chart_type = 'rate stacked'
    else:
        error('Invalid chart type found. Aborting chart creation process.')
        return

    # Chart Creation
    if 'default' in chart_type:
        chart = pygal.Line()
    elif 'stacked' in chart_type:
        chart = pygal.StackedLine()

    # Chart Data
    if 'total' in chart_type:
        chart.add('N5', [i[1] for i in data])
        chart.add('N4', [i[2] for i in data])
        chart.add('N3', [i[3] for i in data])
        chart.add('N2', [i[4] for i in data])
        chart.add('N1', [i[5] for i in data])
        chart.add('-', [i[6] for i in data])
    elif 'rate' in chart_type:
        chart.add('N5', [data[i][1] - data[i - 1][1] for i in range(1, len(data))])
        chart.add('N4', [data[i][2] - data[i - 1][2] for i in range(1, len(data))])
        chart.add('N3', [data[i][3] - data[i - 1][3] for i in range(1, len(data))])
        chart.add('N2', [data[i][4] - data[i - 1][4] for i in range(1, len(data))])
        chart.add('N1', [data[i][5] - data[i - 1][5] for i in range(1, len(data))])
        chart.add('-',  [data[i][6] - data[i - 1][6] for i in range(1, len(data))])

    # Chart Titles
    if chart_type == 'total default':
        chart.title = 'Kanji Development'
    elif chart_type == 'total stacked':
        chart.title = 'Kanji Development (Stacked)'
    elif chart_type == 'rate default':
        chart.title = 'Kanji Development Rate'
    elif chart_type == 'rate stacked':
        chart.title = 'Kanji Development Rate (Stacked)'
    chart.x_title = 'Date'
    chart.y_title = 'Kanji Amount'

    # Chart Labels
    if 'total' in chart_type:
        chart.x_labels = [i[0] for i in data]
    elif 'rate' in chart_type:
        chart.x_labels = [i[0] for i in data[1:]]
    chart.x_label_rotation = 30
    chart.x_labels_major_every = 3
    chart.show_minor_x_labels = False

    if chart_type == 'total default':
        chart.y_labels = range(0, max([i for i in data[-1][1:]]) + 25, 25)
    elif chart_type == 'total stacked':
        chart.y_labels = range(0, sum([i for i in data[-1][1:]]) + 50, 50)
    elif chart_type == 'rate default':
        chart.y_labels = range(0, max([max([data[i][j] - data[i - 1][j] for i in range(1, len(data))]) for j in range(1, 7)]) + 2, 2)
    elif chart_type == 'rate stacked':
        raw_data = [[data[i][j] - data[i - 1][j] for i in range(1, len(data))] for j in range(1, 7)]
        chart.y_labels = range(0, max([sum([raw_data[j][i] for j in range(len(raw_data))]) for i in range(len(raw_data[0]))]) + 5, 5)

    # Chart Legends
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 6
    chart.legend_box_size = 16

    # Chart Interpolations
    if 'total' in chart_type:
        chart.interpolate = 'cubic'
    elif 'rate' in chart_type:
        pass

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
        if 'total' in chart_type:
            chart.render_to_file('charts/kanji_development_total.svg')
        elif 'rate' in chart_type:
            chart.render_to_file('charts/kanji_development_rate.svg')
    elif 'stacked' in chart_type:
        chart.dots_size = 1.5
        chart.fill = True
        if 'total' in chart_type:
            chart.render_to_file('charts/kanji_development_total_stacked.svg')
        elif 'rate' in chart_type:
            chart.render_to_file('charts/kanji_development_rate_stacked.svg')

    # Notice
    if chart_type == 'total default':
        notice('Chart \'kanji_development_total\' successfully exported.')
    elif chart_type == 'total stacked':
        notice('Chart \'kanji_development_total_stacked\' successfully exported.')
    elif chart_type == 'rate default':
        notice('Chart \'kanji_development_rate\' successfully exported.')
    elif chart_type == 'rate stacked':
        notice('Chart \'kanji_development_rate_stacked\' successfully exported.')
