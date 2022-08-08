import PySimpleGUI as sg

import config
import network
from commands.game.sell_cards import sell_cards_command


def sell_cards__bulk_GUI_command():
    # Provides a GUI to select a range of cards to sell.
    r = network.get_teams()
    team_cards = []
    for team in r['user_card_teams']:
        team_cards.extend(team['user_card_ids'])

    r = network.get_support_leaders()
    team_cards.extend(r['support_leader_ids'])

    r = network.get_cards()

    cards_master_dict = []
    for card in r['cards']:
        # Avoid selling favourited cards
        if card['is_favorite'] == True:
            continue

        # Quick and dirty way to exclude elder kais from sell
        hp_max = config.Cards.find_or_fail(card['card_id']).hp_max
        if hp_max == 1:
            continue

        card_name = config.Cards.find_or_fail(card['card_id']).name
        rarity = config.Cards.find_or_fail(card['card_id']).rarity
        if card['id'] not in team_cards:
            cards_master_dict.append({
                'card_id': card['card_id'],
                'unique_id': card['id'],
                'name': card_name,
                'rarity': rarity
            })

            card_name = config.Cards.find_or_fail(card['card_id']).name
            rarity = config.Cards.find_or_fail(card['card_id']).rarity
            if card['id'] not in team_cards:
                cards_master_dict.append({
                    'card_id': card['card_id'],
                    'unique_id': card['id'],
                    'name': card_name,
                    'rarity': rarity
                })

    cards_to_display_dicts = []
    cards_to_display_dicts = cards_master_dict[:]

    cards_to_display = []
    for card in cards_to_display_dicts:
        cards_to_display.append(card['name'])

    col1 = [[sg.Checkbox('N', default=False, key='N', change_submits=True)],
            [sg.Checkbox('R', default=False, key='R', change_submits=True)],
            [sg.Checkbox('SR', default=False, key='SR', change_submits=True)],
            [sg.Checkbox('SSR', default=False, key='SSR', change_submits=True)]]
    col2 = [[sg.Listbox(values=([]), size=(30, 20), key='CARDS')]]
    layout = [[sg.Column(col1), sg.Column(col2)], [sg.Button(button_text='Sell!', key='SELL')]]
    window = sg.Window('Sell Cards').Layout(layout)
    while True:
        event, values = window.Read()

        if event == None:
            window.Close()
            return 0

        if event in ['N', 'R', 'SR', 'SSR', 'SELL']:
            accepted_rarities = []
            if values['N']:
                accepted_rarities.append(0)
            if values['R']:
                accepted_rarities.append(1)
            if values['SR']:
                accepted_rarities.append(2)
            if values['SSR']:
                accepted_rarities.append(3)

            cards_to_display[:] = []
            cards_to_display_dicts[:] = []
            for card in cards_master_dict:
                if card['rarity'] in accepted_rarities:
                    cards_to_display.append(card['name'])
                    cards_to_display_dicts.append(card)

        if event == 'SELL':
            cards_to_sell = []
            window.Hide()
            window.Refresh()
            for card in cards_to_display_dicts:
                cards_to_sell.append(card['unique_id'])
                cards_master_dict.remove(card)
            sell_cards_command(cards_to_sell)
            cards_to_display[:] = []
            cards_to_display_dicts[:] = []
            cards_to_display_dicts[:] = cards_master_dict
            for card in cards_to_display_dicts:
                if card['rarity'] in accepted_rarities:
                    cards_to_display.append(card['name'])
            window.UnHide()
            window.Refresh()

        window.FindElement('CARDS').Update(values=cards_to_display)

    return 0
