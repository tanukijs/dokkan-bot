import json
import time
from random import randint

import requests
from colorama import Fore, Style

import config
import crypto
from network.utils import generate_headers


def complete_clash_command():
    print('Fetching current clash...')
    headers = generate_headers('GET', '/resources/home?rmbattles=true')
    url = config.gb_url + '/resources/home?rmbattles=true'
    r = requests.get(url, headers=headers)
    clash_id = r.json()['rmbattles']['id']

    #### dropout
    print('Resetting clash to beginning...')
    headers = generate_headers('POST', '/rmbattles/' + str(clash_id) + '/stages/dropout')
    sign = {
        'reason': "dropout"
    }
    url = config.gb_url + '/rmbattles/' + str(clash_id) + '/stages/dropout'

    r = requests.post(url, data=json.dumps(sign), headers=headers)
    print('Reset complete...')

    print('Fetching list of stages from Bandai...')
    headers = generate_headers('GET', '/rmbattles/' + str(clash_id))
    url = config.gb_url + '/rmbattles/' + str(clash_id)

    r = requests.get(url, headers=headers)

    available_stages = []
    for area in r.json()['level_stages'].values():
        for stage in area:
            available_stages.append(stage['id'])
    print('Stages obtained...')
    print('Asking Bandai for available cards...')
    headers = generate_headers('GET', '/rmbattles/available_user_cards')
    url = config.gb_url + '/rmbattles/available_user_cards'

    r = requests.get(url, headers=headers)
    print('Cards received...')
    available_user_cards = []
    # print(r.json())
    for card in r.json():
        available_user_cards.append(card)
    available_user_cards = available_user_cards[:99]

    if len(available_user_cards) == 0:
        print(Fore.RED + Style.BRIGHT + "Not enough cards to complete Battlefield with!")
        return 0

    is_beginning = True
    # print(available_stages)
    print('Sending Bandai full team...')
    headers = generate_headers('PUT', '/rmbattles/teams/1')
    data = {'user_card_ids': available_user_cards}
    url = config.gb_url + '/rmbattles/teams/1'

    r = requests.put(url, data=json.dumps(data), headers=headers)
    print('Sent!')
    print('')
    print('Commencing Ultimate Clash!')
    print('----------------------------')
    for stage in available_stages:
        leader = available_user_cards[0]
        members = available_user_cards[1]
        sub_leader = available_user_cards[2]

        sign = {
            'is_beginning': is_beginning,
            'user_card_ids': {
                'leader': leader,
                'members': members,
                'sub_leader': sub_leader
            }
        }

        headers = generate_headers('POST', '/rmbattles/' + str(clash_id) + '/stages/' + str(stage) + '/start')
        url = config.gb_url + '/rmbattles/' + str(clash_id) + '/stages/' + str(stage) + '/start'

        r = requests.post(url, data=json.dumps(sign), headers=headers)
        print('Commencing Stage ' + Fore.YELLOW + str(stage))

        is_beginning = False

        ###Second request
        finish_time = int(round(time.time(), 0) + 2000)
        start_time = finish_time - randint(40000000, 50000000)
        if 'sign' in r.json():
            dec_sign = crypto.decrypt_sign(r.json()['sign'])
        enemy_hp = 0
        try:
            for enemy in dec_sign['enemies']:
                enemy_hp += enemy[0]['hp']
            # can also use this instead... -k1mpl0s
            hp = dec_sign['continuous_info']['remaining_hp']
            round = dec_sign['continuous_info']['round']
        except:
            print('nah')

        sign = {
            'damage': enemy_hp,
            'finished_at_ms': finish_time,
            'finished_reason': 'win',
            'is_cleared': True,
            'remaining_hp': 0,
            'round': int(round),
            'started_at_ms': start_time,
            'token': dec_sign['token']
        }

        headers = generate_headers('POST', '/rmbattles/' + str(clash_id) + '/stages/finish')
        url = config.gb_url + '/rmbattles/' + str(clash_id) + '/stages/finish'

        r = requests.post(url, data=json.dumps(sign), headers=headers)
        print('Completed Stage ' + Fore.YELLOW + str(stage))

        headers = generate_headers('GET', '/rmbattles/teams/1')
        url = config.gb_url + '/rmbattles/teams/1'

        r = requests.get(url, headers=headers)
        print('----------------------------')
        if 'sortiable_user_card_ids' not in r.json():
            return 0
        available_user_cards = r.json()['sortiable_user_card_ids']
