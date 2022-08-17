import network
from config import GameContext
from services.card import CardService

NAME = 'farm medals'
DESCRIPTION = 'Collect medals to fully awaken given units'
CONTEXT = [GameContext.GAME]
__RARITY_NAMES = ['N', 'R', 'SR', 'SSR', 'UR', 'LR']


def run(rarity: str):
    try:
        rarity_index = __RARITY_NAMES.index(rarity.upper())
    except ValueError:
        print('rarity not found')
        return

    account_cards = network.get_cards()['cards']
    matching_cards = CardService.get_by_max_rarity(account_cards, [rarity_index])
    print(matching_cards)
