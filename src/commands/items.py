from colorama import Back, Fore

import config
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
        potential_items=True,
        training_items=True,
        support_items=True,
        treasure_items=True,
        special_items=True
    )

    print_title('Support Items')
    for item in r['support_items']['items']:
        support_item = config.SupportItems.find_or_fail(item['item_id'])
        print(support_item.name + ' x' + str(item['quantity']))

    print_title('Training Items')
    for item in r['training_items']:
        training_item = config.TrainingItems.find(item['training_item_id'])
        print(training_item.name + ' x' + str(item['quantity']))

    print_title('Potential Items')
    for item in reversed(r['potential_items']['user_potential_items']):
        potential_item = config.PotentialItems.find(item['potential_item_id'])
        print(potential_item.name + ' x' + str(item['quantity']))

    print_title('Treasure Items')
    for item in r['treasure_items']['user_treasure_items']:
        treasure_item = config.TreasureItems.find(item['treasure_item_id'])
        print(treasure_item.name + ' x' + str(
            item['quantity']))

    print_title('Special Items')
    for item in r['special_items']:
        special_item = config.SpecialItems.find(item['special_item_id'])
        print(special_item.name + ' x' + str(item['quantity']))
