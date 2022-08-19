from typing import Optional

import models.game


class CardService:
    @staticmethod
    def get_by_max_rarity(account_cards: list, rarities: list[int], skip_dupes: bool = True) -> list[int]:
        account_card_ids = [row['card_id'] for row in account_cards]
        card_ids: list[int] = []

        for account_card_id in account_card_ids:
            awakenings = CardService.get_awakenings(account_card_id)
            dupes_awakened = [awaked_card_id for _, _, awaked_card_id in awakenings if
                              awaked_card_id is not None and awaked_card_id in account_card_ids]
            if skip_dupes and len(dupes_awakened) > 0: continue
            max_rarity, card_id, _ = awakenings[len(awakenings) - 1]
            if card_id == account_card_id or max_rarity not in rarities: continue
            if skip_dupes and account_card_id in card_ids: continue
            card_ids.append(account_card_id)

        return card_ids

    @staticmethod
    def get_awakenings(card_id: int) -> list[tuple[str, int, int]]:
        awakening_route: Optional[models.game.CardAwakeningRoutes] = models.game.CardAwakeningRoutes.select()\
            .where(models.game.CardAwakeningRoutes.type.in_(['CardAwakeningRoute::Dokkan', 'CardAwakeningRoute::Zet']) &
                   (models.game.CardAwakeningRoutes.card_id == card_id)).first()
        awoken_card_id: Optional[int] = awakening_route.awaked_card_id if awakening_route is not None else None
        card: Optional[models.game.Cards] = models.game.Cards.get_by_id(card_id)

        result_item = [card.rarity, card_id, awoken_card_id]
        return [result_item] if awoken_card_id is None else [result_item, *CardService.get_awakenings(awoken_card_id)]
