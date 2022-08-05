import json

import requests

import config
from network.utils import generate_headers


def change_name_command():
  # Changes name associated with account
  headers = generate_headers('PUT', '/user')
  name = input('What would you like to change your name to?: ')
  user = {'user': {'name': name}}
  url = config.game_env.url + '/user'
  r = requests.put(url, data=json.dumps(user), headers=headers)
  if 'error' in r.json():
    print(r.json())
  else:
    print("Name changed to: " + name)
