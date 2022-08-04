import os

import PySimpleGUI as sg
import requests

import config
from network.utils import generate_headers


def items_viewer_command():
    # ## Accepts Outstanding Login Bonuses
    headers = generate_headers('GET', '/resources/login?potential_items=true&training_items=true&support_items=true&treasure_items=true&special_items=true')
    url = config.gb_url + '/resources/login?potential_items=true&training_items=true&support_items=true&treasure_items=true&special_items=true'
    r = requests.get(url, headers=headers)

    col1 = [[sg.Checkbox('Support Items', default=False, key='SUPPORT', change_submits=True)],
            [sg.Checkbox('Training Items', default=False, key='TRAINING', change_submits=True)],
            [sg.Checkbox('Potential Items', default=False, key='POTENTIAL', change_submits=True)],
            [sg.Checkbox('Treasure Items', default=False, key='TREASURE', change_submits=True)],
            [sg.Checkbox('Special Items', default=False, key='SPECIAL', change_submits=True)]]
    col2 = [[sg.Output(size=(40, 30))]]
    layout = [[sg.Column(col1), sg.Column(col2)]]
    window = sg.Window('Items').Layout(layout)
    while True:
        event, values = window.Read()

        if event == None:
            window.Close()
            return 0

        if event in ['SUPPORT', 'TRAINING', 'POTENTIAL', 'TREASURE', 'SPECIAL']:
            os.system('cls' if os.name == 'nt' else 'clear')
            if values['SUPPORT']:
                print('\n##########################')
                print('Support Items -')
                print('##########################')
                window.Refresh()
                for item in r.json()['support_items']['items']:
                    try:
                        config.Model.set_connection_resolver(config.db_glb)
                        print(
                            str(config.SupportItems.find_or_fail(item['item_id']).name) + ' x' + str(item['quantity']))
                    except:
                        config.Model.set_connection_resolver(config.db_jp)
                        print(
                            str(config.SupportItems.find_or_fail(item['item_id']).name) + ' x' + str(item['quantity']))
                window.Refresh()
            if values['TRAINING']:
                print('\n##########################')
                print('Training Items -')
                print('##########################')
                window.Refresh()
                for item in r.json()['training_items']:
                    try:
                        config.Model.set_connection_resolver(config.db_glb)
                        print(str(config.TrainingItems.find(item['training_item_id']).name) + ' x' + str(
                            item['quantity']))
                    except:
                        config.Model.set_connection_resolver(config.db_jp)
                        print(str(config.TrainingItems.find(item['training_item_id']).name) + ' x' + str(
                            item['quantity']))
                window.Refresh()
            if values['POTENTIAL']:
                print('\n##########################')
                print('Potential Items -')
                print('##########################')
                window.Refresh()
                for item in reversed(r.json()['potential_items']['user_potential_items']):
                    try:
                        config.Model.set_connection_resolver(config.db_glb)
                        print(str(config.PotentialItems.find(item['potential_item_id']).name) + ' x' + str(
                            item['quantity']))
                        print(config.PotentialItems.find(item['potential_item_id']).description)
                    except:
                        config.Model.set_connection_resolver(config.db_jp)
                        print(str(config.PotentialItems.find(item['potential_item_id']).name) + ' x' + str(
                            item['quantity']))
                        print(config.PotentialItems.find(item['potential_item_id']).description)
                window.Refresh()
            if values['TREASURE']:
                print('\n##########################')
                print('Treasure Items -')
                print('##########################')
                window.Refresh()
                for item in r.json()['treasure_items']['user_treasure_items']:
                    try:
                        config.Model.set_connection_resolver(config.db_glb)
                        print(str(config.TreasureItems.find(item['treasure_item_id']).name) + ' x' + str(
                            item['quantity']))
                    except:
                        config.Model.set_connection_resolver(config.db_jp)
                        print(str(config.TreasureItems.find(item['treasure_item_id']).name) + ' x' + str(
                            item['quantity']))
                window.Refresh()
            if values['SPECIAL']:
                print('\n##########################')
                print('Special Items -')
                print('##########################')
                window.Refresh()
                for item in r.json()['special_items']:
                    try:
                        config.Model.set_connection_resolver(config.db_glb)
                        print(
                            str(config.SpecialItems.find(item['special_item_id']).name) + ' x' + str(item['quantity']))
                    except:
                        config.Model.set_connection_resolver(config.db_jp)
                        print(
                            str(config.SpecialItems.find(item['special_item_id']).name) + ' x' + str(item['quantity']))
                window.Refresh()
