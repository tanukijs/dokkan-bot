import json

import requests
from colorama import Fore, Style

import config
from commands.game.complete_stage import complete_stage_command
from network.utils import generate_headers


def dragonballs_command():
    is_got = 0
    ###Check for Dragonballs
    headers = generate_headers('GET', '/dragonball_sets')
    url = config.game_env.url + '/dragonball_sets'
    r = requests.get(url, headers=headers)
    if 'error' in r.json():
        print(Fore.RED + Style.BRIGHT + str(r.json()))
        return 0

    ####Determine which dragonball set is being used
    set = r.json()['dragonball_sets'][0]['id']

    ### Complete stages and count dragonballs
    for dragonball in r.json()['dragonball_sets']:
        for db in reversed(dragonball['dragonballs']):
            if db['is_got'] == True:
                is_got += 1
            elif db['is_got'] == False:
                is_got += 1
                complete_stage_command(str(db['quest_id']), db['difficulties'][0])

    ### If all dragonballs found then wish
    if is_got == 7:
        headers = generate_headers('GET', '/dragonball_sets/' + str(set) + '/wishes')
        url = config.game_env.url + '/dragonball_sets/' + str(set) + '/wishes'

        r = requests.get(url, headers=headers)
        if 'error' in r.json():
            print(Fore.RED + Style.BRIGHT + str(r.json()))
            return 0
        wish_ids = []
        for wish in r.json()['dragonball_wishes']:
            if wish['is_wishable']:
                print('#########################')
                print('Wish ID: ' + str(wish['id']))
                wish_ids.append(str(wish['id']))
                print(wish['title'])
                print(wish['description'])
                print('')

        print(Fore.YELLOW + 'What wish would you like to ask shenron for? ID: ', end='')
        choice = input()
        while choice not in wish_ids:
            print("Shenron did not understand you! ID: ", end='')
            choice = input()
        wish_ids[:] = []
        headers = generate_headers('POST', '/dragonball_sets/' + str(set) + '/wishes')
        url = config.game_env.url + '/dragonball_sets/' + str(set) + '/wishes'
        data = {'dragonball_wish_ids': [int(choice)]}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if 'error' in r.json():
            print(Fore.RED + Style.BRIGHT + str(r.json()))
        else:
            print(Fore.YELLOW + 'Wish granted!')
            print('')

        dragonballs_command()

        return 0
