from colorama import Fore, Style

import network


def tutorial_command():
    # ##Progress NULL TUTORIAL FINISH

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 1/8')
    network.put_tutorial_finish()

    # ##Progress NULL Gasha
    network.post_tutorial_gasha()
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 2/8')

    # ##Progress to 999%

    network.put_tutorial('999')
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 3/8')

    # ##Change User name
    network.put_user(name="Naruto")
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 4/8')

    # ##/missions/put_forward
    network.post_missions_put_forward()
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 5/8')

    # ##Apologies accept
    network.put_apologies_accept()

    # ##On Demand
    network.put_user(is_ondemand=True)
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 6/8')

    # ##Hidden potential releasable

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 7/8')
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial Progress: 8/8')
    print(Fore.RED + Style.BRIGHT + 'TUTORIAL COMPLETE')
