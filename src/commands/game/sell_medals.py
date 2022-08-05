import PySimpleGUI as sg
from colorama import Fore, Style

import config
import network


def sell_medals_command():
    # Get Medals
    config.Model.set_connection_resolver(config.game_env.db_manager)
    r = network.get_awakening_items()

    # Create list with ID for listbox
    medal_list = []
    for medal in reversed(r['awakening_items']):
        config.Model.set_connection_resolver(config.game_env.db_manager)
        item = config.Medal.find_or_fail(int(medal['awakening_item_id']))

        medal_list.append(item.name + ' [x' + str(medal['quantity']) + '] | ' + str(item.id))

    layout = [[sg.Text('Select a medal-')],
              [sg.Listbox(values=(medal_list), size=(30, 15), key='medal_tally', font=('', 15, 'bold'))],
              [sg.Text('Amount'), sg.Spin([i for i in range(1, 999)], initial_value=1, size=(5, None))],
              [sg.Button(button_text='Sell', key='Medal')]]

    window = sg.Window('Medal List', keep_on_top=True).Layout(layout)
    while True:
        event, values = window.Read()

        if event == None:
            window.Close()
            return 0

        # Check if medal selected and sell
        if event == 'Medal':
            if len(values['medal_tally']) == 0:
                print(Fore.RED + Style.BRIGHT + "You did not select a medal.")
                continue

            value = values['medal_tally'][0]
            medal = value.split(' | ')
            medalo = medal[1]
            amount = values[0]

            medal_id = int(medalo)
            chunk = int(amount) // 99
            remainder = int(amount) % 99

            window.Hide()
            window.Refresh()
            for i in range(chunk):
                r = network.post_awakening_item_exchange(medal_id, 99)
                if 'error' in r:
                    print(Fore.RED + Style.BRIGHT + str(r))
                else:
                    print(Fore.GREEN + Style.BRIGHT + 'Sold Medals x' + str(99))

            if remainder > 0:
                r = network.post_awakening_item_exchange(medal_id, remainder)
                if 'error' in r:
                    print(Fore.RED + Style.BRIGHT + str(r))
                else:
                    print(Fore.GREEN + Style.BRIGHT + 'Sold Medals x' + str(remainder))

            # New medal list
            r = network.get_awakening_items()

            medal_list[:] = []
            for medal in reversed(r['awakening_items']):
                config.Model.set_connection_resolver(config.game_env.db_manager)
                item = config.Medal.find_or_fail(int(medal['awakening_item_id']))

                medal_list.append(item.name + ' [x' + str(medal['quantity']) + ']' + ' | ' + str(item.id))

            window.FindElement('medal_tally').Update(values=medal_list)
            window.UnHide()
            window.Refresh()
