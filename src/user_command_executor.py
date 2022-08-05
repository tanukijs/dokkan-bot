import io
import os
import sys

from colorama import Fore, Style

import config
from commands.game.accept_gifts import accept_gifts_command
from commands.game.accept_missions import accept_missions_command
from commands.game.change_name import change_name_command
from commands.game.change_supporter import change_supporter_command
from commands.game.change_team import change_team_command
from commands.game.complete_area import complete_area_command
from commands.game.complete_clash import complete_clash_command
from commands.game.complete_potential import complete_potential_command
from commands.game.complete_stage import complete_stage_command
from commands.game.complete_unfinished_events import complete_unfinished_events_command
from commands.game.complete_unfinished_quest_stages import complete_unfinished_quest_stages_command
from commands.game.complete_unfinished_zbattles import complete_unfinished_zbattles_command
from commands.game.complete_zbattle_stage import complete_zbattle_stage_command
from commands.game.dragonballs import dragonballs_command
from commands.game.event_viewer import event_viewer_command
from commands.game.get_transfer_code import get_transfer_code_command
from commands.game.get_user_info import get_user_info_command
from commands.game.increase_capacity import increase_capacity_command
from commands.game.items_viewer import items_viewer_command
from commands.game.list_cards import list_cards_command
from commands.game.list_events import list_events_command
from commands.game.list_summons import list_summons_command
from commands.game.refresh_client import refresh_client_command
from commands.game.sell_cards__bulk_GUI import sell_cards__bulk_GUI_command
from commands.game.sell_medals import sell_medals_command
from commands.game.summon import summon_command


def user_command_executor_command(command):
  if ',' in command:
    command = command.replace(" ", "")
    command = command.replace(",", "\n")
    s = io.StringIO(command + '\n')
    sys.stdin = s
    command = input()

  if command == 'help':
    if os.path.exists('help.txt'):
      f = open(os.path.join('help.txt'), 'r')
      help_text = f.read()
      print(help_text)
    else:
      print(Fore.RED + Style.BRIGHT + 'help.txt does not exist.')
  elif command == 'stage':
    stage = input('What stage would you like to complete?: ')
    difficulty = input('Enter the difficulty|(0:Easy, 1:Hard etc...): ')
    loop = input('Enter how many times to execute: ')
    for i in range(int(loop)):
      complete_stage_command(stage, difficulty)
  elif command == 'area':
    area = input('Enter the area to complete: ')
    loop = input('How many times to complete the entire area: ')
    for i in range(int(loop)):
      complete_area_command(area)
  elif command == 'gift':
    accept_gifts_command()
    accept_missions_command()
  elif command == 'omegafarm':
    accept_gifts_command()
    accept_missions_command()
    complete_unfinished_quest_stages_command()
    complete_unfinished_events_command()
    complete_unfinished_zbattles_command()
    complete_clash_command()
  ## When this will get updated, we shall add :finishzbattle,30, + sell + sellhercule + baba(?)
  elif command == 'quests':
    complete_unfinished_quest_stages_command()
  elif command == 'events':
    complete_unfinished_events_command()
  elif command == 'zbattles':
    complete_unfinished_zbattles_command()
  elif command == 'zstages':
    complete_zbattle_stage_command()
  elif command == 'clash':
    complete_clash_command()
  elif command == 'daily':
    complete_stage_command('130001', 0)
    complete_stage_command('131001', 0)
    complete_stage_command('132001', 0)
    complete_potential_command()
    accept_gifts_command()
    accept_missions_command()
  elif command == 'listevents':
    list_events_command()
  elif command == 'chooseevents':
    event_viewer_command()
  elif command == 'summon':
    summon_command()
  elif command == 'listsummons':
    list_summons_command()
  elif command == 'dragonballs':
    dragonballs_command()
  elif command == 'info':
    get_user_info_command()
  elif command == 'items':
    items_viewer_command()
  elif command == 'medals':
    sell_medals_command()
  elif command == 'sell':
    sell_cards__bulk_GUI_command()
  elif command == 'cards':
    list_cards_command()
  elif command == 'supporter':
    change_supporter_command()
  elif command == 'team':
    change_team_command()
  elif command == 'deck':
    config.deck = int(input('Enter a deck number to use: '))
  elif command == 'transfer':
    get_transfer_code_command()
  elif command == 'capacity':
    increase_capacity_command()
  elif command == 'name':
    change_name_command()
  elif command == 'refresh':
    refresh_client_command()
  else:
    print('Command not found.')
