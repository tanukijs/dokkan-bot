import json

import requests

import config
from network.utils import generate_headers


def sell_cards_command(card_list):
    # Takes cards list and sells them in batches of 99

    headers = generate_headers('POST', '/cards/sell')
    url = config.gb_url + '/cards/sell'

    cards_to_sell = []
    i = 0
    for card in card_list:
        i += 1
        cards_to_sell.append(card)
        if i == 99:
            data = {'card_ids': cards_to_sell}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            print('Sold Cards x' + str(len(cards_to_sell)))
            if 'error' in r.json():
                print(r.json()['error'])
                return 0
            i = 0
            cards_to_sell[:] = []
    if i != 0:
        data = {'card_ids': cards_to_sell}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print('Sold Cards x' + str(len(cards_to_sell)))
    # print(r.json())
