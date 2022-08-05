from colorama import Fore, Style

import network


def increase_capacity_command():
    # Increases account card capacity by 5 every time it is called
    r = network.post_user_capacity_card()
    if 'error' in r:
        print(Fore.RED + Style.BRIGHT + str(r))
    else:
        print(Fore.GREEN + Style.BRIGHT + 'Card capacity +5')
