from inspect import getfullargspec

from colorama import Fore

import config
from services.command import CommandService

NAME = 'help'
DESCRIPTION = 'List of available commands'
CONTEXT = [config.GameContext.AUTH, config.GameContext.GAME]


def run():
    for command_name, command in CommandService.get_all().items():
        if config.game_context not in command.CONTEXT: continue
        specs = getfullargspec(command.run)
        name = Fore.GREEN + command.NAME + Fore.RESET
        args = Fore.YELLOW + ' '.join(map(lambda arg: '<' + arg + '>', specs.args)) + Fore.RESET
        row = name + (' ' + args if len(specs.args) > 0 else '') + ' ' + command.DESCRIPTION
        print(row)

    print('Join our official ' + Fore.MAGENTA + 'Discord' + Fore.RESET + ' server: https://discord.gg/wEAx6r59as')
