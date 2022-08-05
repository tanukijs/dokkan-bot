import json

import requests

import config


def get_transfer_code_command():
    # Returns transfer code in dictionary

    headers = generate_headers('POST', '/auth/link_codes')
    data = {'eternal': 1}
    url = config.game_env.url + '/auth/link_codes'

    r = requests.post(url, data=json.dumps(data), headers=headers)
    try:
        print(r.json()['link_code'])
        return {'transfer_code': r.json()['link_code']}
    except:
        return None
