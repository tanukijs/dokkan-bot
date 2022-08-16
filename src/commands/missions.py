from colorama import Fore, Style

import network
from config import GameContext

NAME = 'missions'
DESCRIPTION = 'Accept missions rewards'
CONTEXT = [GameContext.GAME]


def run():
    req = network.get_missions()
    mission_list = []
    for mission in req['missions']:
        if mission['completed_at'] is not None and mission['accepted_reward_at'] is None:
            mission_list.append(mission['id'])

    req = network.post_missions_accept(mission_list)
    if 'error' not in req:
        print(Fore.GREEN + Style.BRIGHT + 'Accepted missions')
