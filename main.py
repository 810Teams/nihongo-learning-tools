"""
    `main.py`
    <!-- Docs go here -->

    @author 810Teams
    @version a0.0.1
"""

import storage

def main():
    """ Main """
    store = storage.Storage('kanji')
    #store.new(['N5', 'N4', 'N3', 'N2', 'N1', 'N?'])
    store.load()
    #store.add([102, 95, 97, 56, 30, 7])
    store.save()

    print(store.storage)

main()
