import requests

import config
from network.utils import generate_headers


def get_friend_command(
        stage_id,
        difficulty,
):
    # Returns supporter for given stage_id & difficulty
    # Chooses cpu_supporter if possible

    headers = generate_headers('GET', '/quests/' + stage_id + '/supporters')
    url = config.game_env.url + '/quests/' + stage_id \
          + '/supporters'

    r = requests.get(url, headers=headers)

    '''
    if 'supporters' not in r.json():
        print('Bandai has temp blocked connection... Attempting sign in...')
        response = SignIn(signup, AdId, UniqueId)
        RefreshClient()
        headers = {
        'User-Agent': config.game_platform.user_agent,
        'Accept': '*/*',
        'Authorization': GetMac('GET', '/quests/' + stage_id
                                + '/supporters', MacId, secret1),
        'Content-type': 'application/json',
        'X-Platform': config.game_platform.name,
        'X-AssetVersion': '////',
        'X-DatabaseVersion': '////',
        'X-ClientVersion': config.game_env.version_code,
        }
        r = requests.get(url, headers=headers)
    '''
    # If CPU supporter available, choose it every time
    if 'cpu_supporters' in r.json():
        if int(difficulty) == 5:
            if 'super_hard3' in r.json()['cpu_supporters']:
                if len(r.json()['cpu_supporters']['super_hard3'
                       ]['cpu_friends']) > 0:
                    return {
                        'is_cpu': True,
                        'id': r.json()['cpu_supporters']['super_hard3']
                        ['cpu_friends'][0]['id'],
                        'leader': r.json()['cpu_supporters']['super_hard3']
                        ['cpu_friends'][0]['card_id']
                    }
        if int(difficulty) == 4:
            if 'super_hard2' in r.json()['cpu_supporters']:
                if len(r.json()['cpu_supporters']['super_hard2'
                       ]['cpu_friends']) > 0:
                    return {
                        'is_cpu': True,
                        'id': r.json()['cpu_supporters']['super_hard2']
                        ['cpu_friends'][0]['id'],
                        'leader': r.json()['cpu_supporters']['super_hard2']
                        ['cpu_friends'][0]['card_id']
                    }
        if int(difficulty) == 3:
            if 'super_hard1' in r.json()['cpu_supporters']:
                if len(r.json()['cpu_supporters']['super_hard1'
                       ]['cpu_friends']) > 0:
                    return {
                        'is_cpu': True,
                        'id': r.json()['cpu_supporters']['super_hard1']
                        ['cpu_friends'][0]['id'],
                        'leader': r.json()['cpu_supporters']['super_hard1']
                        ['cpu_friends'][0]['card_id']
                    }
        if int(difficulty) == 2:
            if 'very_hard' in r.json()['cpu_supporters']:
                if len(r.json()['cpu_supporters']['very_hard'
                       ]['cpu_friends']) > 0:
                    return {
                        'is_cpu': True,
                        'id': r.json()['cpu_supporters']['very_hard']
                        ['cpu_friends'][0]['id'],
                        'leader': r.json()['cpu_supporters']['very_hard']
                        ['cpu_friends'][0]['card_id']
                    }
        if int(difficulty) == 1:
            if 'hard' in r.json()['cpu_supporters']:
                if len(r.json()['cpu_supporters']['hard']['cpu_friends'
                       ]) > 0:
                    return {
                        'is_cpu': True,
                        'id': r.json()['cpu_supporters']['hard']
                        ['cpu_friends'][0]['id'],
                        'leader': r.json()['cpu_supporters']['hard']
                        ['cpu_friends'][0]['card_id']
                    }
        if int(difficulty) == 0:
            if 'normal' in r.json()['cpu_supporters']:
                if len(r.json()['cpu_supporters']['normal'
                       ]['cpu_friends']) > 0:
                    return {
                        'is_cpu': True,
                        'id': r.json()['cpu_supporters']['normal']
                        ['cpu_friends'][0]['id'],
                        'leader': r.json()['cpu_supporters']['normal']
                        ['cpu_friends'][0]['card_id']
                    }

    return {
        'is_cpu': False,
        'id': r.json()['supporters'][0]['id'],
        'leader': r.json()['supporters'][0]['leader']['card_id']
    }
