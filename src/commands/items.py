from typing import Optional

from colorama import Back, Fore

import config
import models.game
import network

NAME = 'items'
DESCRIPTION = 'List your inventory items'
CONTEXT = [config.GameContext.GAME]


def print_title(title: str):
    print('--------------------------------------------')
    print(Back.YELLOW + Fore.WHITE + title + Fore.RESET)
    print('--------------------------------------------')


def run():
    r = network.get_resources_login(
        awakening_items=True,
        potential_items=True,
        training_items=True,
        support_items=True,
        treasure_items=True,
        special_items=True
    )

    print_title('Awakening Items')
    for item in r['awakening_items']:
        awakening_item: Optional[models.game.AwakeningItems] = models.game.AwakeningItems.get_by_id(item['awakening_item_id'])
        print(awakening_item.name + ' x' + str(item['quantity']))

    print_title('Support Items')
    for item in r['support_items']['items']:
        support_item: Optional[models.game.SupportItems] = models.game.SupportItems.get_by_id(item['item_id'])
        print(support_item.name + ' x' + str(item['quantity']))

    print_title('Training Items')
    for item in r['training_items']:
        training_item: Optional[models.game.TrainingItems] = models.game.TrainingItems.get_by_id(item['training_item_id'])
        print(training_item.name + ' x' + str(item['quantity']))

    print_title('Potential Items')
    for item in reversed(r['potential_items']['user_potential_items']):
        potential_item: Optional[models.game.PotentialItems] = models.game.PotentialItems.get_by_id(item['potential_item_id'])
        print(potential_item.name + ' x' + str(item['quantity']))

    print_title('Treasure Items')
    for item in r['treasure_items']['user_treasure_items']:
        treasure_item: Optional[models.game.TreasureItems] = models.game.TreasureItems.get_by_id(item['treasure_item_id'])
        print(treasure_item.name + ' x' + str(item['quantity']))

    print_title('Special Items')
    for item in r['special_items']:
        special_item: Optional[models.game.SpecialItems] = models.game.SpecialItems.get_by_id(item['special_item_id'])
        print(special_item.name + ' x' + str(item['quantity']))
