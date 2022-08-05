import json
from pathlib import Path
from typing import Optional


class ClientConfig:
    def __init__(self, path: Path):
        self.__path: Path = path
        self.gb_db_version: Optional[int] = None
        self.jp_db_version: Optional[int] = None
        self.load()

    def load(self):
        if not self.__path.exists() or not self.__path.is_file():
            return

        data = json.loads(self.__path.read_bytes())
        self.gb_db_version = data['gb_db_version'] if 'gb_db_version' in data else None
        self.jp_db_version = data['jp_db_version'] if 'jp_db_version' in data else None

    def save(self):
        data = json.dumps({
            'gb_db_version': self.gb_db_version,
            'jp_db_version': self.jp_db_version
        })
        self.__path.write_text(data, encoding='utf8')
        pass
