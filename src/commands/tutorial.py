import random

from colorama import Fore, Style

import network
from config import GameContext

__OTHER_NAMES = ['777Tanuki', 'TanukiJs']
__MAIN_CHARACTERS = ['SonGoku', 'Bulma', 'Krillin', 'Piccolo', 'SonGohan', 'Vegeta', 'Trunks']
__SECONDARY_CHARACTERS = ['Bardock', 'MasterRoshi', 'Yamcha', 'TienShinhan', 'Chiaotzu', 'Android18', 'SonGoten', 'Beerus', 'Whis']
__ANTAGONISTS = ['PilafGang', 'RedRibbonArmy', 'KingPiccolo', 'GarlicJr.', 'Frieza', 'Cell', 'Broly', 'MajinBuu', 'GokuBlack', 'Zamasu']
__CHARACTER_NAMES = [*__OTHER_NAMES, *__MAIN_CHARACTERS, *__SECONDARY_CHARACTERS, *__ANTAGONISTS]


NAME = 'tutorial'
DESCRIPTION = 'Completes the tutorial'
CONTEXT = [GameContext.GAME]


def run():
    user = network.get_user()
    tutorial_is_finished = user['user']['tutorial']['is_finished']
    tutorial_progress = user['user']['tutorial']['progress']
    if tutorial_is_finished:
        return

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial 1/6: passing 5 first scenes')
    if tutorial_progress < 10201: network.put_tutorial(10201)
    if tutorial_progress < 20101: network.put_tutorial(20101)
    if tutorial_progress < 30101: network.put_tutorial(30101)
    if tutorial_progress < 40101: network.put_tutorial(40101)
    if tutorial_progress < 50101: network.put_tutorial(50101)

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial 2/6: drawing cards')
    if tutorial_progress < 60101:
        network.post_tutorial_gasha(60101)
        network.put_tutorial(60101)

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial 3/6: passing 8 other scenes')
    if tutorial_progress < 70101: network.put_tutorial(70101)
    if tutorial_progress < 80101: network.put_tutorial(80101)
    if tutorial_progress < 90101: network.put_tutorial(90101)
    if tutorial_progress < 100101: network.put_tutorial(100101)
    if tutorial_progress < 110101: network.put_tutorial(110101)
    if tutorial_progress < 120101: network.put_tutorial(120101)
    if tutorial_progress < 15010: network.put_tutorial(15010)
    if tutorial_progress < 160101: network.put_tutorial(160101)

    character_name = random.choice(__CHARACTER_NAMES)
    print(Fore.CYAN + Style.BRIGHT + 'Tutorial 4/6: randomly renaming you as ' + character_name)
    network.put_user(name=character_name)

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial 5/6: finishing tutorial')
    network.put_tutorial_finish()

    print(Fore.CYAN + Style.BRIGHT + 'Tutorial 6/6: post tutorial processing')
    network.get_user()
    network.post_missions_put_forward()
    network.put_apologies_accept()

    print(Fore.RED + Style.BRIGHT + 'Tutorial completed')
