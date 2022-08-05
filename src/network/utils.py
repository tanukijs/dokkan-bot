import config
import crypto


# Remove key that have a None values
from classes.GameEnvironment import GamePlatform


def generate_headers(
    method: str,
    endpoint: str,
    platform: GamePlatform = config.game_platform,
    client_version: str = config.game_env.version_code,
    language: str = 'en',
    asset_version: str = '////',
    database_version: str = '////'
) -> "dict[str: any]":
  return {
    'User-Agent': platform.user_agent,
    'Accept': '*/*',
    'Authorization': crypto.mac(method, endpoint),
    'Content-type': 'application/json',
    'X-Platform': platform.name,
    'X-AssetVersion': asset_version,
    'X-DatabaseVersion': database_version,
    'X-ClientVersion': client_version,
    'X-Language': language
  }
