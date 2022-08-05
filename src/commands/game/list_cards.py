import PySimpleGUI as sg
import requests

import config
from network.utils import generate_headers


def list_cards_command():
  headers = generate_headers('GET', '/cards')
  url = config.game_env.url + '/cards'
  r = requests.get(url, headers=headers)
  cards = {}
  for card in r.json()['cards']:
    config.Model.set_connection_resolver(config.game_env.db_manager)
    name = config.Cards.find_or_fail(card['card_id']).name
    element = str(config.Cards.find_or_fail(card['card_id']).element)

    if element[-1] == '0':
      element = 'AGL'
    elif element[-1] == '1':
      element = 'TEQ'
    elif element[-1] == '2':
      element = 'INT'
    elif element[-1] == '3':
      element = 'STR'
    elif element[-1] == '4':
      element = 'PHY'

    config.Model.set_connection_resolver(config.game_env.db_manager)
    cost = config.Cards.find_or_fail(card['card_id']).cost
    leader_skill_id = config.Cards.find_or_fail(card['card_id']).leader_skill_id
    passive_skill_id = config.Cards.find_or_fail(card['card_id']).passive_skill_set_id
    links_skill_ids = []
    links_skill_ids.append(config.Cards.find_or_fail(card['card_id']).link_skill1_id)
    links_skill_ids.append(config.Cards.find_or_fail(card['card_id']).link_skill2_id)
    links_skill_ids.append(config.Cards.find_or_fail(card['card_id']).link_skill3_id)
    links_skill_ids.append(config.Cards.find_or_fail(card['card_id']).link_skill4_id)
    links_skill_ids.append(config.Cards.find_or_fail(card['card_id']).link_skill5_id)
    links_skill_ids.append(config.Cards.find_or_fail(card['card_id']).link_skill6_id)
    links_skill_ids.append(config.Cards.find_or_fail(card['card_id']).link_skill7_id)

    cards[card['card_id']] = {
      'id': card['card_id'],
      'unique_id': card['id'],
      'name': name,
      'type': element,
      'cost': cost,
      'leader_skill_id': leader_skill_id,
      'link_skill_ids': links_skill_ids,
      'passive_skill_id': passive_skill_id
    }
  cards_sort = []
  for item in cards:
    cards_sort.append(cards[item])

  # Sort cards for listbox
  cards_sort = sorted(cards_sort, key=lambda k: k['name'])
  cards_sort = sorted(cards_sort, key=lambda k: k['cost'])

  # Card strings to for listbox value
  cards_to_display = []
  for card in cards_sort:
    cards_to_display.append(card['type'] + ' ' + str(card['cost']) + ' ' + card['name'] + ' | ' + str(card['id']))

  col1 = [[sg.Listbox(values=(cards_to_display), size=(30, 30), key='CARDS', change_submits=True,
                      font=('Courier', 15, 'bold'))]]
  col2 = [[sg.Text('Type', key='TYPE', font=('', 15, 'bold'), auto_size_text=True),
           sg.Text('Name', key='NAME', size=(None, 3), font=('', 15, 'bold'), auto_size_text=True)],
          [sg.Text('Cost', key='COST', font=('', 10, 'bold'))],
          [sg.Text('Leader Skill', key='LEADERSKILLNAME', size=(None, 1), font=('', 12, 'bold underline'))],
          [sg.Text('Leader Skill Description', key='LEADERSKILLDESC', size=(None, 4), font=('', 10, 'bold'))],
          [sg.Text('Passive', key='PASSIVESKILLNAME', size=(None, 2), font=('', 12, 'bold underline'))],
          [sg.Text('Passive Description', key='PASSIVESKILLDESC', size=(None, 5), font=('', 10, 'bold'))],
          [sg.Text('Link Skill', key='LINKSKILL1', size=(None, 1), font=('', 10, 'bold'))],
          [sg.Text('Link Skill', key='LINKSKILL2', size=(None, 1), font=('', 10, 'bold'))],
          [sg.Text('Link Skill', key='LINKSKILL3', size=(None, 1), font=('', 10, 'bold'))],
          [sg.Text('Link Skill', key='LINKSKILL4', size=(None, 1), font=('', 10, 'bold'))],
          [sg.Text('Link Skill', key='LINKSKILL5', size=(None, 1), font=('', 10, 'bold'))],
          [sg.Text('Link Skill', key='LINKSKILL6', size=(None, 1), font=('', 10, 'bold'))],
          [sg.Text('Link Skill', key='LINKSKILL7', size=(None, 1), font=('', 10, 'bold'))]]

  layout = [[sg.Column(col1), sg.Column(col2)]]
  window = sg.Window('Items').Layout(layout)
  while True:
    event, values = window.Read()

    if event == None:
      window.Close()
      return 0

    if event == 'CARDS':
      # Get Card ID
      card_id = int(values['CARDS'][0].split(' | ')[1])

      # Get correct colour for card element
      if cards[card_id]['type'] == 'PHY':
        colour = 'gold2'
      elif cards[card_id]['type'] == 'STR':
        colour = 'red'
      elif cards[card_id]['type'] == 'AGL':
        colour = 'blue'
      elif cards[card_id]['type'] == 'TEQ':
        colour = 'green'
      elif cards[card_id]['type'] == 'INT':
        colour = 'purple'
      else:
        colour = 'black'

      # Retrieve leaderskill from DB
      config.Model.set_connection_resolver(config.game_env.db_manager)
      leader_skill_name = config.LeaderSkills.find_or_fail(cards[card_id]['leader_skill_id']).name.replace(
        '\n', ' ')
      leader_skill_desc = config.LeaderSkills.find_or_fail(
        cards[card_id]['leader_skill_id']).description.replace('\n', ' ')

      # Retrieve passive skill
      if cards[card_id]['passive_skill_id'] == None:
        passive_skill_name = 'None'
        passive_skill_desc = 'None'
      else:
        config.Model.set_connection_resolver(config.game_env.db_manager)
        passive_skill_name = config.Passives.find_or_fail(cards[card_id]['passive_skill_id']).name.replace(
          '\n', ' ')
        passive_skill_desc = config.Passives.find_or_fail(
          cards[card_id]['passive_skill_id']).description.replace('\n', ' ')

      # Retrieve link skills from DB
      ls1 = None
      ls2 = None
      ls3 = None
      ls4 = None
      ls5 = None
      ls6 = None
      ls7 = None

      config.Model.set_connection_resolver(config.game_env.db_manager)
      if config.LinkSkills.find(cards[card_id]['link_skill_ids'][0]) != None:
        ls1 = config.LinkSkills.find(cards[card_id]['link_skill_ids'][0]).name.replace('\n', ' ')
      if config.LinkSkills.find(cards[card_id]['link_skill_ids'][1]) != None:
        ls2 = config.LinkSkills.find(cards[card_id]['link_skill_ids'][1]).name.replace('\n', ' ')
      if config.LinkSkills.find(cards[card_id]['link_skill_ids'][2]) != None:
        ls3 = config.LinkSkills.find(cards[card_id]['link_skill_ids'][2]).name.replace('\n', ' ')
      if config.LinkSkills.find(cards[card_id]['link_skill_ids'][3]) != None:
        ls4 = config.LinkSkills.find(cards[card_id]['link_skill_ids'][3]).name.replace('\n', ' ')
      if config.LinkSkills.find(cards[card_id]['link_skill_ids'][4]) != None:
        ls5 = config.LinkSkills.find(cards[card_id]['link_skill_ids'][4]).name.replace('\n', ' ')
      else:
        ls5 = 'Link Skill'
      if config.LinkSkills.find(cards[card_id]['link_skill_ids'][5]) != None:
        ls6 = config.LinkSkills.find(cards[card_id]['link_skill_ids'][5]).name.replace('\n', ' ')
      else:
        ls6 = 'Link Skill'
      if config.LinkSkills.find(cards[card_id]['link_skill_ids'][6]) != None:
        ls7 = config.LinkSkills.find(cards[card_id]['link_skill_ids'][6]).name.replace('\n', ' ')
      else:
        ls7 = 'Link Skill'

      window.FindElement('NAME').Update(value=cards[card_id]['name'].replace('\n', ' '))
      window.FindElement('TYPE').Update(value='[' + cards[card_id]['type'] + ']', text_color=colour)
      window.FindElement('COST').Update(value='COST: ' + str(cards[card_id]['cost']))
      window.FindElement('LEADERSKILLNAME').Update(value=leader_skill_name)
      window.FindElement('LEADERSKILLDESC').Update(value=leader_skill_desc)
      window.FindElement('PASSIVESKILLNAME').Update(value=passive_skill_name)
      window.FindElement('PASSIVESKILLDESC').Update(value=passive_skill_desc)
      window.FindElement('LINKSKILL1').Update(value=ls1)
      window.FindElement('LINKSKILL2').Update(value=ls2)
      window.FindElement('LINKSKILL3').Update(value=ls3)
      window.FindElement('LINKSKILL4').Update(value=ls4)
      window.FindElement('LINKSKILL5').Update(value=ls5)
      window.FindElement('LINKSKILL6').Update(value=ls6)
      window.FindElement('LINKSKILL7').Update(value=ls7)
