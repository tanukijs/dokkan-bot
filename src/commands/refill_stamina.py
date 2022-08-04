import requests
from colorama import Fore, Style

import config
from commands.get_user import get_user_command
from network.utils import generate_headers


def refill_stamina_command():
    # ## Restore user stamina

    stones = get_user_command()['user']['stone']
    if stones < 1:
        print(Fore.RED + Style.BRIGHT + 'You have no stones left...')
        return 0
    headers = generate_headers('PUT', '/user/recover_act_with_stone')
    url = config.gb_url + '/user/recover_act_with_stone'

    r = requests.put(url, headers=headers)
    print(Fore.GREEN + Style.BRIGHT + 'STAMINA RESTORED')
