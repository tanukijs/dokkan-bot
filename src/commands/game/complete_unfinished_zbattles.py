import json
import time
from random import randint

import requests
from colorama import Fore, Style

import config
import crypto
from commands.game.refill_stamina import refill_stamina_command
from commands.game.refresh_client import refresh_client_command
from network.utils import generate_headers


def complete_unfinished_zbattles_command(kagi=False):
  # JP Translated
  headers = generate_headers('GET', '/events')
  url = config.game_env.url + '/events'
  r = requests.get(url, headers=headers)
  events = r.json()
  try:
    for event in events['z_battle_stages']:
      config.Model.set_connection_resolver(config.game_env.db_manager)
      x = config.ZBattles.where('z_battle_stage_id', '=', event['id']).first().enemy_name
      print(config.ZBattles.where('z_battle_stage_id', '=', event['id']).first().enemy_name, end='')
      print(Fore.CYAN + Style.BRIGHT + ' | ID: ' + str(event['id']))

      # Get current zbattle level
      headers = generate_headers('GET', '/user_areas')
      url = config.game_env.url + '/user_areas'
      r = requests.get(url, headers=headers)
      if 'user_z_battles' in r.json():
        zbattles = r.json()['user_z_battles']
        if zbattles == []:
          zbattles = 0
      else:
        zbattles = 0

      level = 1
      for zbattle in zbattles:
        if int(zbattle['z_battle_stage_id']) == int(event['id']):
          level = zbattle['max_clear_level'] + 1
          print('Current EZA Level: ' + str(level))

      # Stop at level 30 !! This may not work for all zbattle e.g kid gohan
      while level < 31:
        ##Get supporters
        headers = generate_headers('GET', '/z_battles/' + str(event['id']) + '/supporters')
        url = config.game_env.url + '/z_battles/' + str(event['id']) + '/supporters'
        r = requests.get(url, headers=headers)
        if 'supporters' in r.json():
          supporter = r.json()['supporters'][0]['id']
        elif 'error' in r.json():
          print(Fore.RED + Style.BRIGHT + r.json())
          return 0
        else:
          print(Fore.RED + Style.BRIGHT + 'Problem with ZBattle')
          print(r.raw())
          return 0

        ###Send first request
        headers = generate_headers('POST', '/z_battles/' + str(event['id']) + '/start')

        if kagi == True:
          sign = json.dumps({
            'friend_id': supporter,
            'level': level,
            'selected_team_num': config.deck,
            'eventkagi_item_id': 5
          })
        else:
          sign = json.dumps({
            'friend_id': supporter,
            'level': level,
            'selected_team_num': config.deck,
          })

        enc_sign = crypto.encrypt_sign(sign)
        data = {'sign': enc_sign}
        url = config.game_env.url + '/z_battles/' + str(event['id']) + '/start'
        r = requests.post(url, data=json.dumps(data), headers=headers)

        if 'sign' in r.json():
          dec_sign = crypto.decrypt_sign(r.json()['sign'])
        # Check if error was due to lack of stamina
        elif 'error' in r.json():
          if r.json()['error']['code'] == 'act_is_not_enough':
            # Check if allowed to refill stamina
            if config.allow_stamina_refill == True:
              refill_stamina_command()
              r = requests.post(url, data=json.dumps(data),
                                headers=headers)
          else:
            print(r.json())
            return 0
        else:
          print(Fore.RED + Style.BRIGHT + 'Problem with ZBattle')
          print(r.raw())
          return 0

        finish_time = int(round(time.time(), 0) + 2000)
        start_time = finish_time - randint(6200000, 8200000)

        data = {
          'elapsed_time': finish_time - start_time,
          'is_cleared': True,
          'level': level,
          's': 'rGAX18h84InCwFGbd/4zr1FvDNKfmo/TJ02pd6onclk=',
          't': 'eyJzdW1tYXJ5Ijp7ImVuZW15X2F0dGFjayI6MTAwMzg2LCJlbmVteV9hdHRhY2tfY291bnQiOjUsImVuZW15X2hlYWxfY291bnRzIjpbMF0sImVuZW15X2hlYWxzIjpbMF0sImVuZW15X21heF9hdHRhY2siOjEwMDAwMCwiZW5lbXlfbWluX2F0dGFjayI6NTAwMDAsInBsYXllcl9hdHRhY2tfY291bnRzIjpbMTBdLCJwbGF5ZXJfYXR0YWNrcyI6WzMwNjYwNTJdLCJwbGF5ZXJfaGVhbCI6MCwicGxheWVyX2hlYWxfY291bnQiOjAsInBsYXllcl9tYXhfYXR0YWNrcyI6WzEyMzY4NTBdLCJwbGF5ZXJfbWluX2F0dGFja3MiOls0NzcxOThdLCJ0eXBlIjoic3VtbWFyeSJ9fQ==',
          'token': dec_sign['token'],
          'used_items': [],
          'z_battle_finished_at_ms': finish_time,
          'z_battle_started_at_ms': start_time,
        }
        # enc_sign = encrypt_sign(sign)

        headers = generate_headers('POST', '/z_battles/' + str(event['id']) + '/finish')
        url = config.game_env.url + '/z_battles/' + str(event['id']) + '/finish'

        r = requests.post(url, data=json.dumps(data), headers=headers)
        dec_sign = crypto.decrypt_sign(r.json()['sign'])
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
        if 'gasha_point' in dec_sign:
          print('Friend Points: ' + str(dec_sign['gasha_point']))

        print('--------------------------')
        print('##############################################')
        level += 1
      refresh_client_command()

  except Exception as e:
    print(Fore.RED + Style.BRIGHT + str(e))
    print(Fore.RED + Style.BRIGHT + 'Trouble finding new Z-Battle events')
