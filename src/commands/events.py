from typing import Optional

from colorama import Back, Fore

import config
import models.game
import network

NAME = 'events'
DESCRIPTION = 'List active events'
CONTEXT = [config.GameContext.GAME]


def run():
    events = network.get_events()
    area_id = None

    for event in events['events']:
        for quest in event['quests']:
            if event['id'] != area_id:
                area_id = event['id']
                area: Optional[models.game.Areas] = models.game.Areas.get_by_id(area_id)
                area_name = area.name.replace('\n', '')
                print('--------------------------------------------')
                print(Back.YELLOW + Fore.WHITE + '[' + str(area_id) + '] ' + area_name + Fore.RESET)
                print('--------------------------------------------')

            quest_id = quest['id']
            sugorokus: list[models.game.SugorokuMaps] = models.game.SugorokuMaps.select().where(models.game.SugorokuMaps.quest_id == int(quest_id))
            difficulties = []
            for sugoroku in sugorokus:
                difficulties.append(sugoroku.difficulty)

            quest: Optional[models.game.Quests] = models.game.Quests.get_by_id(quest_id)
            print(quest_id, Fore.GREEN + quest.name + Fore.RESET, str(difficulties))
