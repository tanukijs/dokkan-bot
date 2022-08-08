from pathlib import Path

from colorama import Fore, Style

import config
from classes.Game import GameAccount
from commands.game.daily_login import daily_login_command
from commands.game import tutorial, gifts, missions

from services.account import AccountService
from services.database import DatabaseService

NAME = 'load'
DESCRIPTION = 'Load a save'


def run(file_name: str):
    file_path = Path('saves', file_name + '.json')
    if not file_path.exists():
        print(Fore.RED + Style.BRIGHT + "Could not find " + file_name)
        return

    config.game_account = GameAccount.from_file(file_path)
    config.game_account = AccountService.login(config.game_account)
    config.game_account.to_file(file_path)

    DatabaseService.fetch_latest()
    tutorial.run()
    daily_login_command()
    gifts.run()
    missions.run()
