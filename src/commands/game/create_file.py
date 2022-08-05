import os

from colorama import Fore, Style

import config


def create_file_command(filename, save_name):
  try:
    f = open(os.path.join(filename), 'w')
    f.write(str(config.identifier) + '\n')
    f.write(str(config.AdId) + '\n')
    f.write(str(config.UniqueId) + '\n')
    f.write(str(config.game_platform.name) + '\n')
    f.write(str(config.game_env.name) + '\n')
    f.close()
    print('--------------------------------------------')
    print(Fore.CYAN + Style.BRIGHT + 'Written details to file: ' + save_name)
    print(Fore.RED + Style.BRIGHT + 'If ' + save_name + ' is deleted your account will be lost!')
    print('--------------------------------------------')
  except Exception as e:
    print(e)
