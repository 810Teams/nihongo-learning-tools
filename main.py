'''
    `main.py`
    <!-- Docs go here -->

    @author 810Teams
    @version a0.0.2
'''

from extensions.kanji import kanji_calculate
from lib.storage import Storage
from lib.utils import error, notice
import numpy

def main():
    ''' Main Function '''
    print()
    print('--- Local Time Data Storage Terminal App ---')
    print()
    notice('Please input storage name')
    storage_main = Storage(input('Storage Name: ').strip())
    print()
    storage_main.load()

    while True:
        print()
        print('- Action List -')
        print('[A] Append Data')
        print('[S] Save Storage')
        print('[V] View Storage')
        print('[X] Exit Application')
        extensions_actions()
        print()
        operate(storage_main, input('(Action) ').split(' ')[0].upper())

def operate(storage_main, action):
    ''' Function: Operate a specific action '''
    if action == 'A':
        storage_main.append(input('Appending Data: ').split(' '))
    elif action == 'S':
        storage_main.save()
        print()
        notice('Storage saved successfully.')
    elif action == 'V':
        print()
        storage_main.view()
    elif action == 'X':
        print()
        exit()
    elif not extensions_operations(storage_main, action):
        error('Invalid action.')

def extensions_actions():
    ''' Function: Extensions actions '''
    print('[KS] Kanji Status')
    print('[KA] Append Kanji Data')

def extensions_operations(storage_main, action):
    ''' Function: Extensions operations '''
    if action == 'KS':
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
        return True
    elif action == 'KA':
        storage_main.append([kanji_calculate(int(i.split('-')[0]), int(i.split('-')[1])) for i in input('Appending Kanji Data: ').split(' ')])
        return True
    return False

main()
