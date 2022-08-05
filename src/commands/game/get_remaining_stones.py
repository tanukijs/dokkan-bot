import requests

import config
from network.utils import generate_headers


def get_remaining_stones_command():
  # ## Returns User possessed stones

  headers = generate_headers('GET', '/user')
  url = config.game_env.url + '/user'
  r = requests.get(url, headers=headers)
  user = r.json()

  return 'Stones: ' + str(user['user']['stone'])
