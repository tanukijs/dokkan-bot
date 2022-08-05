import json
import random
import time
from random import randint

import requests
from colorama import Fore, Style

import config
import crypto
from commands.game.get_friend import get_friend_command
from commands.game.refill_stamina import refill_stamina_command
from commands.game.sell_cards import sell_cards_command
from network.utils import generate_headers


def complete_stage_command(stage_id, difficulty, kagi=None):
  # Completes a given stage stage name or ID has been supplied as a string
  # kagi must be correct kagi item ID if used
  # Check if user has supplied a stage name and searches DB for correct stage id
  if not stage_id.isnumeric():
    try:
      config.Model.set_connection_resolver(config.game_env.db_manager)
      stage_id = str(config.Quests.where('name', 'like', '%' + stage_id
                                         + '%').first().id)
    except:
      print(Fore.RED + Style.BRIGHT + "Could not find stage name in databases")
      return 0
  # Retrieve correct stage name to print
  # Check if GLB database has id, if not try JP DB.

  config.Model.set_connection_resolver(config.game_env.db_manager)
  config.Quests.find_or_fail(int(stage_id))
  stage_name = config.Quests.find_or_fail(int(stage_id)).name

  try:
    print('Begin stage: ' + stage_name + ' ' + stage_id + ' | Difficulty: ' \
          + str(difficulty) + ' Deck: ' + str(config.deck))
  except:
    print(Fore.RED + Style.BRIGHT + 'Does this quest exist?')
    return 0

  # Begin timer for overall stage completion, rounded to second.
  timer_start = int(round(time.time(), 0))

  # Form First Request
  APIToken = ''.join(
    random.choice(list('abcdefghijklmnopqrstuvwxyzBCDEFGHIKLMNOPQRUVWXYZ123456789-_')) for i in range(63))
  friend = get_friend_command(stage_id, difficulty)

  if friend['is_cpu'] == False:
    if kagi != None:
      sign = json.dumps({'difficulty': int(difficulty), 'eventkagi_item_id': kagi, 'friend_id': int(friend['id']),
                         'is_playing_script': True, 'selected_team_num': int(config.deck),
                         'support_leader': {'card_id': int(friend['leader']), 'exp': 0, 'optimal_awakening_step': 0,
                                            'released_rate': 0}})
    else:
      sign = json.dumps({'difficulty': int(difficulty), 'friend_id': int(friend['id']), 'is_playing_script': True,
                         'selected_team_num': int(config.deck),
                         'support_leader': {'card_id': int(friend['leader']), 'exp': 0, 'optimal_awakening_step': 0,
                                            'released_rate': 0}})
  else:
    if kagi != None:
      sign = json.dumps({'difficulty': int(difficulty), 'eventkagi_item_id': kagi, 'cpu_friend_id': int(friend['id']),
                         'is_playing_script': True, 'selected_team_num': int(config.deck)})
    else:
      sign = json.dumps({'difficulty': int(difficulty), 'cpu_friend_id': int(friend['id']), 'is_playing_script': True,
                         'selected_team_num': int(config.deck)})

  enc_sign = crypto.encrypt_sign(sign)

  # ## Send First Request

  headers = generate_headers('POST', '/quests/${stage_id}/sugoroku_maps/start')
  data = {'sign': enc_sign}

  url = config.game_env.url + '/quests/' + stage_id + '/sugoroku_maps/start'

  r = requests.post(url, data=json.dumps(data), headers=headers)

  # Form second request
  # Time for request sent

  if 'sign' in r.json():
    dec_sign = crypto.decrypt_sign(r.json()['sign'])
  elif 'error' in r.json():
    print(Fore.RED + Style.BRIGHT + str(r.json()['error']))
    # Check if error was due to lack of stamina
    if r.json()['error']['code'] == 'act_is_not_enough':
      # Check if allowed to refill stamina
      if config.allow_stamina_refill == True:
        refill_stamina_command()
        r = requests.post(url, data=json.dumps(data),
                          headers=headers)
      else:
        print(Fore.RED + Style.BRIGHT + 'Stamina refill not allowed.')
        return 0
    elif r.json()['error']['code'] == 'active_record/record_not_found':
      return 0
    elif r.json()['error']['code'] == 'invalid_area_conditions_potential_releasable':
      print(Fore.RED + Style.BRIGHT + 'You do not meet the coniditions to complete potential events')
      return 0
    else:
      print(Fore.RED + Style.BRIGHT + str(r.json()['error']))
      return 0
  else:
    print(Fore.RED + Style.BRIGHT + str(r.json()))
    return 0
  if 'sign' in r.json():
    dec_sign = crypto.decrypt_sign(r.json()['sign'])
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

  # Send second request

  headers = generate_headers('POST', '/quests/' + stage_id + '/sugoroku_maps/finish')
  data = {'sign': enc_sign}
  url = config.game_env.url + '/quests/' + stage_id \
        + '/sugoroku_maps/finish'

  r = requests.post(url, data=json.dumps(data), headers=headers)
  dec_sign = crypto.decrypt_sign(r.json()['sign'])

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

        #                print('' + card.name + '['+rarity+']'+ ' x '+str(x['quantity']))
        # print('' + TreasureItems.find(x['item_id']).name + ' x '+str(x['quantity']))

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
      # JP Translation
      config.Model.set_connection_resolver(config.game_env.db_manager)
      config.SupportItems.find_or_fail(x).name

      # Print name and item count
      print(Fore.CYAN + Style.BRIGHT + config.SupportItems.find(x).name + ' x' \
            + str(supportitems.count(x)))
    for x in awakeningitemsset:
      # JP Translation
      config.Model.set_connection_resolver(config.game_env.db_manager)
      config.AwakeningItems.find_or_fail(x).name

      # Print name and item count
      print(Fore.MAGENTA + Style.BRIGHT + config.AwakeningItems.find(x).name + ' x' \
            + str(awakeningitems.count(x)))
    for x in trainingitemsset:
      # JP Translation
      config.Model.set_connection_resolver(config.game_env.db_manager)
      config.TrainingItems.find_or_fail(x).name

      # Print name and item count
      print(Fore.RED + Style.BRIGHT + config.TrainingItems.find(x).name + ' x' \
            + str(trainingitems.count(x)))
    for x in potentialitemsset:
      # JP Translation
      config.Model.set_connection_resolver(config.game_env.db_manager)
      config.PotentialItems.find_or_fail(x).name

      # Print name and item count
      print(config.PotentialItems.find_or_fail(x).name + ' x' \
            + str(potentialitems.count(x)))
    for x in treasureitemsset:
      # JP Translation
      config.Model.set_connection_resolver(config.game_env.db_manager)
      config.TreasureItems.find_or_fail(x).name

      # Print name and item count
      print(Fore.GREEN + Style.BRIGHT + config.TreasureItems.find(x).name + ' x' \
            + str(treasureitems.count(x)))
    for x in trainingfieldsset:
      # JP Translation
      config.Model.set_connection_resolver(config.game_env.db_manager)
      config.TrainingFields.find_or_fail(x).name

      # Print name and item count
      print(config.TrainingFields.find(x).name + ' x' \
            + str(trainingfields.count(x)))
    for x in carditemsset:
      # JP Translation
      config.Model.set_connection_resolver(config.game_env.db_manager)
      config.Cards.find_or_fail(x).name

      # Print name and item count
      print(config.Cards.find(x).name + ' x' + str(carditems.count(x)))
    print(Fore.YELLOW + Style.BRIGHT + 'Stones x' + str(stones))
  zeni = '{:,}'.format(dec_sign['zeni'])
  print('Zeni: ' + zeni)
  if 'gasha_point' in dec_sign:
    print('Friend Points: ' + str(dec_sign['gasha_point']))

  print('--------------------------')

  # Sell Cards

  i = 0
  card_list = []
  if 'user_items' in dec_sign:
    if 'cards' in dec_sign['user_items']:
      for x in dec_sign['user_items']['cards']:
        if config.Cards.find(x['card_id']).rarity == 0:
          card_list.append(x['id'])

  if len(card_list) > 0:
    sell_cards_command(card_list)

  # ## Finish timing level

  timer_finish = int(round(time.time(), 0))
  timer_total = timer_finish - timer_start

  # #### COMPLETED STAGE

  print(Fore.GREEN + Style.BRIGHT + 'Completed stage: ' + str(stage_id) + ' in ' \
        + str(timer_total) + ' seconds')
  print('##############################################')
