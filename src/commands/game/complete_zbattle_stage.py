import base64
import json
import time
from random import randint

import PySimpleGUI as sg
from colorama import Fore, Style

import config
import crypto
import network
from commands.game.act import refill_stamina_command


def complete_zbattle_stage_command(kagi=False):
    events = network.get_events()

    zbattles_to_display = []
    for event in events['z_battle_stages']:
        zbattle = config.ZBattles.where('z_battle_stage_id', '=', event['id']).first().enemy_name + ' | ' + str(
            event['id'])
        zbattles_to_display.append(zbattle)

    col1 = [[sg.Text('Select a Z-Battle', font=('', 15, 'bold'))],
            [sg.Listbox(values=(zbattles_to_display), size=(30, 15), key='ZBATTLE', font=('', 15, 'bold'))]]

    col2 = [[sg.Text('Select Single Stage:'), sg.Combo(['5', '10', '15', '20', '25', '30'], size=(6, 3), key='LEVEL')],
            [sg.Text('Amount of times: '),
             sg.Spin([i for i in range(1, 999)], initial_value=1, size=(5, None), key='LOOP')],
            [sg.Button(button_text='Go!', key='GO')]]

    layout = [[sg.Column(col1), sg.Column(col2)]]
    window = sg.Window('Medal List').Layout(layout)

    while True:
        event, values = window.Read()
        if event == None:
            window.Close()
            return 0

        if event == 'GO':
            if len(values['ZBATTLE']) == 0:
                print(Fore.RED + Style.BRIGHT + "Select a Z-Battle!")
                continue

            for i in range(int(values['LOOP'])):
                window.Hide()
                window.Refresh()
                #
                stage = values['ZBATTLE'][0].split(' | ')[1]
                level = values['LEVEL']

                ##Get supporters
                r = network.get_zbattles_supporters(str(stage))
                if 'supporters' in r:
                    supporter = r['supporters'][0]['id']
                    leader = r['supporters'][0]['card_id']
                elif 'error' in r:
                    print(Fore.RED + Style.BRIGHT + r)
                    return 0
                else:
                    print(Fore.RED + Style.BRIGHT + 'Problem with ZBattle')
                    print(r)
                    return 0

                ###Send first request
                if kagi == True:
                    sign = json.dumps({
                        'friend_id': int(supporter),
                        'level': int(level),
                        'selected_team_num': int(config.deck),
                        'eventkagi_item_id': 5,
                        'support_leader': {'card_id': int(leader), 'exp': 0, 'optimal_awakening_step': 0,
                                           'released_rate': 0}
                    })
                else:
                    sign = json.dumps({
                        'friend_id': int(supporter),
                        'level': int(level),
                        'selected_team_num': int(config.deck),
                        'support_leader': {'card_id': int(leader), 'exp': 0, 'optimal_awakening_step': 0,
                                           'released_rate': 0}
                    })

                enc_sign = crypto.encrypt_sign(sign)
                r = network.post_zbattles_start(str(stage), enc_sign)

                if 'sign' in r:
                    dec_sign = crypto.decrypt_sign(r['sign'])
                # Check if error was due to lack of stamina
                elif 'error' in r:
                    if r['error']['code'] == 'act_is_not_enough':
                        # Check if allowed to refill stamina
                        if config.allow_stamina_refill == True:
                            refill_stamina_command()
                            r = network.post_zbattles_start(str(stage), enc_sign)
                    else:
                        print(r)
                        return 0
                else:
                    print(Fore.RED + Style.BRIGHT + 'Problem with ZBattle')
                    print(r)
                    return 0

                finish_time = int(round(time.time(), 0) + 2000)
                start_time = finish_time - randint(6200000, 8200000)

                em_hp = []
                em_atk = 0
                for i in dec_sign['enemies'][0]:
                    em_hp.append(i['hp'])
                    em_atk = int(em_atk) + int(i['attack'])

                summary = {
                    'summary': {
                        'enemy_attack': int(em_atk),
                        'enemy_attack_count': 1,
                        'enemy_heal_counts': [0],
                        'enemy_heals': [0],
                        'enemy_max_attack': int(em_atk),
                        'enemy_min_attack': int(em_atk),
                        'player_attack_counts': [3],
                        'player_attacks': em_hp,
                        'player_heal': 0,
                        'player_heal_count': 0,
                        'player_max_attacks': em_hp,
                        'player_min_attacks': em_hp,
                        'type': 'summary'
                    }
                }

                # enc_sign = encrypt_sign(sign)

                r = network.post_zbattles_finish(
                    stage_id=str(stage),
                    elapsed_time=finish_time - start_time,
                    is_cleared=True,
                    level=int(level),
                    reason='win',
                    s='rGAX18h84InCwFGbd/4zr1FvDNKfmo/TJ02pd6onclk=',
                    t=base64.b64encode(json.dumps(summary).encode()).decode(),
                    token=dec_sign['token'],
                    used_items=[],
                    z_battle_started_at_ms=start_time,
                    z_battle_finished_at_ms=finish_time
                )
                dec_sign = crypto.decrypt_sign(r['sign'])
                # ## Print out Items from Database
                print('Level: ' + str(level))
                # ## Print out Items from Database
                if 'items' in dec_sign:
                    supportitems = []
                    awakeningitems = []
                    trainingitems = []
                    potentialitems = []
                    treasureitems = []
                    carditems = []
                    trainingfields = []
                    stones = 0
                    supportitemsset = set()
                    awakeningitemsset = set()
                    trainingitemsset = set()
                    potentialitemsset = set()
                    treasureitemsset = set()
                    carditemsset = set()
                    trainingfieldsset = set()
                    print('Items:')
                    print('-------------------------')
                    if 'quest_clear_rewards' in dec_sign:
                        for x in dec_sign['quest_clear_rewards']:
                            if x['item_type'] == 'Point::Stone':
                                stones += x['amount']
                    for x in dec_sign['items']:
                        if x['item_type'] == 'SupportItem':

                            # print('' + SupportItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                            for i in range(x['quantity']):
                                supportitems.append(x['item_id'])
                            supportitemsset.add(x['item_id'])
                        elif x['item_type'] == 'PotentialItem':

                            # print('' + PotentialItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                            for i in range(x['quantity']):
                                potentialitems.append(x['item_id'])
                            potentialitemsset.add(x['item_id'])
                        elif x['item_type'] == 'TrainingItem':

                            # print('' + TrainingItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                            for i in range(x['quantity']):
                                trainingitems.append(x['item_id'])
                            trainingitemsset.add(x['item_id'])
                        elif x['item_type'] == 'AwakeningItem':

                            # print('' + AwakeningItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                            for i in range(x['quantity']):
                                awakeningitems.append(x['item_id'])
                            awakeningitemsset.add(x['item_id'])
                        elif x['item_type'] == 'TreasureItem':

                            # print('' + TreasureItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                            for i in range(x['quantity']):
                                treasureitems.append(x['item_id'])
                            treasureitemsset.add(x['item_id'])
                        elif x['item_type'] == 'Card':

                            # card = Cards.find(x['item_id'])

                            carditems.append(x['item_id'])
                            carditemsset.add(x['item_id'])
                        elif x['item_type'] == 'Point::Stone':
                            stones += 1
                        elif x['item_type'] == 'TrainingField':

                            # card = Cards.find(x['item_id'])

                            for i in range(x['quantity']):
                                trainingfields.append(x['item_id'])
                            trainingfieldsset.add(x['item_id'])
                        else:
                            print(x['item_type'])

                    # Print items
                    for x in supportitemsset:
                        config.SupportItems.find_or_fail(x).name

                        # Print name and item count
                        print(Fore.CYAN + Style.BRIGHT + config.SupportItems.find(x).name + ' x' \
                              + str(supportitems.count(x)))
                    for x in awakeningitemsset:
                        config.AwakeningItems.find_or_fail(x).name

                        # Print name and item count
                        print(Fore.MAGENTA + Style.BRIGHT + config.AwakeningItems.find(x).name + ' x' \
                              + str(awakeningitems.count(x)))
                    for x in trainingitemsset:
                        config.TrainingItems.find_or_fail(x).name

                        # Print name and item count
                        print(Fore.RED + Style.BRIGHT + config.TrainingItems.find(x).name + ' x' \
                              + str(trainingitems.count(x)))
                    for x in potentialitemsset:
                        config.PotentialItems.find_or_fail(x).name

                        # Print name and item count
                        print(config.PotentialItems.find_or_fail(x).name + ' x' \
                              + str(potentialitems.count(x)))
                    for x in treasureitemsset:
                        config.TreasureItems.find_or_fail(x).name

                        # Print name and item count
                        print(Fore.GREEN + Style.BRIGHT + config.TreasureItems.find(x).name + ' x' \
                              + str(treasureitems.count(x)))
                    for x in trainingfieldsset:
                        config.TrainingFields.find_or_fail(x).name

                        # Print name and item count
                        print(config.TrainingFields.find(x).name + ' x' \
                              + str(trainingfields.count(x)))
                    for x in carditemsset:
                        config.Cards.find_or_fail(x).name

                        # Print name and item count
                        print(config.Cards.find(x).name + ' x' + str(carditems.count(x)))
                    print(Fore.YELLOW + Style.BRIGHT + 'Stones x' + str(stones))
                if 'gasha_point' in dec_sign:
                    print('Friend Points: ' + str(dec_sign['gasha_point']))

                print('--------------------------')
                print('##############################################')
            window.UnHide()
            window.Refresh()
