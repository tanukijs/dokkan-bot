from typing import Optional
from collections import namedtuple

from colorama import Fore

from models.game import Cards, CardAwakeningRoutes, CardAwakenings, AwakeningItems

RARITY_NAMES = ['N', 'R', 'SR', 'SSR', 'UR', 'LR']
get_for_awakening_result = namedtuple('literal', 'required_medals medal_names')


class MedalService:
    @staticmethod
    def get_for_awakening(card_ids: list[int]) -> get_for_awakening_result:
        required_medals: dict[int, int] = {}
        medal_names: dict[int, str] = {}

        for card_id in card_ids:
            card: Cards = Cards.get(card_id)
            rarity = RARITY_NAMES[card.rarity]
            print(card_id, '|', rarity, Fore.GREEN + card.name + Fore.RESET)

            # Search for required medals to evolve
            awakening_route: Optional[CardAwakeningRoutes] = CardAwakeningRoutes.select()\
                .where(CardAwakeningRoutes.type.in_(['CardAwakeningRoute::Dokkan', 'CardAwakeningRoute::Zet']) &
                       (CardAwakeningRoutes.card_id == card_id))\
                .first()

            if awakening_route is None:
                continue

            awakenings: list[CardAwakenings] = CardAwakenings.select()\
                .where(CardAwakenings.card_awakening_set_id == awakening_route.card_awakening_set_id)

            for awakening in awakenings:
                awakening_item: Optional[AwakeningItems] = AwakeningItems.get(awakening.awakening_item_id)
                medal_names[awakening.awakening_item_id] = repr(awakening_item.name)
                required_medals[awakening.awakening_item_id] = \
                    required_medals.get(awakening.awakening_item_id, 0) + awakening.quantity

            # Recursive
            if awakening_route.awaked_card_id is not None:
                info = MedalService.get_for_awakening([awakening_route.awaked_card_id])
                for key, value in info.required_medals: required_medals[key] = required_medals.get(key, 0) + value
                for key, value in info.medal_names: medal_names[key] = value

        return get_for_awakening_result(
            required_medals=required_medals,
            medal_names=medal_names
        )
