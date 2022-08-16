import requests
from colorama import Fore, init

import cli
import config
from classes.Game import GameEnvironment

init(autoreset=True)


# before anything a request for new URL & API port is required. - k1mpl0s
def check_servers(env: GameEnvironment):
    print('Checking servers...')
    try:
        url = env.url + '/ping'
        # we send an ancient version code that is valid.
        headers = {
            'X-Platform': 'android',
            'X-ClientVersion': env.version_code,
            'X-Language': 'en',
            'X-UserID': '////'
        }
        r = requests.get(url, data=None, headers=headers)
        # store our requested data into a variable as json.
        store = r.json()
        if 'error' in store:
            print(Fore.RED + '[' + env.name + ' server] ' + str(store['error']))
            return False
    except:
        print(Fore.RED + '[' + env.name + ' server] can\'t connect.')
        return False
    return True


if check_servers(config.game_env):
    cli.run()
else:
    print(Fore.RED + 'press ENTER to close...')
    input()
    exit()
