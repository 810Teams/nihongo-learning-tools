"""
    core/constant/caching.py
"""

from core.util.format import path


CACHE_BASE_PATH: str = path('core', 'cache')
CACHE_FILE_EXTENSION: str = '.json'

SESSION_CACHE_FILE_NAME: str = 'session'


class SessionCacheConstant:
    LAST_USED_APP: str = 'last_used_app'
    TIMESTAMP: str = 'timestamp'
