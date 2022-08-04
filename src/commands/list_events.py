import requests
from colorama import Back, Fore, Style

import config
from network.utils import generate_headers


def list_events_command():
    # Prints all currently available events
    # JP Translated
    headers = generate_headers('GET', '/events')
    url = config.gb_url + '/events'
    r = requests.get(url, headers=headers)
    events = r.json()

    area_id = None
    for event in events['events']:
        for quest in event['quests']:
            if str(event['id']) != area_id:
                area_id = str(event['id'])
                try:
                    config.Model.set_connection_resolver(config.db_glb)
                    area_name = str(config.Area.where('id', '=', area_id).first().name)
                except:
                    config.Model.set_connection_resolver(config.db_jp)
                    area_name = str(config.Area.where('id', '=', area_id).first().name)
                print('--------------------------------------------')
                print(Back.BLUE + Fore.WHITE + Style.BRIGHT \
                      + area_name)
                print('--------------------------------------------')

            ids = quest['id']
            config.Model.set_connection_resolver(config.db_glb)
            sugorokus = config.Sugoroku.where('quest_id', '=', int(ids)).get()
            if len(sugorokus) < 1:
                config.Model.set_connection_resolver(config.db_jp)
                sugorokus = config.Sugoroku.where('quest_id', '=', int(ids)).get()
            difficulties = []
            for sugoroku in sugorokus:
                difficulties.append(sugoroku.difficulty)
            print(config.Quests.find(ids).name + ' ' + str(ids) \
                  + ' Difficulties: ' + str(difficulties) \
                  + ' AreaID: ' + str(event['id']))
