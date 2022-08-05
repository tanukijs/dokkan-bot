import json

import PySimpleGUI as sg
import requests
from colorama import Fore, Style

import config
from network.utils import generate_headers


def change_supporter_command():
  # Needs to have translation properly implemented!

  ###Get user cards
  print(Fore.CYAN + Style.BRIGHT + 'Fetching user cards...')
  headers = generate_headers('GET', '/cards')
  url = config.game_env.url + '/cards'
  r = requests.get(url, headers=headers)
  master_cards = r.json()['cards']
  print(Fore.GREEN + Style.BRIGHT + 'Done...')

  ###Sort user cards into a list of dictionaries with attributes
  print(Fore.CYAN + Style.BRIGHT + 'Fetching card attributes...')
  card_list = []
  for card in master_cards:
    ###Get card collection object from database
    config.Model.set_connection_resolver(config.game_env.db_manager)
    db_card = config.Cards.find_or_fail(card['card_id'])
    # db_card = config.Cards.where('id','=',card['card_id']).first()

    ###Get card rarity
    if db_card.rarity == 0:
      rarity = 'N'
    elif db_card.rarity == 1:
      rarity = 'R'
    elif db_card.rarity == 2:
      rarity = 'SR'
    elif db_card.rarity == 3:
      rarity = 'SSR'
    elif db_card.rarity == 4:
      rarity = 'UR'
    elif db_card.rarity == 5:
      rarity = 'LR'
    ###Get card Type
    if str(db_card.element)[-1] == '0':
      type = '[AGL] '
    elif str(db_card.element)[-1] == '1':
      type = '[TEQ] '
    elif str(db_card.element)[-1] == '2':
      type = '[INT] '
    elif str(db_card.element)[-1] == '3':
      type = '[STR] '
    elif str(db_card.element)[-1] == '4':
      type = '[PHY] '
    ###Get card categories list
    categories = []
    # Get category id's given card id
    card_card_categories = config.CardCardCategories.where(
      'card_id', '=', db_card.id).get()

    try:
      for category in card_card_categories:
        config.Model.set_connection_resolver(config.game_env.db_manager)
        categories.append(config.CardCategories.find(
          category.card_category_id).name)
    except:
      None
    ###Get card link_skills list
    link_skills = []
    config.Model.set_connection_resolver(config.game_env.db_manager)
    link_skills.append(config.LinkSkills.find(db_card.link_skill1_id).name)
    link_skills.append(config.LinkSkills.find(db_card.link_skill2_id).name)
    link_skills.append(config.LinkSkills.find(db_card.link_skill3_id).name)
    link_skills.append(config.LinkSkills.find(db_card.link_skill4_id).name)
    link_skills.append(config.LinkSkills.find(db_card.link_skill5_id).name)
    link_skills.append(config.LinkSkills.find(db_card.link_skill6_id).name)
    link_skills.append(config.LinkSkills.find(db_card.link_skill7_id).name)

    dict = {
      'ID': db_card.id,
      'Rarity': rarity,
      'Name': db_card.name,
      'Type': type,
      'Cost': db_card.cost,
      'Hercule': db_card.is_selling_only,
      'HP': db_card.hp_init,
      'Categories': categories,
      'Links': link_skills,
      'UniqueID': card['id']
    }
    card_list.append(dict)
  print(Fore.GREEN + Style.BRIGHT + "Done...")

  ###Sort cards
  print(Fore.CYAN + Style.BRIGHT + "Sorting cards...")
  card_list = sorted(card_list, key=lambda k: k['Name'])
  card_list = sorted(card_list, key=lambda k: k['Rarity'])
  card_list = sorted(card_list, key=lambda k: k['Cost'])
  print(Fore.GREEN + Style.BRIGHT + "Done...")
  ###Define cards to display
  cards_to_display_dicts = []
  cards_to_display = []
  # Take cards in card_list that aren't hercule statues or kais?
  for char in card_list:
    if char['Hercule'] != 1 and char['HP'] > 5:
      cards_to_display_dicts.append(char)
      cards_to_display.append(
        char['Type'] + char['Rarity'] + ' ' + char['Name'] + ' | ' + str(char['ID']) + ' | ' + str(
          char['UniqueID']))

  ###Define links to display
  links_master = []
  for link in config.LinkSkills.all():
    links_master.append(link.name)
  links_to_display = sorted(links_master)

  ###Define categories to display
  categories_master = []
  for category in config.CardCategories.all():
    config.Model.set_connection_resolver(config.game_env.db_manager)
    categories_master.append(config.CardCategories.find_or_fail(category.id).name)

  categories_to_display = sorted(categories_master)

  ###Define window layout

  col1 = [[sg.Listbox(values=(cards_to_display), size=(30, 20), key='CARDS')],
          [sg.Listbox(values=([]), size=(30, 6), key='CARDS_CHOSEN')],
          [sg.Button(button_text='Set as Supporter', key='choose_card')]]

  col2 = [[sg.Listbox(values=(sorted(categories_to_display)), size=(25, 20), key='CATEGORIES')],
          [sg.Listbox(values=([]), size=(25, 6), key='CATEGORIES_CHOSEN')],
          [sg.Button(button_text='Choose Categories', key='choose_categories'),
           sg.Button(button_text='Clear Categories', key='clear_categories')]]

  col3 = [[sg.Listbox(values=(sorted(links_to_display)), size=(25, 20), key='LINKS')],
          [sg.Listbox(values=([]), size=(25, 6), key='LINKS_CHOSEN')],
          [sg.Button(button_text='Choose Links', key='choose_links'),
           sg.Button(button_text='Clear Links', key='clear_links')]]

  layout = [[sg.Column(col1), sg.Column(col2), sg.Column(col3)]]
  window = sg.Window('Supporter Update', grab_anywhere=True, keep_on_top=True).Layout(layout)

  ###Begin window loop
  chosen_links = []
  chosen_categories = []

  ###
  chosen_cards_ids = []
  chosen_cards_unique_ids = []
  chosen_cards_names = []
  chosen_cards_to_display = []

  while len(chosen_cards_ids) < 1:
    event, values = window.Read()

    if event == None:
      return 0

    if event == 'choose_card':
      if len(values['CARDS']) < 1:
        continue
      # Get ID of chosen card to send to bandai
      chosen_line = values['CARDS'][0]
      char_name, char_id, char_unique_id = chosen_line.split(' | ')
      chosen_cards_ids.append(int(char_id))
      chosen_cards_unique_ids.append(int(char_unique_id))
      config.Model.set_connection_resolver(config.game_env.db_manager)
      chosen_cards_names.append(config.Cards.find(char_id).name)

      # Chosen cards to display in lower box
      chosen_cards_to_display.append(chosen_line)

    if event == 'choose_categories':
      for category in values['CATEGORIES']:
        chosen_categories.append(category)
        categories_to_display.remove(category)

    if event == 'clear_categories':
      categories_to_display.extend(chosen_categories)
      chosen_categories[:] = []
      categories_to_display = sorted(categories_to_display)

    if event == 'choose_links':
      for link in values['LINKS']:
        chosen_links.append(link)
        links_to_display.remove(link)

    if event == 'clear_links':
      links_to_display.extend(chosen_links)
      chosen_links[:] = []
      links_to_display = sorted(links_to_display)
      break

    ###Re-populate cards to display, checking filter criteria
    cards_to_display[:] = []
    for char in cards_to_display_dicts:
      if char['Name'] in chosen_cards_names:
        continue

      if len(list(set(chosen_links) & set(char['Links']))) != len(chosen_links):
        # print("List intersection")
        continue

      if len(list(set(chosen_categories) & set(char['Categories']))) != len(chosen_categories):
        # print("Category intersectino")
        continue

      cards_to_display.append(
        char['Type'] + char['Rarity'] + ' ' + char['Name'] + ' | ' + str(char['ID']) + ' | ' + str(
          char['UniqueID']))

    ###Update window elements
    window.FindElement('CARDS').Update(values=cards_to_display)
    window.FindElement('CARDS_CHOSEN').Update(values=chosen_cards_to_display)
    window.FindElement('CATEGORIES').Update(values=categories_to_display)
    window.FindElement('CATEGORIES_CHOSEN').Update(values=chosen_categories)
    window.FindElement('LINKS').Update(values=links_to_display)
    window.FindElement('LINKS_CHOSEN').Update(values=chosen_links)

  window.Close()
  ###Send selected supporter to bandai
  headers = generate_headers('PUT', '/support_leaders')
  url = config.game_env.url + '/support_leaders'
  # print(chosen_cards_unique_ids)
  data = {'support_leader_ids': chosen_cards_unique_ids}
  # print(data)
  r = requests.put(url, data=json.dumps(data), headers=headers)
  if 'error' in r.json():
    print(Fore.RED + Style.BRIGHT + str(r.json()))
  else:
    # print(r.json())
    print(chosen_cards_names)
    print(Fore.GREEN + Style.BRIGHT + "Supporter updated!")

  return 0
