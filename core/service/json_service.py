"""
    `core/service/json_service_base.py`
"""

import json
import os

from typing import Any

from core.util.format import path


class JsonService:
    def __init__(self, folder_path: str, file_name: str) -> None:
        self.folder_path: str = folder_path
        self.file_name: str = file_name

    def setup(self) -> None:
        """ Method: Set up folders """
        try:
            os.mkdir(self.folder_path)
        except FileExistsError:
            pass

    def read_json(self) -> dict[str, Any]:
        """ Method: Read JSON from file """
        with open(self.get_file_path(), 'r') as openfile:
            return json.load(openfile)

    def write_json(self, data: dict[str, Any]):
        """ Method: Write JSON to file """
        json_object: str = json.dumps(data, indent=4)

        with open(self.get_file_path(), 'w') as outfile:
            outfile.write(json_object)

    def get_file_path(self) -> str:
        """ Method: Get file path """
        return path(self.folder_path, self.file_name)
