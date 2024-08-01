"""
    `core/service/cache_service_base.py`
"""

import datetime

from typing import Any

from core.constant.caching import *
from core.service.json_service import JsonService


class CacheService:
    def __init__(self) -> None:
        self.json_service: JsonService = JsonService(CACHE_BASE_PATH, SESSION_CACHE_FILE_NAME + CACHE_FILE_EXTENSION)
        self.json_service.setup()

    def set_last_used_app(self, last_used_app: str) -> None:
        self.json_service.write_json({
            SessionCacheConstant.LAST_USED_APP: last_used_app,
            SessionCacheConstant.TIMESTAMP: datetime.datetime.now().__str__()
        })

    def get_last_used_app(self) -> str | None:
        try:
            return self.json_service.read_json()[SessionCacheConstant.LAST_USED_APP]
        except (FileNotFoundError, KeyError):
            return None
