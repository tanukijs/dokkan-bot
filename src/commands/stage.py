import json
import time
from random import randint
from typing import Optional

from colorama import Fore, Style

import config
import crypto
import network
from commands import act
from services.stage import StageService

NAME = 'stage'
DESCRIPTION = 'Completes the given stage'
CONTEXT = [config.GameContext.GAME]


def run(stage_id: int, difficulty: int, kagi: Optional[int] = None):
    try:
        stage = config.Quests.find_or_fail(stage_id)
    except:
        print('Does this quest exist ?')
        return

    print('Begin stage: ' + stage.name + ' ' + str(stage_id) + ' | Difficulty: ' + str(difficulty) + ' Deck: ' + str(config.deck))
    # Begin timer for overall stage completion, rounded to second.
    timer_start = int(round(time.time(), 0))

    # Form First Request
    friend = StageService.get_friend(stage_id, difficulty)
    sign = StageService.get_sign(
        friend=friend,
        kagi=kagi,
        difficulty=difficulty,
        selected_team_num=config.deck,
    )

    enc_sign = crypto.encrypt_sign(json.dumps(sign))
    r = network.post_quests_sugoroku_start(stage_id, enc_sign)

    # Form second request
    # Time for request sent

    if 'sign' in r:
        dec_sign = crypto.decrypt_sign(r['sign'])
    elif 'error' in r:
        print(Fore.RED + Style.BRIGHT + str(r['error']))
        # Check if error was due to lack of stamina
        if r['error']['code'] == 'act_is_not_enough':
            # Check if allowed to refill stamina
            if config.allow_stamina_refill:
                act.run()
                r = network.post_quests_sugoroku_start(stage_id, enc_sign)
            else:
                print(Fore.RED + Style.BRIGHT + 'Stamina refill not allowed.')
                return 0
        elif r['error']['code'] == 'active_record/record_not_found':
            return 0
        elif r['error']['code'] == 'invalid_area_conditions_potential_releasable':
            print(Fore.RED + Style.BRIGHT + 'You do not meet the conditions to complete potential events')
            return 0
        else:
            print(Fore.RED + Style.BRIGHT + str(r['error']))
            return 0
    else:
        print(Fore.RED + Style.BRIGHT + str(r))
        return 0

    if 'sign' in r:
        dec_sign = crypto.decrypt_sign(r['sign'])

    # Retrieve possible tile steps from response
    steps = []
    defeated = []
    for i in dec_sign['sugoroku']['events']:
        steps.append(i)
        if 'battle_info' in dec_sign['sugoroku']['events'][i]['content']:
            for j in dec_sign['sugoroku']['events'][i]['content']['battle_info']:
                defeated.append(j['round_id'])

    finish_time = int(round(time.time(), 0) + 2000)
    start_time = finish_time - randint(6200000, 8200000)
    damage = randint(500000, 1000000)

    # Hercule punching bag event damage
    if str(stage_id)[0:3] in ('711', '185', '186', '187'):
        damage = randint(100000000, 101000000)

    sign = {
        'actual_steps': steps,
        'difficulty': difficulty,
        'elapsed_time': finish_time - start_time,
        'energy_ball_counts_in_boss_battle': [4, 6, 0, 6, 4, 3, 0, 0, 0, 0, 0, 0, 0, ],
        'has_player_been_taken_damage': False,
        'is_cheat_user': False,
        'is_cleared': True,
        'is_defeated_boss': True,
        'is_player_special_attack_only': True,
        'max_damage_to_boss': damage,
        'min_turn_in_boss_battle': len(defeated),
        'passed_round_ids': defeated,
        'quest_finished_at_ms': finish_time,
        'quest_started_at_ms': start_time,
        'steps': steps,
        'token': dec_sign['token'],
    }

    enc_sign = crypto.encrypt_sign(json.dumps(sign))
    r = network.post_quests_sugoroku_finish(stage_id, enc_sign)
    dec_sign = crypto.decrypt_sign(r['sign'])
    StageService.print_rewards(dec_sign)

    timer_finish = int(round(time.time(), 0))
    timer_total = timer_finish - timer_start
    print(Fore.GREEN + Style.BRIGHT + 'Completed stage ' + str(stage_id) + ' in ' + str(timer_total) + ' seconds')
