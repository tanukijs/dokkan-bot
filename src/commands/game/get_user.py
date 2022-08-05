import requests

import config
from network.utils import generate_headers


def get_user_command():
  # Returns user response from bandai

  headers = generate_headers('GET', '/user')
  url = config.game_env.url + '/user'
  r = requests.get(url, headers=headers)
  return r.json()
