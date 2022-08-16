from colorama import Fore, Style

import network
from config import GameContext

NAME = 'gifts'
DESCRIPTION = 'Accept gifts'
CONTEXT = [GameContext.GAME]


def run():
    res = network.get_gifts()
    gifts = []
    for gift in res['gifts']:
        gifts.append(gift['id'])

    if len(gifts) == 0:
        print('No gifts to accept...')
        return 0

    chunks = [gifts[x:x + 25] for x in range(0, len(gifts), 25)]
    for index, data in enumerate(chunks):
        res = network.post_gifts_accept(data)
        if 'error' not in res:
            print(Fore.GREEN + Style.BRIGHT + 'Gifts Accepted (' + str(index + 1) + '/' + str(len(chunks)) + ')')
        else:
            print(res)
