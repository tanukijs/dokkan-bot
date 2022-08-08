from colorama import Fore

import cli

NAME = 'help'
DESCRIPTION = 'List of available commands'


def run():
    for command in cli.COMMANDS:
        row = Fore.GREEN + command.NAME + Fore.RESET + '\t' + command.DESCRIPTION
        print(row.expandtabs(30))
