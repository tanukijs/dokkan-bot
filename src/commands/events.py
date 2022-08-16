from colorama import Back, Fore

import config
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
                area = config.Area.where('id', '=', area_id).first()
                area_name = area.name.replace('\n', '')
                print('--------------------------------------------')
                print(Back.YELLOW + Fore.WHITE + '[' + str(area_id) + '] ' + area_name + Fore.RESET)
                print('--------------------------------------------')

            quest_id = quest['id']
            sugorokus = config.Sugoroku.where('quest_id', '=', int(quest_id)).get()
            difficulties = []
            for sugoroku in sugorokus:
                difficulties.append(sugoroku.difficulty)

            quest = config.Quests.find(quest_id)
            print(quest_id, Fore.GREEN + quest.name + Fore.RESET, str(difficulties))
