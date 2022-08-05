import requests

import config
from commands.game.complete_stage import complete_stage_command
from commands.game.refresh_client import refresh_client_command
from network.utils import generate_headers


# noinspection SyntaxError
def complete_unfinished_quest_stages_command():
  # ## Will eventually use this to streamline stuff
  # type: (object, object) -> object

  headers = generate_headers('GET', '/user_areas')
  url = config.game_env.url + '/user_areas'
  r = requests.get(url, headers=headers)

  maps = []
  for user in r.json()['user_areas']:
    for map in user['user_sugoroku_maps']:
      if map['cleared_count'] == 0 and map['sugoroku_map_id'] < 999999 and map['sugoroku_map_id'] > 100:
        maps.append(map)

  if len(maps) == 0:
    print("No quests to complete!")
    print('--------------------------------------------')
    return 0

  i = 0
  while i == 0:
    # print(maps)
    for map in maps:
      complete_stage_command(str(map['sugoroku_map_id'])[:-1], str(map['sugoroku_map_id'])[-1])

    headers = generate_headers('GET', '/user_areas')
    r = requests.get(url, headers=headers)
    maps_check = []
    # print(r.json())
    for user in r.json()['user_areas']:
      for map in user['user_sugoroku_maps']:
        if map['cleared_count'] == 0 and map['sugoroku_map_id'] < 999999 and map['sugoroku_map_id'] > 100:
          maps_check.append(map)
    if maps_check == maps:
      i = 1
    else:
      maps = maps_check
      refresh_client_command()
  return 1
