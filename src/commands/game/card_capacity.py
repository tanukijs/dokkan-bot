from colorama import Fore, Style

import network

NAME = 'card_capacity'
DESCRIPTION = 'Increases card capacity by 5'


def run():
    req = network.post_user_capacity_card()
    if 'error' in req:
        print(Fore.RED + Style.BRIGHT + str(req))
    else:
        print(Fore.GREEN + Style.BRIGHT + 'Card capacity +5')
