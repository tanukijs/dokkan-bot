import requests

import config
from network.utils import generate_headers


def get_user_info_command():
    # ## Returns User dictionary and info

    headers = generate_headers('GET', '/user')
    url = config.game_env.url + '/user'
    r = requests.get(url, headers=headers)
    user = r.json()

    print('Account OS: ' + config.game_platform.name)
    print('User ID: ' + str(user['user']['id']))
    print('Stones: ' + str(user['user']['stone']))
    print('Zeni: ' + str(user['user']['zeni']))
    print('Rank: ' + str(user['user']['rank']))
    print('Stamina: ' + str(user['user']['act']))
    print('Name: ' + str(user['user']['name']))
    print('Total Card Capacity: ' + str(user['user']['total_card_capacity']))
