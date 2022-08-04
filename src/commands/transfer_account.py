import base64
import json

import requests

import config
import crypto
from commands.refresh_client import refresh_client_command
from commands.save_account import save_account_command
from commands.set_platform import set_platform_command


def transfer_account_command():
    # Determine correct platform to use
    set_platform_command()

    transfercode = input('Enter your transfer code: ')

    config.AdId = crypto.guid()['AdId']
    config.UniqueId = crypto.guid()['UniqueId']
    headers = {
        'User-Agent': config.user_agent,
        'Accept': '*/*',
        'Content-type': 'application/json',
        'X-Platform': config.platform,
        'X-AssetVersion': '////',
        'X-DatabaseVersion': '////',
        'X-ClientVersion': config.gb_version_code,
    }
    if config.platform == 'android':
        device_name = 'SM'
        device_model = 'SM-E7000'
        os_version = '7.0'
    else:
        device_name = 'iPhone'
        device_model = 'iPhone XR'
        os_version = '13.0'
    data = {'eternal': True, 'old_user_id': '', 'user_account': {
        'device': device_name,
        'device_model': device_model,
        'os_version': os_version,
        'platform': config.platform,
        'unique_id': config.UniqueId,
    }}
    url = config.gb_url + '/auth/link_codes/' + str(transfercode)
    print('URL: ' + url)
    r = requests.put(url, data=json.dumps(data), headers=headers)
    if 'error' in r.json():
        print(r.json())
    print(base64.b64decode(r.json()['identifiers']).decode('utf-8'))
    config.identifier = base64.b64decode(r.json()['identifiers']).decode('utf-8')

    save_account_command()
    refresh_client_command()
