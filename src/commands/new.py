import base64
import webbrowser
from pathlib import Path

from colorama import Fore, Style

import config
import crypto
import network
from classes.Game import GameAccount
from commands import load

NAME = 'new'
DESCRIPTION = 'Create a new Dokkan account'
CONTEXT = [config.GameContext.AUTH]


def run(file_name: str):
    file_path = Path(config.ROOT_DIR, 'saves', file_name.strip() + '.json')
    if file_path.exists():
        print('this name is already taken. please select another one.')
        return

    unique_id = crypto.generate_unique_id()
    req = network.post_auth_signup(unique_id=unique_id)

    if 'captcha_url' not in req:
        print(Fore.RED + Style.BRIGHT + 'Captcha could not be loaded...')
        return None

    webbrowser.open(req['captcha_url'], new=2)
    captcha_session_key = req['captcha_session_key']
    print('Opening captcha in browser. Press' + Fore.RED + Style.BRIGHT + ' ENTER ' + Style.RESET_ALL + 'once you have solved it...')
    input()

    req = network.post_auth_signup(
        unique_id=unique_id,
        captcha_session_key=captcha_session_key
    )

    identifier = base64.b64decode(req['identifier']).decode('utf-8')
    config.game_account = GameAccount(
        unique_id=unique_id,
        identifier=identifier
    )
    config.game_account.to_file(file_path)
    load.run(file_name)
