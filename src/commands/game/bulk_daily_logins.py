import os

import PySimpleGUI as sg
from colorama import Fore, Style

from commands.game.bulk_daily_save_processor import bulk_daily_save_processor_command


def bulk_daily_logins_command():
    layout = [[sg.Text('Choose what gets completed!')],
              [sg.Checkbox('Daily Login', default=True)],
              [sg.Checkbox('Accept Gifts')],
              [sg.Checkbox('Complete Daily Events')],
              [sg.Text('Enter command to execute:')],
              [sg.Input(key='user_input')],
              [sg.Ok()]]

    window = sg.Window('Daily Logins', keep_on_top=True).Layout(layout)
    event, values = window.Read()
    window.Close()
    if event == None:
        return 0

    login = values[0]
    gift = values[1]
    daily_events = values[2]
    user_input = values['user_input']
    print(user_input)

    # Fetch saves to choose from
    files = []
    for subdir, dirs, os_files in os.walk("Saves"):
        for file in sorted(os_files):
            files.append(subdir + os.sep + file)

    ### Create window that manages saves selections
    # Layout
    chosen_files = []
    column1 = [
        [sg.Listbox(values=(files), size=(30, None), bind_return_key=True, select_mode='multiple', key='select_save')],
        [sg.Button(button_text='Select All', key='all')]]
    column2 = [[sg.Listbox(values=(chosen_files), size=(30, None), bind_return_key=True, select_mode='multiple',
                           key='remove_save')],
               [sg.Button(button_text='Remove All', key='remove_all')]]
    layout = [[sg.Column(column1), sg.Column(column2)],
              [sg.Button(button_text='Start Grind!', key='Done')]]
    window = sg.Window('Saves', keep_on_top=True, font=('Helvetica', 15)).Layout(layout)

    while event != 'Done':
        event, value = window.Read()
        if event == 'select_save':
            chosen_files.extend(value['select_save'])
            for save in value['select_save']:
                files.remove(save)

        if event == 'remove_save':
            files.extend(value['remove_save'])
            for save in value['remove_save']:
                chosen_files.remove(save)

        if event == 'all':
            chosen_files.extend(files)
            files[:] = []

        if event == 'remove_all':
            files.extend(chosen_files)
            chosen_files[:] = []

        if event == None:
            print(Fore.RED + Style.BRIGHT + 'User terminated daily logins')
            return 0

        window.FindElement('select_save').Update(values=sorted(files))
        window.FindElement('remove_save').Update(values=sorted(chosen_files))

    window.Close()

    ### Execution per file
    for file in chosen_files:
        bulk_daily_save_processor_command(file, login, gift, daily_events, user_input)
