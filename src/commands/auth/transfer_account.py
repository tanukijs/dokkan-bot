import base64
import json

import requests

import config
import crypto
from commands.auth.save_account import save_account_command
from commands.auth.set_platform import set_platform_command
from commands.game.refresh_client import refresh_client_command


def transfer_account_command():
  # Determine correct platform to use
  set_platform_command()

  transfercode = input('Enter your transfer code: ')

  config.AdId = crypto.guid()['AdId']
  config.UniqueId = crypto.guid()['UniqueId']
  headers = {
    'User-Agent': config.game_platform.user_agent,
    'Accept': '*/*',
    'Content-type': 'application/json',
    'X-Platform': config.game_platform.name,
    'X-AssetVersion': '////',
    'X-DatabaseVersion': '////',
    'X-ClientVersion': config.game_env.version_code,
  }

  data = {'eternal': True, 'old_user_id': '', 'user_account': {
    'device': config.game_platform.device_name,
    'device_model': config.game_platform.device_model,
    'os_version': config.game_platform.os_version,
    'platform': config.game_platform.name,
    'unique_id': config.UniqueId,
  }}
  url = config.game_env.url + '/auth/link_codes/' + str(transfercode)
  print('URL: ' + url)
  r = requests.put(url, data=json.dumps(data), headers=headers)
  if 'error' in r.json():
    print(r.json())
  print(base64.b64decode(r.json()['identifiers']).decode('utf-8'))
  config.identifier = base64.b64decode(r.json()['identifiers']).decode('utf-8')

  save_account_command()
  refresh_client_command()
