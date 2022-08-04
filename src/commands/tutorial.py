import json

import requests
from colorama import Fore, Style

import config
from network.utils import generate_headers


def tutorial_command():
    # ##Progress NULL TUTORIAL FINISH

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 1/8')
    headers = generate_headers('PUT', '/tutorial/finish')
    url = config.gb_url + '/tutorial/finish'
    r = requests.put(url, headers=headers)

    # ##Progress NULL Gasha

    headers = generate_headers('POST', '/tutorial/gasha')
    url = config.gb_url + '/tutorial/gasha'
    r = requests.post(url, headers=headers)
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 2/8')

    # ##Progress to 999%

    headers = generate_headers('PUT', '/tutorial')
    progress = {'progress': '999'}
    url = config.gb_url + '/tutorial'
    r = requests.put(url, data=json.dumps(progress), headers=headers)
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 3/8')

    # ##Change User name

    headers = generate_headers('PUT', '/user')
    user = {'user': {'name': 'Ninja'}}
    url = config.gb_url + '/user'
    r = requests.put(url, data=json.dumps(user), headers=headers)
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 4/8')

    # ##/missions/put_forward

    headers = generate_headers('POST', '/missions/put_forward')
    url = config.gb_url + '/missions/put_forward'
    r = requests.post(url, headers=headers)
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 5/8')

    # ##Apologies accept

    headers = generate_headers('PUT', '/apologies/accept')
    url = config.gb_url + '/apologies/accept'
    r = requests.put(url, headers=headers)

    # ##On Demand

    headers = generate_headers('PUT', '/user')
    url = config.gb_url + '/user'
    data = {'user': {'is_ondemand': True}}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 6/8')

    # ##Hidden potential releasable

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 7/8')
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 8/8')
    print(Fore.RED + Style.BRIGHT + 'TUTORIAL COMPLETE')
