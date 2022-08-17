from typing import Optional

import config
import models.game
import network

NAME = 'cards'
DESCRIPTION = 'List your cards'
CONTEXT = [config.GameContext.GAME]
_CARD_TYPES = ['AGL', 'TEQ', 'INT', 'STR', 'PHY']
_CARD_TYPES_COLORS = ['gold2', 'red', 'blue', 'green', 'purple']


def run():
    res = network.get_cards()

    for card in res['cards']:
        card_id = card['card_id']
        db_card: Optional[models.game.Cards] = models.game.Cards.get_by_id(card_id)
        card_name = db_card.name
        card_element = int(str(db_card.element)[-1])
        card_type = _CARD_TYPES[card_element]
        print('★' if card['is_favorite'] else '', card_id, card['id'], '[' + card_type + ']', card_name)
