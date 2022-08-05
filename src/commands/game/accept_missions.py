from colorama import Fore, Style

import network


def accept_missions_command():
    missions = network.get_missions()
    mission_list = []
    for mission in missions['missions']:
        if mission['completed_at'] != None and mission['accepted_reward_at'] == None:
            mission_list.append(mission['id'])

    r = network.post_missions_accept(mission_list)
    if 'error' not in r:
        print(Fore.GREEN + Style.BRIGHT + 'Accepted missions')
