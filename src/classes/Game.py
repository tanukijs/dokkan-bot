import json
from pathlib import Path
from typing import Optional

from orator import DatabaseManager

import config


class GamePlatform:
    def __init__(
            self,
            name: str,
            user_agent: str,
            device_name: str,
            device_model: str,
            os_version: str
    ):
        self.name = name
        self.user_agent = user_agent
        self.device_name = device_name
        self.device_model = device_model
        self.os_version = os_version


class GameEnvironment:
    def __init__(
            self,
            name: str,
            url: str,
            port: int,
            version_code: str,
            db_path: Path,
            db_password: bytearray,
            country: str,
            currency: str,
            bundle_id: str
    ):
        self.name = name
        self.url = url
        self.port = port
        self.version_code = version_code
        self.db_path = db_path
        self.db_password = db_password
        self.db_manager = DatabaseManager({
            'mysql': {
                'driver': 'sqlite',
                'database': db_path
            }
        })
        self.country = country
        self.currency = currency
        self.bundle_id = bundle_id


class GameAccount:
    def __init__(
            self,
            unique_id: str,
            identifier: Optional[str] = None,
            access_token: Optional[str] = None,
            secret: Optional[str] = None
    ):
        self.unique_id = unique_id
        self.identifier = identifier
        self.access_token = access_token
        self.secret = secret

    def to_file(self, file_path: Path):
        json_data = json.dumps({
            'unique_id': self.unique_id,
            'identifier': self.identifier,
            'platform': config.game_env.name
        })
        file_path.write_text(json_data, encoding='utf8')

    @staticmethod
    def from_file(file_path: Path) -> 'GameAccount':
        json_data = json.loads(file_path.read_bytes())
        config.game_platform = config.IOS_PLATFORM if json_data['platform'] == config.IOS_PLATFORM.name else config.ANDROID_PLATFORM
        return GameAccount(
            unique_id=json_data['unique_id'],
            identifier=json_data['identifier'],
        )
