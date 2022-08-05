import os

import config
from colorama import Fore, Style

from classes.Game import GameAccount
from commands.game.refresh_client import refresh_client_command


def load_account_command():
  while True:
    save_name = input("What save would you like to load?: ")
    file_path = os.path.join('saves', save_name)

    if not os.path.isfile(file_path):
      print(Fore.RED + Style.BRIGHT + "Could not find " + save_name)
    else:
      try:
        f = open(file_path, 'r')
        config.game_account = GameAccount(
          identifier=f.readline().rstrip(),
          ad_id=f.readline().rstrip(),
          unique_id=f.readline().rstrip(),
        )
        config.game_platform = config.IOS_PLATFORM if f.readline().rstrip() == 'ios' else config.ANDROID_PLATFORM
        client = f.readline().rstrip()
        if config.game_env.name == client:
          config.last_save_name = save_name
          break
        else:
          print(Fore.RED + Style.BRIGHT + 'Save does not match client version.')
      except Exception as e:
        print(e)

  refresh_client_command()
