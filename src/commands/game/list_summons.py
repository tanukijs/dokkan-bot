import re

import requests
from colorama import Fore

import config
from network.utils import generate_headers


def list_summons_command():
  # Prints current available summons, could be formatted better but meh

  headers = generate_headers('GET', '/gashas')
  url = config.game_env.url + '/gashas'

  r = requests.get(url, headers=headers)

  for gasha in r.json()['gashas']:
    print(gasha['name'].replace('\n', ' ') + ' ' + str(gasha['id']))
    if len(gasha['description']) > 0:
      print(Fore.YELLOW + re.sub(r'\{[^{}]*\}', "", gasha['description']).replace('\n', ' '))
