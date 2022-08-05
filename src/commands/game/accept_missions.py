import json

import requests
from colorama import Fore, Style

import config
from network.utils import generate_headers


def accept_missions_command():
  # Accept all remaining missions

  headers = generate_headers('GET', '/missions')
  url = config.game_env.url + '/missions'
  r = requests.get(url, headers=headers)
  missions = r.json()
  mission_list = []
  for mission in missions['missions']:
    if mission['completed_at'] != None and mission['accepted_reward_at'] == None:
      mission_list.append(mission['id'])

  headers = generate_headers('POST', '/missions/accept')
  url = config.game_env.url + '/missions/accept'
  data = {"mission_ids": mission_list}
  r = requests.post(url, data=json.dumps(data), headers=headers)
  if 'error' not in r.json():
    print(Fore.GREEN + Style.BRIGHT + 'Accepted missions')
