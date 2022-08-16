import os
from random import randint

import requests
from colorama import Fore, Style

import config
import network
from pysqlsimplecipher.decryptor import decrypt_file


class DatabaseService:
    @staticmethod
    def fetch_latest():
        res = network.get_client_assets_database()
        dist_db_version = res['version']

        if config.client.gb_db_version == dist_db_version:
            print(Fore.GREEN + Style.BRIGHT + 'Database is already up to date')
            return

        print(Fore.RED + Style.BRIGHT + 'Downloading latest global database...')
        res = requests.get(res['url'], allow_redirects=True)
        config.game_env.db_path.parent.mkdir(exist_ok=True, parents=True)
        temp_db_name = str(config.game_env.db_path.parent.absolute()) + str(randint(10_000_00, 99_999_99)) + '.db'
        open(temp_db_name, 'wb').write(res.content)

        print(Fore.RED + Style.BRIGHT + 'Decrypting latests database... This can take a few minutes...')
        decrypt_file(temp_db_name, config.game_env.db_password, str(config.game_env.db_path.absolute()))
        config.client.gb_db_version = dist_db_version
        config.client.save()
        os.remove(temp_db_name)
        print(Fore.GREEN + Style.BRIGHT + 'Database update complete.')
