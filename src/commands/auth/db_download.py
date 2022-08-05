from random import randint

import requests
from colorama import Fore, Style

import config
from commands.auth.signin import signin_command
from commands.auth.signup import signup_command
from network.utils import generate_headers
from pysqlsimplecipher.decryptor import decrypt_file


def db_download_command():
    config.game_account = signup_command(False)
    access_token, secret = signin_command(config.game_account.identifier)
    config.game_account.access_token = access_token
    config.game_account.secret = secret

    headers = generate_headers('GET', '/client_assets/database')
    url = config.game_env.url + '/client_assets/database'
    r = requests.get(url, allow_redirects=True, headers=headers)
    dist_db_version = r.json()['version']

    if config.client.gb_db_version == dist_db_version:
        print(Fore.GREEN + Style.BRIGHT + 'Database is already up to date')
        return

    print(Fore.RED + Style.BRIGHT + 'Downloading latest global database...')
    url = r.json()['url']
    r = requests.get(url, allow_redirects=True)
    temp_db_name = str(randint(10_000_00, 99_999_99)) + '.db'
    open(temp_db_name, 'wb').write(r.content)

    print(Fore.RED + Style.BRIGHT + 'Decrypting latests database... This can take a few minutes...')
    config.game_env.db_path.parent.mkdir(exist_ok=True, parents=True)
    decrypt_file(temp_db_name, config.game_env.db_password, str(config.game_env.db_path.absolute()))
    config.client.gb_db_version = dist_db_version
    config.client.save()
    print(Fore.GREEN + Style.BRIGHT + 'Database update complete.')
