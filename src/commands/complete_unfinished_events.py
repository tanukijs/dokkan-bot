from commands.game.refresh_client import refresh_client_command

import network
from commands.stage import complete_stage_command


# noinspection SyntaxError
def complete_unfinished_events_command():
    events = network.get_events()
    event_ids = []
    for event in events['events']:
        event_ids.append(event['id'])
    event_ids = sorted(event_ids)
    try:
        event_ids.remove(135)
    except:
        None

    ### Complete areas if they are in the current ID pool
    r = network.get_user_areas()
    areas = r['user_areas']
    i = 1
    for area in areas:
        if area['area_id'] in event_ids:
            for stage in area['user_sugoroku_maps']:
                if stage['cleared_count'] == 0:
                    complete_stage_command(str(stage['sugoroku_map_id'])[:-1], str(stage['sugoroku_map_id'])[-1])
                    i += 1
        if i % 30 == 0:
            refresh_client_command()
