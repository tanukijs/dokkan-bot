from config import GameContext

NAME = 'exit'
DESCRIPTION = 'Close the bot'
CONTEXT = [GameContext.AUTH, GameContext.GAME]


def run():
    print('bye-bye king...')
    exit()
