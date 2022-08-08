from colorama import Fore, Style

import network
from commands.game.stage import complete_stage_command


def dragonballs_command():
    is_got = 0
    ###Check for Dragonballs
    r = network.get_dragonball_sets()
    if 'error' in r:
        print(Fore.RED + Style.BRIGHT + str(r))
        return 0

    ####Determine which dragonball set is being used
    set = r['dragonball_sets'][0]['id']

    ### Complete stages and count dragonballs
    for dragonball in r['dragonball_sets']:
        for db in reversed(dragonball['dragonballs']):
            if db['is_got'] == True:
                is_got += 1
            elif db['is_got'] == False:
                is_got += 1
                complete_stage_command(str(db['quest_id']), db['difficulties'][0])

    ### If all dragonballs found then wish
    if is_got == 7:
        r = network.get_dragonball_sets_wishes(str(set))
        if 'error' in r:
            print(Fore.RED + Style.BRIGHT + str(r))
            return 0
        wish_ids = []
        for wish in r['dragonball_wishes']:
            if wish['is_wishable']:
                print('#########################')
                print('Wish ID: ' + str(wish['id']))
                wish_ids.append(str(wish['id']))
                print(wish['title'])
                print(wish['description'])
                print('')

        print(Fore.YELLOW + 'What wish would you like to ask shenron for? ID: ', end='')
        choice = input()
        while choice not in wish_ids:
            print("Shenron did not understand you! ID: ", end='')
            choice = input()
        wish_ids[:] = []
        r = network.post_dragonball_sets_wishes(str(set), [int(choice)])
        if 'error' in r:
            print(Fore.RED + Style.BRIGHT + str(r))
        else:
            print(Fore.YELLOW + 'Wish granted!')
            print('')

        dragonballs_command()

        return 0
