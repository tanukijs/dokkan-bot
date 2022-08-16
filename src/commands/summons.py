import re

from colorama import Fore

import network
from config import GameContext

NAME = 'summons'
DESCRIPTION = 'List available summons'
CONTEXT = [GameContext.GAME]


def run():
    res = network.get_gashas()
    for gasha in res['gashas']:
        summon_id = str(gasha['id'])
        summon_name = Fore.GREEN + gasha['name'].replace('\n', ' ') + Fore.RESET
        summon_description = re.sub(r'\{[^{}]*\}', "", gasha['description']).replace('\n', ' ')
        print(summon_id, summon_name, summon_description)
