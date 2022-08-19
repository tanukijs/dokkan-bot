from typing import Optional

from colorama import Fore

import models.game
import network
from config import GameContext
from services.card import CardService
from services.medal import MedalService
from commands import stage

NAME = 'farm medals'
DESCRIPTION = 'Collect medals to fully awaken a copy of each units'
CONTEXT = [GameContext.GAME]
__RARITY_NAMES = ['N', 'R', 'SR', 'SSR', 'UR', 'LR']


def run(*rarities: list[str]):
    try:
        rarity_indexes = list(map(lambda rarity: __RARITY_NAMES.index(rarity.upper()), rarities))
    except ValueError:
        print(f'only these rarities are available: {__RARITY_NAMES}')
        return

    # Fetch cards
    account_cards = network.get_cards()['cards']
    matching_card_ids = CardService.get_by_max_rarity(account_cards, rarity_indexes)
    info = MedalService.get_for_awakening(matching_card_ids)

    # Removing my inventory medals
    awakening_items = network.get_awakening_items()['awakening_items']
    missing_medals: dict[int, int] = {}
    for medal_id in info.required_medals:
        required_quantity: int = info.required_medals[medal_id]
        inventory_items = [item for item in awakening_items if item['awakening_item_id'] == medal_id]
        inventory_quantity: int = inventory_items[0]['quantity'] if len(inventory_items) > 0 else 0

        medal_name = info.medal_names[medal_id]
        quantity_percentage = round((inventory_quantity / required_quantity) * 100, 2)
        opt_out_quantity = f'{Fore.RED if quantity_percentage < 100 else None}{str(quantity_percentage)}%{Fore.RESET}'
        print(f'{medal_id} | {Fore.GREEN}{medal_name}{Fore.RESET} | {str(inventory_quantity)} / {str(required_quantity)} {opt_out_quantity}')
        if inventory_quantity >= required_quantity: continue
        missing_medals[medal_id] = required_quantity - inventory_quantity

    # Searching for stages
    medals_sugoroku_ids: dict[int, list[int]] = {}
    resolutions_awakening_items = network.get_item_reverse_resolutions_awakening_items()
    for item in resolutions_awakening_items:
        awakening_item_id: int = item['awakening_item_id']
        if awakening_item_id not in missing_medals:
            continue

        for acquirement in item['acquirements']:
            if 'sugoroku_map_ids' not in acquirement:
                continue

            if awakening_item_id not in medals_sugoroku_ids:
                medals_sugoroku_ids[awakening_item_id] = []

            sugoroku_map_ids: list[int] = acquirement['sugoroku_map_ids']
            medals_sugoroku_ids[awakening_item_id].extend(sugoroku_map_ids)

    # Processing to stages
    # Check if the user has access to the latest stage
    # After each stages, refresh user medals with rewards
    for medal_id in medals_sugoroku_ids:
        sugoroku_map_ids = medals_sugoroku_ids[medal_id]
        sugoroku_map_id = sugoroku_map_ids[-1]
        sugoroku: Optional[models.game.SugorokuMaps] = models.game.SugorokuMaps.get_by_id(sugoroku_map_id)
        stage.run(sugoroku.quest_id, sugoroku.difficulty)
