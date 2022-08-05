import json

import requests
from colorama import Fore, Style

import config
from network.utils import generate_headers


def accept_gifts_command():
    # Gets Gift Ids
    headers = generate_headers('GET', '/gifts')
    url = config.game_env.url + '/gifts'
    r = requests.get(url, headers=headers)

    gifts = []
    for x in r.json()['gifts']:
        gifts.append(x['id'])

    # AcceptGifts
    if len(gifts) == 0:
        print('No gifts to accept...')
        return 0
    headers = generate_headers('POST', '/gifts/accept')
    url = config.game_env.url + '/gifts/accept'

    chunks = [gifts[x:x + 25] for x in range(0, len(gifts), 25)]
    for data in chunks:
        data = {'gift_ids': data}
        r = requests.post(url, data=json.dumps(data), headers=headers)
    if 'error' not in r.json():
        print(Fore.GREEN + Style.BRIGHT + 'Gifts Accepted...')
    else:
        print(r.json())
