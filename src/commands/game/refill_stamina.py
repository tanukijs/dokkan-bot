from colorama import Fore, Style

import network
from commands.game.get_user import get_user_command


def refill_stamina_command():
    # ## Restore user stamina

    stones = get_user_command()['user']['stone']
    if stones < 1:
        print(Fore.RED + Style.BRIGHT + 'You have no stones left...')
        return 0

    network.put_user_recover_act_with_stones()
    print(Fore.GREEN + Style.BRIGHT + 'STAMINA RESTORED')
