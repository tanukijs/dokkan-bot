from colorama import Fore, Style

import network


def accept_gifts_command():
    r = network.get_gifts()

    gifts = []
    for x in r['gifts']:
        gifts.append(x['id'])

    # AcceptGifts
    if len(gifts) == 0:
        print('No gifts to accept...')
        return 0

    chunks = [gifts[x:x + 25] for x in range(0, len(gifts), 25)]
    for data in chunks:
        r = network.post_gifts_accept(data)
    if 'error' not in r:
        print(Fore.GREEN + Style.BRIGHT + 'Gifts Accepted...')
    else:
        print(r)
