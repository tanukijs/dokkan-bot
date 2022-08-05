from colorama import Fore, Style

import config


def set_platform_command(reroll_state):
  if reroll_state:
    return

  while True:
    print(
      'Choose your operating system (' + Fore.YELLOW + Style.BRIGHT + 'Android: 1' + Style.RESET_ALL + ' or' + Fore.YELLOW + Style.BRIGHT + ' IOS: 2' + Style.RESET_ALL + ')',
      end='')
    platform = input('')
    if platform[0].lower() in ['1', '2']:
      if platform[0].lower() == '1':
        config.game_platform = config.ANDROID_PLATFORM
      else:
        config.game_platform = config.IOS_PLATFORM
      break
    else:
      print(Fore.RED + 'Could not identify correct operating system to use.')
