import requests
from colorama import Back, Fore, Style

import config
from network.utils import generate_headers


def list_events_command():
    # Prints all currently available events
    # JP Translated
    headers = generate_headers('GET', '/events')
    url = config.game_env.url + '/events'
    r = requests.get(url, headers=headers)
    events = r.json()

    area_id = None
    for event in events['events']:
        for quest in event['quests']:
            if str(event['id']) != area_id:
                area_id = str(event['id'])
                config.Model.set_connection_resolver(config.game_env.db_manager)
                area_name = str(config.Area.where('id', '=', area_id).first().name)
                print('--------------------------------------------')
                print(Back.BLUE + Fore.WHITE + Style.BRIGHT \
                      + area_name)
                print('--------------------------------------------')

            ids = quest['id']
            config.Model.set_connection_resolver(config.game_env.db_manager)
            sugorokus = config.Sugoroku.where('quest_id', '=', int(ids)).get()
            if len(sugorokus) < 1:
                sugorokus = config.Sugoroku.where('quest_id', '=', int(ids)).get()
            difficulties = []
            for sugoroku in sugorokus:
                difficulties.append(sugoroku.difficulty)
            print(config.Quests.find(ids).name + ' ' + str(ids) \
                  + ' Difficulties: ' + str(difficulties) \
                  + ' AreaID: ' + str(event['id']))
