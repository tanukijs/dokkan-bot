import os

from colorama import Fore, Style

import config
from commands.create_file import create_file_command


def save_account_command(reroll_state):
    if not os.path.isdir("Saves"):
        try:
            os.mkdir('Saves')
            os.mkdir('Saves/android')
            os.mkdir('Saves/ios')
        except:
            print(Fore.RED + Style.BRIGHT + 'Unable to create saves file')
            return 0

    if reroll_state:
        create_file_command('Saves' + os.sep + config.platform + os.sep + config.last_save_name, config.last_save_name)
        return

    valid_save = False
    while not valid_save:
        save_name = input("What would you like to name the file?")
        while save_name.isalnum() == 0:
            print(Fore.RED + Style.BRIGHT + "Name not allowed!")
            save_name = input('What would you like to name this save?: ')
        if os.path.exists('Saves' + os.sep + config.platform + os.sep + save_name):
            overwrite_file = input("File by that name already exists. Overwrite? Y/N ")
            if overwrite_file == 'Y' or overwrite_file == 'y':
                create_file_command('Saves' + os.sep + config.platform + os.sep + save_name, save_name)
                config.last_save_name = save_name
                break
            else:
                print('Please choose another name!')
        else:
            create_file_command('Saves' + os.sep + config.platform + os.sep + save_name, save_name)
            config.last_save_name = save_name
            break
