import base64
import json
import webbrowser

import requests
from typing import Optional
from colorama import Fore, Style

import config
import crypto
from classes.Game import GameAccount
from commands.auth.set_platform import set_platform_command


def signup_command(reroll_state) -> "Optional[GameAccount]":
  set_platform_command(reroll_state)
  guid = crypto.guid()

  user_acc = {
    'ad_id': guid['AdId'],
    'unique_id': guid['UniqueId'],
    'country': 'AU',
    'currency': 'AUD',
    'device': config.game_platform.device_name,
    'device_model': config.game_platform.device_model,
    'os_version': config.game_platform.os_version,
    'platform': config.game_platform.name,
  }
  user_account = json.dumps({'user_account': user_acc})

  headers = {
    'User-Agent': config.game_platform.user_agent,
    'Accept': '*/*',
    'Content-type': 'application/json',
    'X-Platform': config.game_platform.name,
    'X-ClientVersion': config.game_env.version_code,
  }
  url = config.game_env.url + '/auth/sign_up'
  r = requests.post(url, data=user_account, headers=headers)

  # It is now necessary to solve the captcha. Opens browser window
  # in order to solve it. Script waits for user input before continuing
  print(r.json())
  if 'captcha_url' not in r.json():
    print(Fore.RED + Style.BRIGHT + 'Captcha could not be loaded...')
    return None

  url = r.json()['captcha_url']
  webbrowser.open(url, new=2)
  captcha_session_key = r.json()['captcha_session_key']
  print(
    'Opening captcha in browser. Press' + Fore.RED + Style.BRIGHT + ' ENTER ' + Style.RESET_ALL + 'once you have solved it...')
  input()

  # ## Query sign up again passing the captcha session key.
  # ## Bandais servers check if captcha was solved relative to the session key

  data = {'captcha_session_key': captcha_session_key,
          'user_account': user_acc}

  url = config.game_env.url + '/auth/sign_up'

  r = requests.post(url, data=json.dumps(data), headers=headers)

  # ##Return identifier for account, this changes upon transferring account
  try:
    identifier = base64.b64decode(r.json()['identifier']).decode('utf-8')
    return GameAccount(
      ad_id=guid['AdId'],
      unique_id=guid['UniqueId'],
      identifier=identifier
    )
  except:
    return None
