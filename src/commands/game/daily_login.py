import requests

import config
from network.utils import generate_headers


def daily_login_command():
    # ## Accepts Outstanding Login Bonuses
    headers = generate_headers('GET',
                               '/resources/home?apologies=true&banners=true&bonus_schedules=true&budokai=true&comeback_campaigns=true&gifts=true&login_bonuses=true&rmbattles=true')
    url = config.game_env.url + '/resources/home?apologies=true&banners=true&bonus_schedules=true&budokai=true&comeback_campaigns=true&gifts=true&login_bonuses=true&rmbattles=true'
    r = requests.get(url, headers=headers)
    if 'error' in r.json():
        print(r.json())

    headers = generate_headers('POST', '/login_bonuses/accept')
    url = config.game_env.url + '/login_bonuses/accept'

    r = requests.post(url, headers=headers)
    if 'error' in r.json():
        print(r.json())
