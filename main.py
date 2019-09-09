'''
    `main.py`
    <!-- Docs go here -->

    @author 810Teams
    @version a0.3.0
'''

from lib.analysis import analysis
from lib.storage import Storage
from lib.utils import error, kanji_calculate, notice
import numpy

def main():
    ''' Main Function '''
    print()
    print('-- Personal Kanji Tracker Terminal Application --')
    print()
    notice('Please input storage name')
    storage_main = Storage(input('(Input) ').strip())
    print()
    storage_main.load()

    while True:
        print()
        print('- Action List -')
        print('[A] Append Data')
        print('[KA] Append Kanji Data')
        print('[KC] Kanji Charts')
        print('[KS] Kanji Status')
        print('[D] Delete Storage')
        print('[S] Save Storage')
        print('[V] View Storage')
        print('[X] Exit Application')
        print()
        operate(storage_main, input('(Action) ').split(' ')[0].upper())

def operate(storage_main, action):
    ''' Function: Operate a specific action '''
    if action == 'A':
        storage_main.append(input('(Input) ').split(' '))
    elif action == 'KA':
        notice('Please input kanji data in x-y format.')
        storage_main.append([kanji_calculate(int(i.split('-')[0]), int(i.split('-')[1])) for i in input('(Input) ').split(' ')])
    elif action == 'KC':
        analysis(storage_main.storage)
    elif action == 'KS':
        kanji_amount_list = numpy.array(storage_main.storage[['n5', 'n4', 'n3', 'n2', 'n1', '-']]).tolist()[-1]
        print()
        print('- Kanji Status -')
        print('Total Kanji:', sum(kanji_amount_list))
        print('N5:', kanji_amount_list[0])
        print('N4:', kanji_amount_list[1])
        print('N3:', kanji_amount_list[2])
        print('N2:', kanji_amount_list[3])
        print('N1:', kanji_amount_list[4])
        print('- :', kanji_amount_list[5])
    elif action == 'S':
        storage_main.save()
        print()
        notice('Storage \'{}\' saved successfully.'.format(storage_main.name))
    elif action == 'V':
        print()
        storage_main.view()
    elif action == 'X':
        print()
        exit()
    else:
        error('Invalid action.')

main()
