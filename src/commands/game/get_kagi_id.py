import json

import requests

import config
from network.utils import generate_headers


def get_kagi_id_command(stage):
    # return kagi ID to use for a stage

    headers = generate_headers('GET', '/eventkagi_items')
    url = config.game_env.url + '/eventkagi_items'
    r = requests.get(url, headers=headers)

    kagi_items = r.json()['eventkagi_items']
    area_id = config.Quests.find(stage).area_id
    area_category = config.Area.find(area_id).category
    areatabs = config.AreaTabs.all()
    for tab in areatabs:
        j = json.loads(tab.area_category_ids)
        if area_category in j['area_category_ids']:
            kagi_id = int(tab.id)
            print('Kagi ID: ' + str(tab.id))
            break
    for kagi in kagi_items:
        if kagi['eventkagi_item_id'] == kagi_id:
            if kagi['quantity'] > 0:
                print('kagi_id' + kagi_id)
                return kagi_id
            else:
                return None

    return None
