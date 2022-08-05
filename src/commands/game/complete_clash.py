import time
from random import randint

from colorama import Fore, Style

import crypto
import network


def complete_clash_command():
    print('Fetching current clash...')
    r = network.get_resources_home(rmbattles=True)
    clash_id = r['rmbattles']['id']

    #### dropout
    print('Resetting clash to beginning...')
    network.post_rmbattles_dropout(str(clash_id))
    print('Reset complete...')

    print('Fetching list of stages from Bandai...')
    r = network.get_rmbattles(str(clash_id))

    available_stages = []
    for area in r['level_stages'].values():
        for stage in area:
            available_stages.append(stage['id'])
    print('Stages obtained...')
    print('Asking Bandai for available cards...')
    r = network.get_rmbattles_available_user_cards()
    print('Cards received...')
    available_user_cards = []
    for card in r:
        available_user_cards.append(card)
    available_user_cards = available_user_cards[:99]

    if len(available_user_cards) == 0:
        print(Fore.RED + Style.BRIGHT + "Not enough cards to complete Battlefield with!")
        return 0

    is_beginning = True
    # print(available_stages)
    print('Sending Bandai full team...')
    network.put_rmbattles_team('1', available_user_cards)
    print('Sent!')
    print('')
    print('Commencing Ultimate Clash!')
    print('----------------------------')
    for stage in available_stages:
        leader = available_user_cards[0]
        members = available_user_cards[1]
        sub_leader = available_user_cards[2]

        r = network.post_rmbattles_start(str(clash_id), str(stage), is_beginning, leader, members, sub_leader)
        print('Commencing Stage ' + Fore.YELLOW + str(stage))

        is_beginning = False

        ###Second request
        finish_time = int(round(time.time(), 0) + 2000)
        start_time = finish_time - randint(40000000, 50000000)
        if 'sign' in r:
            dec_sign = crypto.decrypt_sign(r['sign'])
        enemy_hp = 0
        try:
            for enemy in dec_sign['enemies']:
                enemy_hp += enemy[0]['hp']
            # can also use this instead... -k1mpl0s
            hp = dec_sign['continuous_info']['remaining_hp']
            round = dec_sign['continuous_info']['round']
        except:
            print('nah')

        network.post_rmbattles_finish(
            clash_id=str(clash_id),
            damage=enemy_hp,
            finished_at_ms=finish_time,
            finished_reason='win',
            is_cleared=True,
            remaining_hp=0,
            round=int(round),
            started_at_ms=start_time,
            token=dec_sign['token']
        )
        print('Completed Stage ' + Fore.YELLOW + str(stage))

        r = network.get_rmbattles_teams('1')
        print('----------------------------')
        if 'sortiable_user_card_ids' not in r:
            return 0
        available_user_cards = r['sortiable_user_card_ids']
