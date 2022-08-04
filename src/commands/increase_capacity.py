import requests
from colorama import Fore, Style

import config
from network.utils import generate_headers


def increase_capacity_command():
    # Increases account card capacity by 5 every time it is called

    headers = generate_headers('POST', '/user/capacity/card')
    url = config.gb_url + '/user/capacity/card'

    r = requests.post(url, headers=headers)
    if 'error' in r.json():
        print(Fore.RED + Style.BRIGHT + str(r.json()))
    else:
        print(Fore.GREEN + Style.BRIGHT + 'Card capacity +5')
