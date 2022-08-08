import network

NAME = 'rename'
DESCRIPTION = 'Rename your account in-game'


def run(name: str):
    r = network.put_user(name=name)
    if 'error' in r:
        print(r)
    else:
        print("Name changed to: " + name)
