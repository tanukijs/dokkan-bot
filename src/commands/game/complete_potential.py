import requests

import config
from commands.game.complete_stage import complete_stage_command
from network.utils import generate_headers


def complete_potential_command():
  headers = generate_headers('GET', '/events')
  url = config.game_env.url + '/events'
  r = requests.get(url, headers=headers)
  events = r.json()
  for event in events['events']:
    if event['id'] >= 140 and event['id'] < 145:
      for quest in event['quests']:
        ids = quest['id']
        sugorokus = config.Sugoroku.where('quest_id', '=',
                                          int(ids)).get()
        difficulties = []
        for sugoroku in sugorokus:
          complete_stage_command(str(ids), sugoroku.difficulty)
