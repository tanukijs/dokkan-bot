import PySimpleGUI as sg
import requests
from colorama import Back, Fore, Style

import config
from commands.game.get_remaining_stones import get_remaining_stones_command
from network.utils import generate_headers


def summon_command():
  headers = generate_headers('GET', '/gashas')
  url = config.game_env.url + '/gashas'
  r = requests.get(url, headers=headers)
  gashas = []
  for gasha in r.json()['gashas']:
    gashas.append(gasha['name'] + ' | ' + str(gasha['id']))

  layout = [[sg.Listbox(values=(gashas), size=(50, 20), key='GASHAS')],
            [sg.Radio('Multi', "TYPE", default=True), sg.Radio('Single', "TYPE")],
            [sg.Spin([i for i in range(1, 999)], key='LOOP', initial_value=1, size=(3, 3))],
            [sg.Button(button_text='Summon!', key='SUMMON')]]
  window = sg.Window('Event Viewer').Layout(layout)

  while True:
    event, values = window.Read()
    if event == None:
      return 0

    if event == 'SUMMON' and len(values['GASHAS']) > 0:
      summon_id = values['GASHAS'][0].split(' | ')[1]
      if values[0]:
        headers = generate_headers('POST', '/gashas/' + str(summon_id) + '/courses/2/draw')
        url = config.game_env.url + '/gashas/' + str(summon_id) + '/courses/2/draw'
        window.Hide()
        window.Refresh()
        for i in range(int(values['LOOP'])):
          r = requests.post(url, headers=headers).json()
          if 'error' in r:
            print(r)
            window.Close()
            return 0
          card_list = []
          for card in r['gasha_items']:
            config.Model.set_connection_resolver(config.game_env.db_manager)
            config.Cards.find_or_fail(int(card['item_id'])).rarity

            if config.Cards.find(int(card['item_id'])).rarity == 0:
              rarity = Fore.RED + Style.BRIGHT + 'N' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 1:
              rarity = Fore.RED + Style.BRIGHT + 'R' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 2:
              rarity = Fore.RED + Style.BRIGHT + 'SR' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 3:
              rarity = Fore.BLUE + Back.WHITE + Style.BRIGHT + 'SSR' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 4:
              rarity = Fore.MAGENTA + Style.BRIGHT + 'UR' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 5:
              rarity = Fore.CYAN + 'LR' + Style.RESET_ALL
            if str(config.Cards.find(int(card['item_id'])).element)[-1] == '0':
              type = Fore.CYAN + Style.BRIGHT + 'AGL '
            elif str(config.Cards.find(int(card['item_id'])).element)[-1] == '1':
              type = Fore.GREEN + Style.BRIGHT + 'TEQ '
            elif str(config.Cards.find(int(card['item_id'])).element)[-1] == '2':
              type = Fore.MAGENTA + Style.BRIGHT + 'INT '
            elif str(config.Cards.find(int(card['item_id'])).element)[-1] == '3':
              type = Fore.RED + Style.BRIGHT + 'STR '
            elif str(config.Cards.find(int(card['item_id'])).element)[-1] == '4':
              type = Fore.YELLOW + 'PHY '
            card_list.append(type + config.Cards.find(int(card['item_id'
                                                          ])).name + ' ' + rarity)
          for card in card_list:
            print(card)
        window.UnHide()
        window.Refresh()


      else:
        headers = generate_headers('POST', '/gashas/' + str(summon_id) + '/courses/1/draw')
        url = config.game_env.url + '/gashas/' + str(summon_id) + '/courses/1/draw'
        window.Hide()
        window.Refresh()
        for i in range(int(values['LOOP'])):
          r = requests.post(url, headers=headers).json()
          if 'error' in r:
            print(r)
            window.Close()
            return 0
          card_list = []
          for card in r['gasha_items']:
            config.Model.set_connection_resolver(config.game_env.db_manager)
            config.Cards.find_or_fail(int(card['item_id'])).rarity

            if config.Cards.find(int(card['item_id'])).rarity == 0:
              rarity = Fore.RED + Style.BRIGHT + 'N' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 1:
              rarity = Fore.RED + Style.BRIGHT + 'R' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 2:
              rarity = Fore.RED + Style.BRIGHT + 'SR' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 3:
              rarity = Fore.YELLOW + 'SSR' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 4:
              rarity = Fore.MAGENTA + Style.BRIGHT + 'UR' + Style.RESET_ALL
            elif config.Cards.find(int(card['item_id'])).rarity == 5:
              rarity = Fore.CYAN + 'LR' + Style.RESET_ALL
            if str(config.Cards.find(int(card['item_id'])).element)[-1] == '0':
              type = Fore.CYAN + Style.BRIGHT + 'AGL '
            elif str(config.Cards.find(int(card['item_id'])).element)[-1] == '1':
              type = Fore.GREEN + Style.BRIGHT + 'TEQ '
            elif str(config.Cards.find(int(card['item_id'])).element)[-1] == '2':
              type = Fore.MAGENTA + Style.BRIGHT + 'INT '
            elif str(config.Cards.find(int(card['item_id'])).element)[-1] == '3':
              type = Fore.RED + Style.BRIGHT + 'STR '
            elif str(config.Cards.find(int(card['item_id'])).element)[-1] == '4':
              type = Fore.YELLOW + 'PHY '
            card_list.append(type + config.Cards.find(int(card['item_id'
                                                          ])).name + ' ' + rarity)
          for card in card_list:
            print(card)
        window.UnHide()
        window.Refresh()

      print('------------------- Stones remaining: ' + get_remaining_stones_command())
