from pathlib import Path

from colorama import Fore, Style

import config
import network
from classes.Game import GameAccount
from commands import gifts, missions, tutorial, help

from services.account import AccountService
from services.database import DatabaseService

NAME = 'load'
DESCRIPTION = 'Load a save'
CONTEXT = [config.GameContext.AUTH]


def run(file_name: str):
    file_path = Path('saves', file_name + '.json')
    if not file_path.exists():
        print(Fore.RED + Style.BRIGHT + "Could not find " + file_name)
        return

    config.game_account = GameAccount.from_file(file_path)
    config.game_account = AccountService.login(config.game_account)
    print(Fore.GREEN + 'Welcome back' + Style.RESET_ALL)
    config.game_account.to_file(file_path)
    config.game_context = config.GameContext.GAME

    DatabaseService.fetch_latest()
    tutorial.run()
    network.get_resources_home(
        apologies=True,
        banners=True,
        bonus_schedules=True,
        budokai=True,
        dragonball_sets=True,
        gifts=True,
        login_bonuses=True,
        missions=True,
        random_login_bonuses=True,
        rmbattles=True,
        comeback_campaigns=True
    )
    network.post_login_bonuses_accept()
    gifts.run()
    missions.run()
    help.run()
