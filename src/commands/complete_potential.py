import requests

import config
from commands.complete_stage import complete_stage_command
from network.utils import generate_headers


def complete_potential_command():
    headers = generate_headers('GET', '/events')
    url = config.gb_url + '/events'
    r = requests.get(url, headers=headers)
    events = r.json()
    for event in events['events']:
        if event['id'] >= 140 and event['id'] < 145:
            for quest in event['quests']:
                ids = quest['id']
                config.Model.set_connection_resolver(config.db_jp)
                sugorokus = config.Sugoroku.where('quest_id', '=',
                                                  int(ids)).get()
                difficulties = []
                for sugoroku in sugorokus:
                    config.Model.set_connection_resolver(config.db_jp)
                    complete_stage_command(str(ids), sugoroku.difficulty)
