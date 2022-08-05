import os

import config
from colorama import Fore, Style
from commands.game.create_file import create_file_command


def save_account_command(reroll_state):
  os.makedirs('saves', exist_ok=True)
  file_path = os.path.join('saves', config.last_save_name)
  if reroll_state:
    create_file_command(file_path, config.last_save_name)
    return

  valid_save = False
  while not valid_save:
    save_name = input("What would you like to name the file?")
    while save_name.isalnum() == 0:
      print(Fore.RED + Style.BRIGHT + "Name not allowed!")
      save_name = input('What would you like to name this save?: ')

    file_path = os.path.join('saves', save_name)
    if os.path.exists(file_path):
      overwrite_file = input("File by that name already exists. Overwrite? Y/N ")
      if overwrite_file == 'Y' or overwrite_file == 'y':
        create_file_command(file_path, save_name)
        config.last_save_name = save_name
        break
      else:
        print('Please choose another name!')
    else:
      create_file_command(file_path, save_name)
      config.last_save_name = save_name
      break
