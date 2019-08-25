'''
    `kanji.py`
'''

from datetime import datetime
from datetime import timedelta
import numpy
import pandas
import pygal
from pygal.style import CleanStyle

def kanji_calculate(current_page, current_line):
    ''' Function: Calculate total learned kanjis from current page and line of Notability app '''
    return (current_page - 1) * 16 + current_line - 1

def analysis(df):
    ''' Function: Analysis '''
    data = numpy.array(df).tolist()

    # Formatting Dates
    data = [
                [
                    data[i][0].split()[0],
                    data[i][1],
                    data[i][2],
                    data[i][3],
                    data[i][4],
                    data[i][5],
                    data[i][6]
                ]
                for i in range(len(data)) if data[i][0].split()[0] != data[i - 1][0].split()[0]
            ]

    # Missing Dates
    date = data[0][0]
    temp = list()
    while date <= data[-1][0]:
        if date not in [i[0] for i in data]:
            selected_date = str(datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).split()[0]
            temp.append([i for i in data if i[0] == selected_date][0])
            temp[-1][0] = str(datetime.strptime(temp[-1][0], '%Y-%m-%d') + timedelta(days=1)).split()[0]
        date = str(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).split()[0]
    data += temp
    data.sort(key=lambda i: i[0])

    # Analysis
    analysis_bar(data)
    analysis_line(data)

def analysis_bar(data):
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

    # Chart Legends
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 6
    chart.legend_box_size = 16

    # Chart Render
    chart.render_to_file('charts/kanji_total.svg')

def analysis_line(data):
    ''' Function: Bar Chart Analysis '''
    chart = pygal.StackedLine()

    # Chart Data
    chart.add('N5', [i[1] for i in data])
    chart.add('N4', [i[2] for i in data])
    chart.add('N3', [i[3] for i in data])
    chart.add('N2', [i[4] for i in data])
    chart.add('N1', [i[5] for i in data])
    chart.add('-', [i[6] for i in data])

    # Chart Titles
    chart.title = 'Kanji Development'
    chart.x_title = 'Date & Time'
    chart.y_title = 'Kanji Amount'
    
    # Chart Labels
    chart.x_labels = [i[0] for i in data]

    # Chart Legends
    chart.legend_at_bottom = True
    chart.legend_at_bottom_columns = 6
    chart.legend_box_size = 16

    # Chart Render
    chart.fill = True
    chart.render_to_file('charts/kanji_development.svg')
