import config
from config import GameContext
from commands import help

NAME = 'unload'
DESCRIPTION = 'Disconnect and get back to the login menu'
CONTEXT = [GameContext.GAME]


def run():
    config.game_context = GameContext.AUTH
    config.game_account = None
    help.run()
