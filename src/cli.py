from colorama import Fore

from commands import help, exit
from commands.auth import create, load
from commands.game import info, rename, stage, act, tutorial, gifts, missions, card_capacity

COMMANDS = [
    exit,
    help,
    create,
    load,
    info,
    rename,
    stage,
    act,
    tutorial,
    gifts,
    missions,
    card_capacity
]


def run():
    print(Fore.GREEN + 'Welcome to Dokkan 777')

    while True:
        user_input = input(Fore.YELLOW + '777 $ ' + Fore.RESET).strip()
        [command_name, *command_args] = user_input.split(' ')

        for command in COMMANDS:
            if command_name == command.NAME:
                try:
                    command.run(*command_args)
                    break
                except TypeError:
                    print('invalid command arguments')
