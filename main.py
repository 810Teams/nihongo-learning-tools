'''
    `main.py`
    <!-- Docs go here -->

    @author 810Teams
    @version a0.0.2
'''

from extensions.kanji import kanji_calculate
from lib.storage import Storage
from lib.utils import error, notice

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
        print('[K] Kanji Calculation')
        print('[AK] Append Kanji Data')
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
        exit()
    elif action == 'K':
        print()
        print('- Kanji Calculation -')
        print(kanji_calculate(int(input('Current Page: ')), int(input('Current Line: '))))
    elif action == 'AK':
        storage_main.append([kanji_calculate(int(i.split('-')[0]), int(i.split('-')[1])) for i in input('Appending Data: ').split(' ')])
    else:
        error('Invalid action.')

main()
