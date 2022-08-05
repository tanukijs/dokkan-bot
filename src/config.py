from pathlib import Path
from typing import Optional

from orator import Model

from classes.Client import ClientConfig
from classes.Game import GamePlatform, GameEnvironment, GameAccount

'''
version codes these can be updated automatically but it'd require an APK download.
it's better to manually update them along with the bot to prevent account bans from game-breaking changes.
noted here: https://twitter.com/dbzspace/status/1106316112638210050
we're not sure what the 2 hashes are of... - k1mpl0s
'''

ANDROID_PLATFORM = GamePlatform(
    name='android',
    user_agent='Dalvik/2.1.0 (Linux; Android 7.0; SM-E7000)',
    device_name='SM',
    device_model='SM-E7000',
    os_version='7.0'
)

IOS_PLATFORM = GamePlatform(
    name='ios',
    user_agent='CFNetwork/808.3 Darwin/16.3.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X)',
    device_name='iPhone',
    device_model='iPhone XR',
    os_version='13.0'
)

GB_ENV = GameEnvironment(
    name='global',
    url='https://ishin-global.aktsk.com',
    port=443,
    version_code='5.4.0-c836f25f0997f70e1f5210864a41e078b021034d6a7554e6f70e70e527d82aee',
    db_password=bytearray('9bf9c6ed9d537c399a6c4513e92ab24717e1a488381e3338593abd923fc8a13b'.encode('utf8')),
    db_path=Path('data/gb.db')
)

JP_ENV = GameEnvironment(
    name='japan',
    url='https://ishin-production.aktsk.jp',
    port=443,
    version_code='5.5.1-3dce6ea90bfc690de24bd70fbea42ab4310129aa36cad35dfbbe2fcb096f8711',
    db_password=bytearray('2db857e837e0a81706e86ea66e2d1633'.encode('utf8')),
    db_path=Path('data/jp.db')
)

client: ClientConfig = ClientConfig(path=Path('./config.json'))
game_env: GameEnvironment = GB_ENV
game_platform: GamePlatform = ANDROID_PLATFORM
game_account: Optional[GameAccount] = None
Model.set_connection_resolver(game_env.db_manager)

### Reroll parameters
last_save_name = ''
reroll_state = False
deck = 1
allow_stamina_refill = True


class LeaderSkills(Model):
    __table__ = 'leader_skills'


class LinkSkills(Model):
    __table__ = 'link_skills'


class AreaTabs(Model):
    __table__ = 'area_tabs'


class CardSpecials(Model):
    __table__ = 'card_specials'


class Passives(Model):
    __table__ = 'passive_skill_sets'


class Supers(Model):
    __table__ = 'specials'


class ZBattles(Model):
    __table__ = 'z_battle_stage_views'


class CardCategories(Model):
    __table__ = 'card_categories'


class CardCardCategories(Model):
    __table__ = 'card_card_categories'


class TreasureItems(Model):
    __table__ = 'treasure_items'


class AwakeningItems(Model):
    __table__ = 'awakening_items'


class SupportItems(Model):
    __table__ = 'support_items'


class PotentialItems(Model):
    __table__ = 'potential_items'


class SpecialItems(Model):
    __table__ = 'special_items'


class TrainingItems(Model):
    __table__ = 'training_items'


class Cards(Model):
    __table__ = 'cards'


class Quests(Model):
    __table__ = 'quests'


class Ranks(Model):
    __table__ = 'rank_statuses'


class TrainingFields(Model):
    __table__ = 'training_fields'


class Sugoroku(Model):
    __table__ = 'sugoroku_maps'


class Area(Model):
    __table__ = 'areas'


class Medal(Model):
    __table__ = 'awakening_items'
