import requests

import config
from commands.complete_stage import complete_stage_command
from commands.refresh_client import refresh_client_command
from network.utils import generate_headers


def complete_unfinished_events_command():
    # ## Will eventually use this to streamline stuff
    # type: (object, object) -> object
    ### Get current event IDs
    # ## Gets current events json which contains some useful data

    headers = generate_headers('GET', '/events')
    url = config.gb_url + '/events'
    r = requests.get(url, headers=headers)
    events = r.json()
    event_ids = []
    for event in events['events']:
        event_ids.append(event['id'])
    event_ids = sorted(event_ids)
    try:
        event_ids.remove(135)
    except:
        None

    ### Complete areas if they are in the current ID pool
    headers = generate_headers('GET', '/user_areas')
    url = config.gb_url + '/user_areas'
    r = requests.get(url, headers=headers)
    areas = r.json()['user_areas']
    i = 1
    for area in areas:
        if area['area_id'] in event_ids:
            for stage in area['user_sugoroku_maps']:
                if stage['cleared_count'] == 0:
                    complete_stage_command(str(stage['sugoroku_map_id'])[:-1], str(stage['sugoroku_map_id'])[-1])
                    i += 1
        if i % 30 == 0:
            refresh_client_command()
