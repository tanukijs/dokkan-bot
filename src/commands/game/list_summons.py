import re

from colorama import Fore

import network


def list_summons_command():
    # Prints current available summons, could be formatted better but meh
    r = network.get_gashas()

    for gasha in r['gashas']:
        print(gasha['name'].replace('\n', ' ') + ' ' + str(gasha['id']))
        if len(gasha['description']) > 0:
            print(Fore.YELLOW + re.sub(r'\{[^{}]*\}', "", gasha['description']).replace('\n', ' '))
