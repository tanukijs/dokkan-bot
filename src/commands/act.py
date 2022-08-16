from colorama import Fore, Style

import network
from config import GameContext

NAME = 'act'
DESCRIPTION = 'Restore max act'
CONTEXT = [GameContext.GAME]


def run():
    stones = network.get_user()['user']['stone']
    if stones < 1:
        print(Fore.RED + Style.BRIGHT + 'You have no stones left...')
        return 0

    network.put_user_recover_act_with_stones()
    print(Fore.GREEN + Style.BRIGHT + 'STAMINA RESTORED')
