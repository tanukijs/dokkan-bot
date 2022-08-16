import network
from config import GameContext

NAME = 'rename'
DESCRIPTION = 'Rename your account'
CONTEXT = [GameContext.GAME]


def run(name: str):
    r = network.put_user(name=name)
    if 'error' in r:
        print(r)
    else:
        print("Name changed to: " + name)
