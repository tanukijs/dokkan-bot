from enum import Enum
from os import path
from pathlib import Path
from typing import Optional

from classes.Client import ClientConfig
from classes.Game import GamePlatform, GameEnvironment, GameAccount

'''
version codes these can be updated automatically but it'd require an APK download.
it's better to manually update them along with the bot to prevent account bans from game-breaking changes.
noted here: https://twitter.com/dbzspace/status/1106316112638210050
we're not sure what the 2 hashes are of... - k1mpl0s
'''
ROOT_DIR: Path = Path(path.dirname(path.abspath(__file__))).parent

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
    bundle_id='com.bandainamcogames.dbzdokkanww',
    url='https://ishin-global.aktsk.com',
    port=443,
    version_code='5.5.1-0f5482cd907214ad110feaf1f7bfc2300f72a94af7743f54719d2442b7ec57bd',
    db_password=bytearray('9bf9c6ed9d537c399a6c4513e92ab24717e1a488381e3338593abd923fc8a13b'.encode('utf8')),
    db_path=Path(ROOT_DIR, 'data/gb.db'),
    country='FR',
    currency='EUR'
)

JP_ENV = GameEnvironment(
    name='japan',
    bundle_id='',
    url='https://ishin-production.aktsk.jp',
    port=443,
    version_code='5.5.1-3dce6ea90bfc690de24bd70fbea42ab4310129aa36cad35dfbbe2fcb096f8711',
    db_password=bytearray('2db857e837e0a81706e86ea66e2d1633'.encode('utf8')),
    db_path=Path(ROOT_DIR, 'data/jp.db'),
    country='FR',
    currency='EUR'
)


class GameContext(Enum):
    AUTH = 1
    GAME = 2


client: ClientConfig = ClientConfig(path=Path(ROOT_DIR, 'config.json'))
game_env: GameEnvironment = GB_ENV
game_platform: GamePlatform = ANDROID_PLATFORM
game_account: Optional[GameAccount] = None
game_context: GameContext = GameContext.AUTH

# Reroll parameters
last_save_name = ''
reroll_state = False
deck = 1
allow_stamina_refill = True
