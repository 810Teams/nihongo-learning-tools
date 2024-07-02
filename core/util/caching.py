"""
    `core/util/caching.py`
"""

import os


def clear_cache(directory: str='.'):
    """ Clear cache with pyclean """
    print()
    os.system('pyclean {}'.format(directory))
