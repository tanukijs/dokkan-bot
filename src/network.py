import json
from typing import Optional, Any

import requests

import config
import crypto
from classes.Game import GamePlatform


def __generate_headers(
        method: str,
        endpoint: str,
        platform: GamePlatform = config.game_platform,
        client_version: str = config.game_env.version_code,
        language: str = 'en',
        asset_version: str = '////',
        database_version: str = '////'
) -> "dict[str: any]":
    return {
        'User-Agent': platform.user_agent,
        'Accept': '*/*',
        'Authorization': crypto.mac(method, endpoint),
        'Content-type': 'application/json',
        'X-Platform': platform.name,
        'X-AssetVersion': asset_version,
        'X-DatabaseVersion': database_version,
        'X-ClientVersion': client_version,
        'X-Language': language
    }


def __get(endpoint: str, params: Optional[Any] = None):
    headers = __generate_headers('GET', endpoint)
    url = config.game_env.url + endpoint
    req = requests.get(url, headers=headers, params=params)
    return req.json()


def __put(endpoint: str, data: Optional[dict[str, Any]] = None):
    headers = __generate_headers('PUT', endpoint)
    url = config.game_env.url + endpoint
    req = requests.put(url, headers=headers, data=json.dumps(data) if data is not None else None)
    return req.json()


def __post(endpoint: str, data: Optional[dict[str, Any]] = None):
    headers = __generate_headers('POST', endpoint)
    url = config.game_env.url + endpoint
    req = requests.post(url, headers=headers, data=json.dumps(data) if data is not None else None)
    return req.json()


def get_user():
    return __get('/user')


def get_user_areas():
    return __get('/user_areas')


def get_events():
    return __get('/events')


def get_eventkagi_items():
    return __get('/eventkagi_items')


def get_cards():
    return __get('/cards')


def get_client_assets_database():
    return __get('/client_assets/database')


def get_gifts():
    return __get('/gifts')


def get_missions():
    return __get('/missions')


def get_awakening_items():
    return __get('/awakening_items')


def get_gashas():
    return __get('/gashas')


def get_support_leaders():
    return __get('/support_leaders')


def get_teams():
    return __get('/teams')


def get_dragonball_sets():
    return __get('/dragonball_sets')


def get_dragonball_sets_wishes(set: str):
    return __get('/dragonball_sets/' + set + '/wishes')


def get_resources_home(
    apologies: bool = False,
    banners: bool = False,
    bonus_schedules: bool = False,
    budokai: bool = False,
    comeback_campaignss: bool = False,
    gifts: bool = False,
    login_bonuses: bool = False,
    rmbattles: bool = False
): return __get('/resources/home', {
    'apologies': str(apologies).lower(),
    'banners': str(banners).lower(),
    'bonus_schedules': str(bonus_schedules).lower(),
    'budokai': str(budokai).lower(),
    'comeback_campaignss': str(comeback_campaignss).lower(),
    'gifts': str(gifts).lower(),
    'login_bonuses': str(login_bonuses).lower(),
    'rmbattles': str(rmbattles).lower()
})


def get_resources_login(
    potential_items: bool = False,
    training_items: bool = False,
    support_items: bool = False,
    treasure_items: bool = False,
    special_items: bool = False
): return __get('/resources/login', {
    'potential_items': str(potential_items).lower(),
    'training_items': str(training_items).lower(),
    'support_items': str(support_items).lower(),
    'treasure_items': str(treasure_items).lower(),
    'special_items': str(special_items).lower()
})


def get_quests_supporters(stage_id: str):
    return __get('/quests/' + stage_id + '/supporters')


def get_rmbattles(clash_id: str):
    return __get('/rmbattles/' + clash_id)


def get_rmbattles_available_user_cards():
    return __get('/rmbattles/available_user_cards')


def get_rmbattles_teams(team_id: str):
    return __get('/rmbattles/teams/' + team_id)


def get_zbattles_supporters(stage_id: str):
    return __get('/z_battles/' + stage_id + '/supporters')


def put_user(
    name: Optional[str] = None,
    is_ondemand: Optional[bool] = None
): return __put('/user', {
    'user': {
        'name': name,
        'is_ondemand': is_ondemand
    }
})


def put_user_recover_act_with_stones():
    return __put('/user/recover_act_with_stone')


