import config
from commands import help
from config import GameContext

NAME = 'unload'
DESCRIPTION = 'Disconnect and get back to the login menu'
CONTEXT = [GameContext.GAME]


def run():
    config.game_context = GameContext.AUTH
    config.game_account = None
    help.run()
