import os

from colorama import Fore, Style

import config
from commands.refresh_client import refresh_client_command


def load_account_command():
    while 1 == 1:
        print(
            'Choose your operating system (' + Fore.YELLOW + Style.BRIGHT + 'Android: 1' + Style.RESET_ALL + ' or' + Fore.YELLOW + Style.BRIGHT + ' IOS: 2' + Style.RESET_ALL + ')',
            end='')
        platform = input('')
        if platform[0].lower() in ['1', '2']:
            if platform[0].lower() == '1':
                config.platform = 'android'
            else:
                config.platform = 'ios'
                config.user_agent = 'CFNetwork/808.3 Darwin/16.3.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X)'
            break
        else:
            print(Fore.RED + 'Could not identify correct operating system to use.')

    while 1 == 1:
        save_name = input("What save would you like to load?: ")
        if os.path.isfile('Saves' + os.sep + config.platform + os.sep + save_name):
            try:
                f = open(os.path.join('Saves', config.platform, save_name), 'r')
                config.identifier = f.readline().rstrip()
                config.AdId = f.readline().rstrip()
                config.UniqueId = f.readline().rstrip()
                config.platform = f.readline().rstrip()
                client = f.readline().rstrip()
                if config.client == client:
                    config.last_save_name = save_name
                    if client == 'japan':
                        config.gb_version_code = '4.8.3-3998abb91156a951db70394807eb63d626d20c640c0c2f4611b0973499ce87ef'
                    break
                else:
                    print(Fore.RED + Style.BRIGHT + 'Save does not match client version.')

            except Exception as e:
                print(e)

        else:
            print(Fore.RED + Style.BRIGHT + "Could not find " + save_name)
    refresh_client_command()
