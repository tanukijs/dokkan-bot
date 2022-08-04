import config
import crypto


# Remove key that have a None values
def generate_headers(
  method: str,
  endpoint: str,
  userAgent: str = config.user_agent,
  platform: str = config.platform,
  clientVersion: str = config.gb_version_code,
  language: str = 'en',
  assetVersion: str = '////',
  databaseVersion: str = '////'
) -> "dict[str: any]":
  return {
    'User-Agent': userAgent,
    'Accept': '*/*',
    'Authorization': crypto.mac(method, endpoint),
    'Content-type': 'application/json',
    'X-Platform': platform,
    'X-AssetVersion': assetVersion,
    'X-DatabaseVersion': databaseVersion,
    'X-ClientVersion': clientVersion,
    'X-Language': language
  }
