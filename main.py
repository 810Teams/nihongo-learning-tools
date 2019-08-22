'''
    `main.py`
    <!-- Docs go here -->

    @author 810Teams
    @version a0.0.2
'''

from storage import Storage
from utils import error, notice

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
        print()
        operate(storage_main, action = input('(A/S/V/X) ').strip().upper())

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
    else:
        error('Invalid action.')

main()
