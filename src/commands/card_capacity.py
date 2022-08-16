from colorama import Fore, Style

import network
from config import GameContext

NAME = 'card capacity'
DESCRIPTION = 'Increases card capacity by 5'
CONTEXT = [GameContext.GAME]


def run():
    req = network.post_user_capacity_card()
    if 'error' in req:
        print(Fore.RED + Style.BRIGHT + str(req))
    else:
        print(Fore.GREEN + Style.BRIGHT + 'Card capacity +5')