def put_support_leaders(support_leader_ids: list[int]):
    return __put('/support_leaders', {
        'support_leader_ids': support_leader_ids
    })


def put_rmbattles_team(team_index: str, user_card_ids: list):
    return __put('/rmbattles/teams/' + team_index, {
        'user_card_ids': user_card_ids
    })


def put_tutorial_finish():
    return __put('/tutorial/finish')


def put_tutorial(progress: str):
    return __put('/tutorial', {'progress': progress})


def put_apologies_accept():
    return __put('/apologies/accept')


def post_login_bonuses_accept():
    return __post('/login_bonuses/accept')


def post_gifts_accept(gift_ids: list):
    return __post('/gifts/accept', {'gift_ids': gift_ids})


def post_missions_accept(mission_ids: list):
    return __post('/missions/accept', {'mission_ids': mission_ids})


def post_teams(
    selected_team_num: int,
    user_card_teams: list
): return __post('/teams', {
    'selected_team_num': selected_team_num,
    'user_card_teams': user_card_teams
})


def post_rmbattles_start(
    clash_id: str,
    stage_id: str,
    is_beginning: bool,
    leader: Any,
    members: list[Any],
    sub_leader: Any
): return __post('/rmbattles/' + clash_id + '/stages/' + stage_id + '/start', {
    'is_beginning': is_beginning,
    'user_card_ids': {
        'leader': leader,
        'members': members,
        'sub_leader': sub_leader
    }
})


def post_rmbattles_dropout(clash_id: str):
    return __post('/rmbattles/' + clash_id + '/stages/dropout', {'reason': 'dropout'})


def post_rmbattles_finish(
    clash_id: str,
    damage: int,
    finished_at_ms: int,
    finished_reason: str,
    is_cleared: bool,
    remaining_hp: int,
    round: int,
    started_at_ms: int,
    token: str
): __post('/rmbattles/' + clash_id + '/stages/finish', {
    'damage': damage,
    'finished_at_ms': finished_at_ms,
    'finished_reason': finished_reason,
    'is_cleared': is_cleared,
    'remaining_hp': remaining_hp,
    'round': round,
    'started_at_ms': started_at_ms,
    'token': token
})


def post_quests_sugoroku_start(stage_id: str, sign: str):
    return __post('/quests/' + stage_id + '/sugoroku_maps/start', {
        'sign': sign
    })


def post_quests_sugoroku_finish(stage_id: str, sign: str):
    return __post('/quests/' + stage_id + '/sugoroku_maps/finish', {
        'sign': sign
    })


def post_zbattles_start(stage_id: str, sign: str):
    return __post('/z_battles/' + stage_id + '/start', {
        'sign': sign
    })


def post_zbattles_finish(
    stage_id: str,
    elapsed_time: int,
    is_cleared: bool,
    level: int,
    s: str,
    t: str,
    token: str,
    used_items: list,
    z_battle_finished_at_ms: int,
    z_battle_started_at_ms: int,
    reason: Optional[str]
):
    return __post('/z_battles/' + stage_id + '/finish', {
        'elapsed_time': elapsed_time,
        'is_cleared': is_cleared,
        'level': level,
        's': s,
        't': t,
        'token': token,
        'reason': reason,
        'used_items': used_items,
        'z_battle_started_at_ms': z_battle_started_at_ms,
        'z_battle_finished_at_ms': z_battle_finished_at_ms
    })


def post_dragonball_sets_wishes(set: str, dragonball_wish_ids: list[int]):
    return __post('/dragonball_sets/' + set + '/wishes', {'dragonball_wish_ids': dragonball_wish_ids})


def post_user_capacity_card():
    return __post('/user/capacity/card')


def post_cards_sell(card_ids: list):
    return __post('/cards/sell', {'card_ids': card_ids})


def post_awakening_item_exchange(awakening_item_id: int, quantity: int):
    return __post('/awakening_items/exchange', {
        'awakening_item_id': awakening_item_id,
        'quantity': quantity
    })


def post_gashas_draw(summon_id: str, type: str):
    return __post('/gashas/' + summon_id + '/courses/' + type + '/draw')


def post_tutorial_gasha():
    return __post('/tutorial/gasha')


def post_missions_put_forward():
    return __post('/missions/put_forward')
